from sqlalchemy import select, func
from db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Word
from utils.logger import logger
from utils.config import SPECIAL_CHARACTERS, NUMBERS_TRANSLATION_TABLE, BASIC_TAJWEED_RULES
from typing import List, Dict, Optional, Tuple
from repositories.narrations_numbering_repo import get_hafs_verse_for_narration_verse

# Special narration page splits: split a merged narration ayah across pages
# Keyed by (edition_id, surah, ayah)
SPECIAL_NARRATION_PAGE_SPLITS = {
    ("quran-aldouri", 2, 219): True,
    ("quran-aldouri",14,33): True,
    ("quran-aldouri",4,44): True,
    ("quran-alsoosi", 2, 219): True,
    ("quran-alsoosi", 4, 44): True,
    ("quran-alsoosi", 7, 29): True,
    ("quran-alsoosi",14,33): True,
    ("quran-qaloon", 4, 44): True,
    ("quran-qaloon", 24, 36): True,
    ("quran-qaloon", 24, 42): True,
    ("quran-qunbul", 4, 44): True,
    ("quran-qunbul", 24, 36): True,
    ("quran-qunbul", 24, 42): True,
    ("quran-albazzi", 4, 44): True,
    ("quran-albazzi", 24, 36): True,
    ("quran-albazzi", 24, 42): True,
    ("quran-warsh",4,44): True,
    ("quran-warsh",20,86): True,
    ("quran-warsh",24,36): True,
    ("quran-warsh",24,42): True,

}



def _filter_tajweed_rules(tajweed_data: Dict, level: str) -> Dict:
    """Filter tajweed rules based on level ('basic' or 'advanced')."""
    if not tajweed_data or level == "advanced":
        return tajweed_data
    
    # Basic level: filter rules
    if "rules" in tajweed_data:
        filtered_rules = [
            rule for rule in tajweed_data["rules"]
            if rule.get("cls") in BASIC_TAJWEED_RULES
        ]
        # Return a new dict to avoid mutating original if cached/shared
        new_data = tajweed_data.copy()
        new_data["rules"] = filtered_rules
        return new_data
        
    return tajweed_data


async def get_word_metadata(
    session: AsyncSession, 
    surah_number: int, 
    ayah_number: int, 
    position: int,
    include_tajweed: bool = False,
    tajweed_level: str = "basic",
    line_map: Dict[int, int] = None
) -> Dict:
    """Retrieve metadata for a word given its Surah number, Ayah number, and position."""
    try:
        columns = [Word.id, Word.line_number]
        if include_tajweed:
            columns.append(Word.tajweed)
            
        result = await session.execute(
            select(*columns).filter(
                Word.surat_id == surah_number,
                Word.numberinsurat == ayah_number,
                Word.position == position
            )
        )
        row = result.first()
        if not row:
            return {"line_number": None, "tajweed": None} if include_tajweed else {"line_number": None}
            
        # Use line_map override if available for this specific word ID
        line_number = row.line_number
        if line_map and row.id in line_map:
            line_number = line_map[row.id]

        data = {
            "line_number": line_number
        }
        if include_tajweed:
            data["tajweed"] = _filter_tajweed_rules(row.tajweed, tajweed_level)
        return data
    except Exception as e:
        logger.error(f"Error fetching word metadata: {str(e)}", exc_info=True)
        return {"line_number": None, "tajweed": None} if include_tajweed else {"line_number": None}


