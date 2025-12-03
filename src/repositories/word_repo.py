from sqlalchemy import select, func
from db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Word
from utils.logger import logger
from utils.config import SPECIAL_CHARACTERS, NUMBERS_TRANSLATION_TABLE
from typing import List, Dict, Optional, Tuple
from repositories.narrations_numbering_repo import get_narration_numbering_from_hafs, get_hafs_verse_for_narration_verse

# Special narration page splits: split a merged narration ayah across pages
# Keyed by (edition_id, surah, ayah)
SPECIAL_NARRATION_PAGE_SPLITS = {
    # Aldūrī 2:219 = Hafs 219 + 220, with page break between them
    ("quran-aldouri", 2, 219): True,
}


async def get_line_number(
    session: AsyncSession, 
    surah_number: int, 
    ayah_number: int, 
    position: int
) -> Optional[int]:
    """Retrieve the line number of a word given its Surah number, Ayah number, and position."""
    try:
        result = await session.execute(
            select(Word.line_number).filter(
                Word.surat_id == surah_number,
                Word.numberinsurat == ayah_number,
                Word.position == position
            )
        )
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error fetching line number: {str(e)}", exc_info=True)
        return None


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


async def get_line_numbers_by_position_mapping(
    session: AsyncSession,
    surah_number: int,
    narration_word_count: int,
    hafs_ayah_numbers: List[int],
    word_offset: int = 0
) -> List[Optional[int]]:
    """
    Get line numbers by mapping narration word positions to Hafs word positions.
    Automatically extends Hafs range if narration has more words.
    """
    # Build initial position map
    position_map = await get_cumulative_word_positions_for_hafs_ayahs(
        session, surah_number, hafs_ayah_numbers
    )
    
    if not position_map:
        logger.error(f"No position map built for Hafs ayahs {hafs_ayah_numbers}")
        return [None] * narration_word_count
    
    max_position = max(position_map.keys())
    total_needed = word_offset + narration_word_count
    
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
    
    # Map narration words to Hafs words
    line_numbers = []
    
    for narration_pos in range(1, narration_word_count + 1):
        cumulative_pos = word_offset + narration_pos
        
        if cumulative_pos in position_map:
            hafs_ayah, hafs_pos = position_map[cumulative_pos]
            line_number = await get_line_number(
                session, surah_number, hafs_ayah, hafs_pos
            )
            
            logger.debug(
                f"Pos {narration_pos} (cum {cumulative_pos}) → "
                f"Hafs {hafs_ayah}:{hafs_pos} → line {line_number}"
            )
        else:
            # Use last valid line as fallback
            logger.warning(
                f"Position {cumulative_pos} exceeds max {max_position}"
            )
            
            hafs_ayah, hafs_pos = position_map[max(position_map.keys())]
            line_number = await get_line_number(
                session, surah_number, hafs_ayah, hafs_pos
            )
            
            if line_number is None and line_numbers:
                for prev_line in reversed(line_numbers):
                    if prev_line is not None:
                        line_number = prev_line
                        break
        
        line_numbers.append(line_number)
    
    return line_numbers


