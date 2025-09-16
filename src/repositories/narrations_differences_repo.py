from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from db.session import AsyncSessionLocal
from db.models import NarrationsDifferences, Edition, Ayat  # Assuming these are your model classes
from utils.logger import logger  # Assuming you have a logger module
from pyarabic.araby import strip_tashkeel,strip_diacritics
from repositories.edition_repo import get_edition_by_identifier, get_audio_edition_by_max_bitrate, get_text_edition_for_narrator
from utils.helpers import remove_extra_spaces, find_indices,custom_sort, get_ayah_audio_url
from repositories.narrations_numbering_repo import get_narration_numbering_from_hafs, get_narration_numbering_from_narration
from utils.config import QURANIC_SYMBOLS_TRANSLATION_TABLE

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from db.models import NarrationsDifferences, Edition  # Assuming you have these models
from utils.logger import logger


async def get_narrations_differences_db(
    session: AsyncSession, 
    source_edition_id: int, 
    chosen_edition_id: int, 
    surah_id: int, 
    ayah_number_in_surah: int
):
    try:
        # Subquery: select difference_texts appearing only in one of the editions
        subquery = (
            select(NarrationsDifferences.difference_text)
            .filter(
                (NarrationsDifferences.edition_id == source_edition_id) | 
                (NarrationsDifferences.edition_id == chosen_edition_id),
                NarrationsDifferences.surat_id == surah_id,
                NarrationsDifferences.numberinsurat == ayah_number_in_surah,
            )
            .group_by(
                NarrationsDifferences.difference_text,
                NarrationsDifferences.difference_content,
            )
            .having(func.count(NarrationsDifferences.difference_text) == 1)
            .subquery()
        )

        # Main query: select difference details for the chosen edition only
        query = (
            select(
                NarrationsDifferences.difference_text,
                NarrationsDifferences.difference_content,
                Edition.name
            )
            .join(
                Edition, NarrationsDifferences.edition_id == Edition.id
            )
            .filter(
                (NarrationsDifferences.edition_id == chosen_edition_id),
                NarrationsDifferences.surat_id == surah_id,
                NarrationsDifferences.numberinsurat == ayah_number_in_surah,
                NarrationsDifferences.difference_text.in_(select(subquery.c.difference_text))
            )
            .distinct()
        )

        # Execute asynchronously
        result = await session.execute(query)

        # Return list of results
        return result.fetchall()

    except Exception as e:
        logger.error(f"Error in get_narrations_differences_db: {str(e)}", exc_info=True)
        return None




    