async def get_words_metadata_map(
    session: AsyncSession,
    surah_number: int,
    ayah_numbers: List[int],
    include_tajweed: bool = False,
    tajweed_level: str = "basic",
    line_map: Dict[int, int] = None
) -> Dict[int, Dict[int, Dict]]:
    """
    Fetch metadata for all words in the given ayahs at once.
    Returns a map: {ayah_number: {position: {line_number, tajweed}}}
    """
    try:
        columns = [Word.id, Word.numberinsurat, Word.position, Word.line_number]
        if include_tajweed:
            columns.append(Word.tajweed)
            
        result = await session.execute(
            select(*columns).filter(
                Word.surat_id == surah_number,
                Word.numberinsurat.in_(ayah_numbers)
            )
        )
        
        metadata_map = {}
        for row in result:
            ayah = row.numberinsurat
            pos = row.position
            if ayah not in metadata_map:
                metadata_map[ayah] = {}
            
            # Use line_map override if available for this specific word ID
            line_number = row.line_number
            if line_map and row.id in line_map:
                line_number = line_map[row.id]

            data = {
                "line_number": line_number
            }
            if include_tajweed:
                data["tajweed"] = _filter_tajweed_rules(row.tajweed, tajweed_level)
                
            metadata_map[ayah][pos] = data
            
        return metadata_map
    except Exception as e:
        logger.error(f"Error fetching words metadata map: {str(e)}", exc_info=True)
        return {}


async def get_cumulative_word_positions_for_hafs_ayahs(
    session: AsyncSession,
    surah_number: int,
    hafs_ayah_numbers: List[int]
) -> Dict[int, Tuple[int, int]]:
    """Build a cumulative position map for Hafs ayahs."""
    position_map = {}
    cumulative_pos = 0
    
    for hafs_ayah in sorted(hafs_ayah_numbers):
        count_result = await session.execute(
            select(func.count(Word.id)).filter(
                Word.surat_id == surah_number,
                Word.numberinsurat == hafs_ayah
            )
        )
        word_count = count_result.scalar() or 0
        
        if word_count == 0:
            logger.warning(f"Hafs {surah_number}:{hafs_ayah} has no words")
            continue
        
        for pos_in_ayah in range(1, word_count + 1):
            cumulative_pos += 1
            position_map[cumulative_pos] = (hafs_ayah, pos_in_ayah)
    
    logger.info(
        f"Built position map for Hafs ayahs {hafs_ayah_numbers}: "
        f"{len(position_map)} total positions"
    )
    
    return position_map


