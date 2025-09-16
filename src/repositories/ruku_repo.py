from sqlalchemy.future import select
from db.models import Ayat, Surat
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from utils.logger import logger
from db.session import AsyncSessionLocal
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls

async def get_ruku(ruku_number: int, edition_identifier: str, limit: int, offset: int):
    try:
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):
            return edition
        elif isinstance(edition, list):
            if edition[0].type == "versebyverse":
                edition = edition[0]
            else:
                edition = edition[1]

        edition_id = edition.id
        if edition.format == "audio":
            # Get text edition for the same narrator_identifier
            if edition.narrator_identifier:
                text_edition = await get_text_edition_for_narrator(edition.narrator_identifier)
            else:
                text_edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
            
            if isinstance(text_edition, str):
                return text_edition
            edition_id = text_edition.id

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
                )
                .join(Surat, Ayat.surat_id == Surat.id)
                .filter(Ayat.ruku_id == ruku_number, Ayat.edition_id == edition_id)
                .limit(limit)
                .offset(offset)
            )
            result = result.all()

        ayahs = []
        surahs = []
        surah_ids = []

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
            if item.id not in surah_ids:
                surahs.append({
                    "number": item.id,
                    "name": item.name,
                    "englishName": item.englishname,
                    "englishNameTranslation": item.englishtranslation,
                    "revelationType": item.revelationcity,
                    "numberOfAyahs": item.numberofayats
                })
                surah_ids.append(item.id)

        if edition.format == "audio":
            bitrates = edition.bitrates
            max_bitrate = max(bitrates)
            remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
            for item in ayahs:
                item["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, item["number"])
                item["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, item["number"])

        edition_info = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name,
            "englishName": edition.englishname,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        return {
            "number": ruku_number,
            "ayahs": ayahs,
            "surahs": surahs,
            "edition": edition_info
        }

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An unexpected error occurred, please try again later."
