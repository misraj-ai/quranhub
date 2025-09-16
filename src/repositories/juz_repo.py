from sqlalchemy.future import select
from utils.logger import logger
from utils.config import DEFAULT_EDITION_IDENTIFIER
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from db.models import Ayat, Surat
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls
from db.session import AsyncSessionLocal  # Assuming AsyncSessionLocal is defined for async sessions

async def get_juz(juz_number, edition_identifier, limit, offset):
    try:
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # Error fetching edition
            return edition
        elif isinstance(edition, list):
            # Select the appropriate edition based on type
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]

        edition_id = edition.id
        if edition.format == "audio":
            text_edition = await get_text_edition_for_narrator(edition.identifier)
            if isinstance(text_edition, str):
                return text_edition
            edition_id = text_edition.id

        results = []
        surahs = []
        surahs_ids = []

        # Query Ayahs and Surah metadata asynchronously
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    Ayat.number,
                    Ayat.text,
                    Ayat.numberinsurat,
                    Ayat.juz_id,
                    Ayat.manzil_id,
                    Ayat.page_id,
                    Ayat.ruku_id,
                    Ayat.hizbquarter_id,
                    Ayat.sajda_id,
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.revelationcity,
                    Surat.numberofayats
                ).join(Surat, Ayat.surat_id == Surat.id).filter(
                    Ayat.juz_id == juz_number,
                    Ayat.edition_id == edition_id
                ).order_by(Ayat.number).limit(limit).offset(offset)
            )

            result = result.fetchall()

            if not result:
                return "Ayahs not found."

            # Process the result
            for item in result:
                ayah = {
                    "number": item.number,
                    "text": item.text,
                    "surah": {
                        "number": item.id,
                        "name": item.name,
                        "englishName": item.englishname,
                        "englishNameTranslation": item.englishtranslation,
                        "revelationType": item.revelationcity,
                        "numberOfAyahs": item.numberofayats
                    },
                    "numberInSurah": item.numberinsurat,
                    "juz": item.juz_id,
                    "manzil": item.manzil_id,
                    "page": item.page_id,
                    "ruku": item.ruku_id,
                    "hizbQuarter": item.hizbquarter_id,
                    "sajda": item.sajda_id if item.sajda_id else False
                }
                results.append(ayah)

                if item.id not in surahs_ids:
                    surahs.append({
                        "number": item.id,
                        "name": item.name,
                        "englishName": item.englishname,
                        "englishNameTranslation": item.englishtranslation,
                        "revelationType": item.revelationcity,
                        "numberOfAyahs": item.numberofayats
                    })
                    surahs_ids.append(item.id)

        # If edition format is audio, add audio URLs for the Ayahs
        if edition.format == "audio":
            bitrates = edition.bitrates
            max_bitrate = max(bitrates)
            remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
            for item in results:
                item["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, item["number"])
                item["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, item["number"])

        edition_data = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name,
            "englishName": edition.englishname,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        return {"number": juz_number, "ayahs": results, "surahs": surahs, "edition": edition_data}

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching the juz data."

# Add after the existing get_juz function

async def get_all_juzs(edition_identifier=DEFAULT_EDITION_IDENTIFIER):
    try:
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # Error fetching edition
            return edition
        elif isinstance(edition, list):
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]

        edition_id = edition.id
        if edition.format == "audio":
            text_edition = await get_text_edition_for_narrator(edition.identifier)
            if isinstance(text_edition, str):
                return text_edition
            edition_id = text_edition.id
            
        juzs_info = []

        async with AsyncSessionLocal() as session:
            # Query first ayah of each juz in a single query
            result = await session.execute(
                select(
                    Ayat.juz_id,
                    Ayat.number,
                    Ayat.text,
                    Ayat.numberinsurat,
                    Ayat.page_id,
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.revelationcity,
                    Surat.numberofayats
                ).join(Surat, Ayat.surat_id == Surat.id).filter(
                    Ayat.edition_id == edition_id
                ).order_by(Ayat.juz_id, Ayat.number)
            )

            fetched_data = result.fetchall()
            juz_data_map = {}

            # Process the fetched data to group by juz_id
            for item in fetched_data:
                juz_id = item.juz_id
                if juz_id not in juz_data_map:
                    juz_data_map[juz_id] = {
                        "number": juz_id,
                        "firstPage": item.page_id,
                        "firstAyah": {
                            "number": item.number,
                            "text": item.text,
                            "numberInSurah": item.numberinsurat,
                        },
                        "firstSurah": {
                            "number": item.id,
                            "name": item.name,
                            "englishName": item.englishname,
                            "englishNameTranslation": item.englishtranslation,
                            "revelationType": item.revelationcity,
                            "numberOfAyahs": item.numberofayats
                        }
                    }

            juzs_info = list(juz_data_map.values())

        if not juzs_info:
            return "No Juzs found."

        edition_data = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name,
            "englishName": edition.englishname,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        return {
            "juzs": juzs_info,
            "edition": edition_data
        }

    except Exception as e:
        logger.error("An exception occurred while fetching all juzs: %s", str(e))
        return "An error occurred while fetching all juzs data."