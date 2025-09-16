from sqlalchemy import select
from db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Word  # Assuming Edition is in a models module
from utils.logger import logger  # Assuming you have a logger module
from utils.config import SPECIAL_CHARACTERS, NUMBERS_TRANSLATION_TABLE
from typing import List, Dict
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls
from repositories.narrations_numbering_repo import get_narration_numbering_from_hafs


async def get_line_number(session: AsyncSession, surah_number: int, ayah_number: int, position: int):
    """
    Retrieve the line number of a word given its Surah number, Ayah number, and position.

    Args:
        surah_number (int): The Surah ID.
        ayah_number (int): The Ayah number within the Surah.
        position (int): The position of the word in the Ayah.

    Returns:
        int: The line number if found.
        None: If no matching word is found.

    Raises:
        SQLAlchemyError: If a database error occurs.
        RuntimeError: If an unexpected error occurs.
    """
    try:
        result = await session.execute(
            select(Word.line_number).filter(
                Word.surat_id == surah_number,
                Word.numberinsurat == ayah_number,
                Word.position == position
            )
        )
        line_number = result.scalar_one_or_none()

        if line_number is not None:
            return line_number
        else:
            logger.info(f"No line number found for Surah {surah_number}, Ayah {ayah_number}, Position {position}.")
            return None

    except Exception as e:
        logger.error(f"Unexpected error while fetching line number: {str(e)}", exc_info=True)
        raise RuntimeError("An unexpected error occurred, please try again later.")

async def get_line_numbers_without_position(session: AsyncSession, surah_number: int, ayah_numbers: list[int]):
    """
    Retrieve line numbers for a Surah given a list of Ayah numbers without specifying positions.

    Args:
        surah_number (int): The Surah ID.
        ayah_numbers (list[int]): A list of Ayah numbers.

    Returns:
        list: A list of (line_number,) tuples ordered by Ayah number and position.
        None: If no matching words are found.

    Raises:
        SQLAlchemyError: If a database error occurs.
        RuntimeError: If an unexpected error occurs.
    """
    try:
        result = await session.execute(
            select(Word.line_number).filter(
                Word.surat_id == surah_number,
                Word.numberinsurat.in_(ayah_numbers)
            ).order_by(Word.numberinsurat, Word.position)
        )
        line_numbers = result.all()

        if line_numbers:
            return line_numbers
        else:
            logger.info(f"No line numbers found for Surah {surah_number} and Ayahs {ayah_numbers}.")
            return None


    except Exception as e:
        logger.error(f"Unexpected error while fetching line numbers: {str(e)}", exc_info=True)
        raise RuntimeError("An unexpected error occurred, please try again later.")



async def get_words(
    surah_number: int,
    ayah_number: int,
    page_number: int,
    ayah_text: str,
    edition_id: str,
    last_ayah: Dict,
    is_narration: bool = False
) -> List[Dict]:
    try:
        ayah_text_list = ayah_text.strip().split()
        words_list = []
        index = 0
        word_position = 0

        # Replace session creation with the async session
        async with AsyncSessionLocal() as session:
            if not is_narration:
                for word in ayah_text_list:
                    word = word.strip()
                    if word in SPECIAL_CHARACTERS:
                        continue
                    line_number = await get_line_number(session, surah_number, ayah_number, word_position + 1)
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
                    word_position += 1   
            else:
                # Replace synchronous `getNarrationNumberingFromHafs` call
                hafs_numbers, target_numbers = await get_narration_numbering_from_hafs(
                    surah_number, ayah_number, edition_id
                )

                if len(hafs_numbers) == 1 and len(target_numbers) == 1:
                    ayah_in_hafs = hafs_numbers[0]
                    word_position = 0
                elif len(hafs_numbers) == 1 and len(target_numbers) > 1:
                    ayah_in_hafs = hafs_numbers[0]
                    if ayah_number == min(target_numbers):
                        word_position = 0
                    else:
                        word_position = (last_ayah["words"][-1]["position"]) - 1
                elif len(hafs_numbers) > 1 and len(target_numbers) == 1:
                    ayah_in_hafs = await get_line_numbers_without_position(session, surah_number, hafs_numbers)
                elif len(hafs_numbers) > 1 and len(target_numbers) > 1:
                    ayah_in_hafs = await get_line_numbers_without_position(session, surah_number, hafs_numbers)
                    if ayah_number == min(target_numbers):
                        word_position = 0
                    else:
                        word_position = (last_ayah["words"][-1]["position"]) - 1

                # Handling list of Hafs numbers
                if isinstance(ayah_in_hafs, list):
                    for word in ayah_text_list:
                        word = word.strip()
                        if word in SPECIAL_CHARACTERS:
                            continue
                        if word_position:
                            line_number = ayah_in_hafs[word_position][0]
                            word_position += 1
                        else:
                            line_number = ayah_in_hafs[index][0]
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
                    for word in ayah_text_list:
                        word = word.strip()
                        if word in SPECIAL_CHARACTERS:
                            continue
                        line_number = await get_line_number(session, surah_number, ayah_in_hafs, word_position + 1)
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
                        word_position += 1

            # Add Ayah ending symbol
            words_list.append({
                "text": str(ayah_number).translate(NUMBERS_TRANSLATION_TABLE),
                "char_type_name": "end",
                "position": len(ayah_text_list) + 1,
                "line_number": words_list[-1]["line_number"],
                "verse_key": f"{surah_number}:{ayah_number}",
                "location": f"{surah_number}:{ayah_number}:{len(ayah_text_list) + 1}",
                "page_number": page_number
            })

        return words_list

    except Exception as e:
        logger.error(f"An exception occurred in get_words: {str(e)}", exc_info=True)
        return []