async def get_words(
    surah_number: int,
    ayah_number: int,
    page_number: int,
    ayah_text: str,
    edition_id: str,
    last_ayah: Dict,
    is_narration: bool = False
) -> List[Dict]:
    """Get words with line numbers for any edition (Hafs or narration)."""
    try:
        ayah_text_list = ayah_text.strip().split()
        words_list = []
        index = 0

        async with AsyncSessionLocal() as session:
            if not is_narration:
                # HAFS - Direct Mapping
                word_position = 0
                for word in ayah_text_list:
                    word = word.strip()
                    if word in SPECIAL_CHARACTERS:
                        continue
                    
                    word_position += 1
                    line_number = await get_line_number(
                        session, surah_number, ayah_number, word_position
                    )
                    
                    words_list.append({
                        "text": word,
                        "char_type_name": "word", 
                        "position": index + 1,
                        "line_number": line_number,
                        "verse_key": f"{surah_number}:{ayah_number}",
                        "location": f"{surah_number}:{ayah_number}:{index + 1}",
                        "page_number": page_number
                    })
                    index += 1
                    

            else:
                hafs_verses = await get_hafs_verse_for_narration_verse(
                    surah_number, ayah_number, edition_id
                )
                
                narration_words = [
                    w.strip() for w in ayah_text_list 
                    if w.strip() not in SPECIAL_CHARACTERS
                ]
                
                # Get all mapping info for context
                hafs_numbers, target_numbers = await get_narration_numbering_from_hafs(
                    surah_number, ayah_number, edition_id
                )
                
                if not hafs_numbers:
                    hafs_numbers = [ayah_number]
                    target_numbers = [ayah_number]
                
                # CRITICAL FIX: Calculate offset ONLY for TRUE split continuations
                word_offset = 0
                
                # A TRUE split continuation means:
                # 1. This narration verse uses the SAME Hafs verse as the previous narration verse
                # 2. We're not the first narration verse using this Hafs verse
                
                if len(hafs_verses) == 1 and last_ayah:
                    # Check if previous verse also used this same Hafs verse
                    prev_hafs_verses = await get_hafs_verse_for_narration_verse(
                        surah_number, ayah_number - 1, edition_id
                    )
                    
                    # If previous verse used the SAME Hafs verse, we're a continuation
                    if prev_hafs_verses == hafs_verses:
                        # This is a split continuation - calculate offset
                        if "words" in last_ayah:
                            word_offset = sum(
                                1 for w in last_ayah["words"] 
                                if w.get("char_type_name") == "word"
                            )
                        logger.info(
                            f"SPLIT continuation detected: {edition_id} {surah_number}:{ayah_number} "
                            f"shares Hafs {hafs_verses} with previous verse (offset {word_offset})"
                        )
                
                logger.info(
                    f"{edition_id} {surah_number}:{ayah_number} → Hafs {hafs_verses} (offset {word_offset})"
                )
                
                # Get line numbers using SPECIFIC Hafs verses
                line_numbers = await get_line_numbers_by_position_mapping(
                    session,
                    surah_number,
                    len(narration_words),
                    hafs_verses,
                    word_offset
                )
                next_page_cutover_idx = None

                # Special case: Aldouri numbering where 2:219 = Hafs 219 + 220 split across pages
                if (
                    SPECIAL_NARRATION_PAGE_SPLITS.get((edition_id, surah_number, ayah_number))
                    and len(hafs_verses) >= 1
                ):
                    # Count words of the FIRST Hafs ayah (here: Hafs 2:219)
                    count_result = await session.execute(
                        select(func.count(Word.id)).filter(
                            Word.surat_id == surah_number,
                            Word.numberinsurat == hafs_verses[0]
                        )
                    )
                    first_hafs_word_count = count_result.scalar() or 0

                    # Respect any offset (usually 0 for this case)
                    next_page_cutover_idx = max(0, first_hafs_word_count - (word_offset or 0))

                    logger.info(
                        f"SPECIAL SPLIT applied for {edition_id} {surah_number}:{ayah_number} – "
                        f"cut after {first_hafs_word_count} Hafs words (offset {word_offset}, "
                        f"next_page_cutover_idx={next_page_cutover_idx})"
                    )



                # Build words list
                word_idx = 0
                for word in ayah_text_list:
                    word = word.strip()
                    if word in SPECIAL_CHARACTERS:
                        continue
                    
                    line_number = line_numbers[word_idx] if word_idx < len(line_numbers) else None
                    effective_page = page_number
                    if next_page_cutover_idx is not None and word_idx >= next_page_cutover_idx:
                        effective_page = page_number + 1

                    words_list.append({
                        "text": word,
                        "char_type_name": "word",
                        "position": index + 1,
                        "line_number": line_number,
                        "verse_key": f"{surah_number}:{ayah_number}",
                        "location": f"{surah_number}:{ayah_number}:{index + 1}",
                        "page_number": effective_page,
                    })
                    index += 1
                    word_idx += 1

            # Add ending symbol
            if words_list:
                last_line = words_list[-1]["line_number"]
                last_page = words_list[-1].get("page_number", page_number)

                if last_line is None:
                    for w in reversed(words_list):
                        if w.get("line_number") is not None:
                            last_line = w["line_number"]
                        if w.get("page_number") is not None:
                            last_page = w["page_number"]
                        if last_line is not None and last_page is not None:
                            break

                words_list.append({
                    "text": str(ayah_number).translate(NUMBERS_TRANSLATION_TABLE),
                    "char_type_name": "end",
                    "position": len(ayah_text_list) + 1,
                    "line_number": last_line,
                    "verse_key": f"{surah_number}:{ayah_number}",
                    "location": f"{surah_number}:{ayah_number}:{len(ayah_text_list) + 1}",
                    "page_number": last_page,
                })


        return words_list

    except Exception as e:
        logger.error(f"Exception in get_words: {str(e)}", exc_info=True)
        return []