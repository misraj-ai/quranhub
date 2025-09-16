from sqlalchemy.future import select
from db.session import AsyncSessionLocal  # Assuming AsyncSessionLocal is defined for async sessions
from utils.logger import logger
from db.models import Ayat, Surat  # Assuming these are imported correctly
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls


async def get_hizb_quarter(hizb_quarter_number: int, edition_identifier: str, limit: int, offset: int):
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
                    Ayat.hizbquarter_id,
                    Ayat.sajda_id,
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.revelationcity,
                    Surat.numberofayats
                ).join(Surat, Ayat.surat_id == Surat.id)
                 .filter(Ayat.hizbquarter_id == hizb_quarter_number, Ayat.edition_id == edition_id)
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
                "hizbQuarter": item.hizbquarter_id,
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

        return {"number": hizb_quarter_number, "ayahs": ayahs, "surahs": surahs, "edition": edition_info}

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching this hizb quarter data."