async def get_word_metadata_by_position_mapping(
    session: AsyncSession,
    surah_number: int,
    narration_word_count: int,
    hafs_ayah_numbers: List[int],
    word_offset: int = 0,
    include_tajweed: bool = False,
    tajweed_level: str = "basic",
    line_map: Dict[int, int] = None
) -> List[Dict]:
    """
    Get word metadata by mapping narration word positions to Hafs word positions.
    Automatically extends Hafs range if narration has more words.
    """
    # Build initial position map
    position_map = await get_cumulative_word_positions_for_hafs_ayahs(
        session, surah_number, hafs_ayah_numbers
    )
    
    if not position_map:
        logger.error(f"No position map built for Hafs ayahs {hafs_ayah_numbers}")
        # Return list of empty metadata
        empty_md = {"line_number": None}
        if include_tajweed: empty_md["tajweed"] = None
        return [empty_md] * narration_word_count
    
    max_position = max(position_map.keys())
    total_needed = word_offset + narration_word_count
    
    # Track which Hafs ayahs we need to fetch metadata for
    all_needed_hafs_ayahs = set(hafs_ayah_numbers)

    # Extend Hafs range if needed
    if total_needed > max_position:
        logger.warning(
            f"Need {total_needed} positions but have {max_position}. "
            f"Extending Hafs range from ayah {max(hafs_ayah_numbers) + 1}..."
        )
        
        next_ayah = max(hafs_ayah_numbers) + 1
        extended_count = 0
        
        while max_position < total_needed and extended_count < 20:
            count_result = await session.execute(
                select(func.count(Word.id)).filter(
                    Word.surat_id == surah_number,
                    Word.numberinsurat == next_ayah
                )
            )
            word_count = count_result.scalar() or 0
            
            if word_count == 0:
                logger.warning(f"Hafs {surah_number}:{next_ayah} doesn't exist")
                break
            
            all_needed_hafs_ayahs.add(next_ayah)
            # Add words from this ayah to position map
            for pos_in_ayah in range(1, word_count + 1):
                max_position += 1
                position_map[max_position] = (next_ayah, pos_in_ayah)
            
            logger.info(
                f"Extended with Hafs {next_ayah} ({word_count} words), "
                f"now {max_position} total"
            )
            
            next_ayah += 1
            extended_count += 1
    
    # Fetch all metadata at once
    metadata_map = await get_words_metadata_map(
        session, surah_number, list(all_needed_hafs_ayahs), include_tajweed, tajweed_level, line_map
    )

    # Map narration words to Hafs words
    result_metadata = []
    
    for narration_pos in range(1, narration_word_count + 1):
        cumulative_pos = word_offset + narration_pos
        
        if cumulative_pos in position_map:
            hafs_ayah, hafs_pos = position_map[cumulative_pos]
            md = metadata_map.get(hafs_ayah, {}).get(hafs_pos)
            if not md:
                md = {"line_number": None}
                if include_tajweed: md["tajweed"] = None
            
            logger.debug(
                f"Pos {narration_pos} (cum {cumulative_pos}) → "
                f"Hafs {hafs_ayah}:{hafs_pos} → line {md.get('line_number')}"
            )
        else:
            # Use last valid metadata as fallback
            logger.warning(
                f"Position {cumulative_pos} exceeds max {max_position}"
            )
            
            hafs_ayah, hafs_pos = position_map[max(position_map.keys())]
            md = metadata_map.get(hafs_ayah, {}).get(hafs_pos)
            if not md:
                md = {"line_number": None}
                if include_tajweed: md["tajweed"] = None
            
            # If no metadata found and we have previous results, fallback further
            if md.get("line_number") is None and result_metadata:
                for prev_md in reversed(result_metadata):
                    if prev_md.get("line_number") is not None:
                        md = prev_md.copy()
                        break
        
        result_metadata.append(md)
    
    return result_metadata


async def get_line_numbers_by_position_mapping(
    session: AsyncSession,
    surah_number: int,
    narration_word_count: int,
    hafs_ayah_numbers: List[int],
    word_offset: int = 0,
    line_map: Dict[int, int] = None
) -> List[Optional[int]]:
    """Legacy helper for backward compatibility."""
    metadata = await get_word_metadata_by_position_mapping(
        session, surah_number, narration_word_count, hafs_ayah_numbers, word_offset, include_tajweed=False, line_map=line_map
    )
    return [m.get("line_number") for m in metadata]


