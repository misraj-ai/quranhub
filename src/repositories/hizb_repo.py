from sqlalchemy.future import select
from db.models import Ayat, Surat
from db.session import AsyncSessionLocal
from typing import List
from utils.logger import logger
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls

async def get_hizb_numbers(page_number: int, edition_id: str) -> List[int]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ayat.hizb_id)
            .filter(Ayat.edition_id == edition_id, Ayat.page_id == page_number)
            .distinct()
        )
        distinct_hizb_ids = result.scalars().all()
    
    return distinct_hizb_ids

async def get_hizb(hizb_number: int, edition_identifier: str, limit: int, offset: int):
    try:
        # Retrieve the edition asynchronously
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):
            return edition
        elif isinstance(edition, list):
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]
        
        edition_id = edition.id
        if edition.format == "audio":
            text_edition = await get_text_edition_for_narrator(edition.identifier)
            if isinstance(text_edition, str):
                return text_edition
            edition_id = text_edition.id

        async with AsyncSessionLocal() as session:
            # Perform the query asynchronously
            result = await session.execute(
                select(
                    Ayat.number,
                    Ayat.text,
                    Ayat.numberinsurat,
                    Ayat.juz_id,
                    Ayat.manzil_id,
                    Ayat.page_id,
                    Ayat.ruku_id,
                    Ayat.hizb_id,
                    Ayat.sajda_id,
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.revelationcity,
                    Surat.numberofayats
                ).join(Surat, Ayat.surat_id == Surat.id)
                 .filter(Ayat.hizb_id == hizb_number, Ayat.edition_id == edition_id)
                 .order_by(Ayat.number)
                 .limit(limit)
                 .offset(offset)
            )
            result = result.all()

        ayahs = []
        surahs = []
        surahs_ids = []

        # Process the result
        for item in result:
            ayahs.append({
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
                "hizb": item.hizb_id,
                "sajda": item.sajda_id if item.sajda_id else False
            })
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

        # Audio handling for audio editions
        if edition.format == "audio":
            bitrates = edition.bitrates
            max_bitrate = max(bitrates)
            remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
            for item in ayahs:
                item["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, item["number"])
                item["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, item["number"])

        # Prepare edition information
        edition_info = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name,
            "englishName": edition.englishname,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        return {"number": hizb_number, "ayahs": ayahs, "surahs": surahs, "edition": edition_info}

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching the hizb data."
    
async def get_all_hizbs(edition_identifier=DEFAULT_EDITION_IDENTIFIER):
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
            
        hizbs_info = []

        async with AsyncSessionLocal() as session:
            # Query first ayah of each hizb in a single query
            result = await session.execute(
                select(
                    Ayat.hizb_id,
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
                ).order_by(Ayat.hizb_id, Ayat.number)
            )

            fetched_data = result.fetchall()
            hizb_data_map = {}

            # Process the fetched data to group by hizb_id
            for item in fetched_data:
                hizb_id = item.hizb_id
                if hizb_id not in hizb_data_map:
                    hizb_data_map[hizb_id] = {
                        "number": hizb_id,
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

            hizbs_info = list(hizb_data_map.values())

        if not hizbs_info:
            return "No Hizbs found."

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
            "hizbs": hizbs_info,
            "edition": edition_data
        }

    except Exception as e:
        logger.error("An exception occurred while fetching all hizbs: %s", str(e))
        return "An error occurred while fetching all hizbs data."