async def get_narrations_differences(page_number: int, source_edition_identifier: str, edition_identifiers: list):
    try:
        editions = []
        source_edition = await get_edition_by_identifier(source_edition_identifier)
        
        if source_edition.type != "narration":
            return "Please provide narration editions only."

        source_edition_id = source_edition.id
        hafs_edition_id = (await get_edition_by_identifier("quran-simple")).id
        
        for edition_identifier in edition_identifiers:
            result = await get_edition_by_identifier(edition_identifier)
            if isinstance(result, str):
                return result
            if result.type != "narration":
                return "Please provide narration editions only."
            editions.append(result)

        differences = []
        differences_list = []
        
        async with AsyncSessionLocal() as session:
            page_verses = (
                await session.execute(
                    select(Ayat.surat_id, Ayat.numberinsurat, Ayat.number)
                    .filter(Ayat.edition_id == source_edition_id, Ayat.page_id == page_number)
                    .order_by(Ayat.surat_id, Ayat.numberinsurat)
                )
            ).all()

            for verse in page_verses:
                # Access tuple elements using indexing instead of attributes
                verse_surat_id = verse[0]  # verse_surat_id
                verse_numberinsurat = verse[1]  # verse_numberinsurat

                # Now you can call the function with these values
                ayah_numbers_in_hafs, ayah_numbers_in_target_edition = await get_narration_numbering_from_hafs(
                    verse_surat_id, verse_numberinsurat, source_edition_identifier
                )
                
                ayah_text = []
                for verse_number in ayah_numbers_in_hafs:
                    ayah_part = await session.execute(
                        select(Ayat.text).filter(
                            Ayat.surat_id == verse_surat_id, 
                            Ayat.numberinsurat == verse_number,
                            Ayat.edition_id == hafs_edition_id
                        )
                    )
                    ayah_part = ayah_part.scalars().first()
                    ayah_text.append(ayah_part.strip())

                ayah_text = " ".join(ayah_text)
                ayah_text = ayah_text.translate(QURANIC_SYMBOLS_TRANSLATION_TABLE)

                is_splitted_ayah = False
                if len(ayah_numbers_in_target_edition) > 1:
                    ayah_text_max_number = await session.execute(
                        select(Ayat.text).filter(
                            Ayat.surat_id == verse_surat_id, 
                            Ayat.numberinsurat == min(ayah_numbers_in_target_edition),
                            Ayat.edition_id == source_edition_id
                        )
                    )
                    ayah_text_max_number = ayah_text_max_number.scalars().first()
                    ayah_text_max_number = ayah_text_max_number.translate(QURANIC_SYMBOLS_TRANSLATION_TABLE)
                    ayah_text_max_number = ayah_text_max_number.strip()
                    is_splitted_ayah = True
                    splitted_ayah_words = len(ayah_text_max_number.split())

                for verse_number in ayah_numbers_in_hafs:
                    for edition in editions:
                        # Always try to get audio edition for any narration identifier
                        try:
                            max_bitrate, audio_edition = await get_audio_edition_by_max_bitrate(edition.identifier)
                        except Exception:
                            audio_edition = None
                            max_bitrate = None
                            
                        # For differences, we need the text edition
                        if edition.format == "audio":
                            # If it's an audio edition, get the corresponding text edition for differences
                            edition_for_differences = await get_text_edition_for_narrator(edition.identifier)
                        else:
                            # If it's already a text edition, use it directly
                            edition_for_differences = edition
                            
                        verse_differences = await get_narrations_differences_db(
                            session, source_edition_id, edition_for_differences.id, verse_surat_id, verse_number
                        )

                        if verse_differences:
                            for difference in verse_differences:
                                difference_dict = {}
                                difference_text = difference.difference_text.translate(QURANIC_SYMBOLS_TRANSLATION_TABLE)
                                difference_text = difference_text.strip()
                                difference_text_content = {
                                    "text": difference_text,
                                    "content": difference.difference_content,
                                    "edition": difference.name
                                }

                                if difference_text_content in differences_list:
                                    continue
                                else:
                                    differences_list.append(difference_text_content)

                                if '-' in difference_text:
                                    difference_dict["words"] = []
                                else:
                                    ayah_text = strip_tashkeel(strip_diacritics(ayah_text.strip()))
                                    ayah_text = remove_extra_spaces(ayah_text)
                                    difference_text_indices = find_indices(ayah_text, difference_text)

                                    if difference_text_indices:
                                        difference_words = []
                                        verse_number_in_surah = verse_numberinsurat
                                        for element in difference_text_indices:
                                            word_position = element['index'] + 1
                                            if is_splitted_ayah:
                                                if word_position > splitted_ayah_words:
                                                    word_position -= splitted_ayah_words
                                                    verse_number_in_surah = max(ayah_numbers_in_target_edition)

                                            target_edition_ayah_number_in_surah = await get_narration_numbering_from_narration(
                                                verse_surat_id, verse_number_in_surah, source_edition_identifier, edition.identifier
                                            )
                                            target_min_number = min(target_edition_ayah_number_in_surah)

                                            stmt = (
                                                select(Ayat.number)
                                                .where(
                                                    Ayat.surat_id == verse_surat_id,
                                                    Ayat.numberinsurat == target_min_number,
                                                    Ayat.edition_id == edition.id
                                                )
                                            )

                                            result = await session.execute(stmt)
                                            target_edition_ayah_number = result.scalar_one_or_none()

                                            if audio_edition:
                                                audio_data = {
                                                    "url": get_ayah_audio_url(max_bitrate, audio_edition.identifier, target_edition_ayah_number),
                                                    "reader_name": audio_edition.name
                                                }
                                            else:
                                                audio_data = None

                                            difference_words.append({
                                                "text": element["word"],
                                                "location": f"{verse_surat_id}:{verse_number_in_surah}:{word_position}",
                                                "audio": audio_data
                                            })

                                        difference_dict["words"] = difference_words
                                    else:
                                        difference_dict["words"] = []

                                difference_dict["narrator_name"] = difference.name
                                difference_dict["difference_text"] = f"في قوله تعالى {{ {difference_text} }}"
                                difference_dict["difference_content"] = difference.difference_content
                                differences.append(difference_dict)

        differences = sorted(differences, key=custom_sort)
        return differences

    except Exception as e:
        logger.error(f"An exception occurred: {str(e)}", exc_info=True)
        return "An error occurred while fetching narration differences."