async def get_words(
    surah_number: int,
    ayah_number: int,
    page_number: int,
    ayah_text: str,
    edition_id: str,
    last_ayah: Dict,
    is_narration: bool = False,
    include_tajweed: bool = False,
    tajweed_level: str = "basic",
    line_map: Dict[int, int] = None
) -> List[Dict]:
    """Get words with line numbers and optional tajweed for any edition."""
    try:
        ayah_text_list = ayah_text.strip().split()
        words_list = []
        index = 0

        async with AsyncSessionLocal() as session:
            if not is_narration:
                # HAFS - Direct Mapping
                # Fetch all metadata for the ayah at once
                metadata_map = await get_words_metadata_map(session, surah_number, [ayah_number], include_tajweed, tajweed_level, line_map)
                ayah_metadata = metadata_map.get(ayah_number, {})

                word_position = 0
                for word in ayah_text_list:
                    word = word.strip()
                    if word in SPECIAL_CHARACTERS:
                        continue
                    
                    word_position += 1
                    md = ayah_metadata.get(word_position, {})
                    
                    word_data = {
                        "text": word,
                        "char_type_name": "word", 
                        "position": index + 1,
                        "line_number": md.get("line_number"),
                        "verse_key": f"{surah_number}:{ayah_number}",
                        "location": f"{surah_number}:{ayah_number}:{index + 1}",
                        "page_number": page_number
                    }
                    if include_tajweed:
                        word_data["tajweed"] = md.get("tajweed")
                    
                    words_list.append(word_data)
                    index += 1
                    

            else:
                hafs_verses = await get_hafs_verse_for_narration_verse(
                    surah_number, ayah_number, edition_id
                )
                
                narration_words = [
                    w.strip() for w in ayah_text_list 
                    if w.strip() not in SPECIAL_CHARACTERS
                ]
                
                # Calculate offset for TRUE split continuations
                word_offset = 0
                if len(hafs_verses) == 1 and last_ayah:
                    prev_hafs_verses = await get_hafs_verse_for_narration_verse(
                        surah_number, ayah_number - 1, edition_id
                    )
                    if prev_hafs_verses == hafs_verses:
                        if "words" in last_ayah:
                            word_offset = sum(
                                1 for w in last_ayah["words"] 
                                if w.get("char_type_name") == "word"
                            )
                
                # Get all metadata via position mapping
                total_metadata = await get_word_metadata_by_position_mapping(
                    session,
                    surah_number,
                    len(narration_words),
                    hafs_verses,
                    word_offset,
                    include_tajweed,
                    tajweed_level,
                    line_map
                )

                next_page_cutover_idx = None

                # Special case: Aldouri numbering split across pages
                if (
                    SPECIAL_NARRATION_PAGE_SPLITS.get((edition_id, surah_number, ayah_number))
                    and len(hafs_verses) >= 1
                ):
                    count_result = await session.execute(
                        select(func.count(Word.id)).filter(
                            Word.surat_id == surah_number,
                            Word.numberinsurat == hafs_verses[0]
                        )
                    )
                    first_hafs_word_count = count_result.scalar() or 0
                    next_page_cutover_idx = max(0, first_hafs_word_count - (word_offset or 0))

                # Build words list
                word_idx = 0
                for word in ayah_text_list:
                    word = word.strip()
                    if word in SPECIAL_CHARACTERS:
                        continue
                    
                    md = total_metadata[word_idx] if word_idx < len(total_metadata) else {}
                    effective_page = page_number
                    if next_page_cutover_idx is not None and word_idx >= next_page_cutover_idx:
                        effective_page = page_number + 1

                    word_data = {
                        "text": word,
                        "char_type_name": "word",
                        "position": index + 1,
                        "line_number": md.get("line_number"),
                        "verse_key": f"{surah_number}:{ayah_number}",
                        "location": f"{surah_number}:{ayah_number}:{index + 1}",
                        "page_number": effective_page,
                    }
                    if include_tajweed:
                        word_data["tajweed"] = md.get("tajweed")

                    words_list.append(word_data)
                    index += 1
                    word_idx += 1

            # Add ending symbol
            if words_list:
                last_line = words_list[-1]["line_number"]
                last_page = words_list[-1].get("page_number", page_number)

                if last_line is None:
                    for w in reversed(words_list):
                        if w.get("line_number") is not None and last_line is None:
                            last_line = w["line_number"]
                        if w.get("page_number") is not None:
                            last_page = w["page_number"]
                        if last_line is not None and last_page is not None:
                            break

                end_word = {
                    "text": str(ayah_number).translate(NUMBERS_TRANSLATION_TABLE),
                    "char_type_name": "end",
                    "position": len(ayah_text_list) + 1,
                    "line_number": last_line,
                    "verse_key": f"{surah_number}:{ayah_number}",
                    "location": f"{surah_number}:{ayah_number}:{len(ayah_text_list) + 1}",
                    "page_number": last_page,
                }
                if include_tajweed:
                    end_word["tajweed"] = None
                    
                words_list.append(end_word)


        return words_list

    except Exception as e:
        logger.error(f"Exception in get_words: {str(e)}", exc_info=True)
        return []

