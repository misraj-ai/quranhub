from sqlalchemy.future import select
from utils.logger import logger
from utils.config import DEFAULT_EDITION_IDENTIFIER
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from db.models import Ayat, Surat
from db.session import AsyncSessionLocal
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls

async def get_quran(edition_identifier):
    try:
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # Error fetching edition
            return edition
        elif isinstance(edition, list):
            # Select the appropriate edition based on type
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]

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

        surahs = []
        
        async with AsyncSessionLocal() as session:
            for i in range(1, 115):
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
                        Surat.id == i,
                        Ayat.edition_id == edition_id
                    ).order_by(Ayat.number)
                )

                result = result.fetchall()

                if not result:
                    continue  # Skip Surah if no ayah data is found
                
                ayahs = []
                for item in result:
                    ayah = {
                        "number": item.number,
                        "text": item.text,
                        "numberInSurah": item.numberinsurat,
                        "juz": item.juz_id,
                        "manzil": item.manzil_id,
                        "page": item.page_id,
                        "ruku": item.ruku_id,
                        "hizbQuarter": item.hizbquarter_id,
                        "sajda": item.sajda_id if item.sajda_id else False
                    }
                    ayahs.append(ayah)

                if edition.format == "audio":
                    bitrates = edition.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    for item in ayahs:
                        item["audio"] =  get_ayah_audio_url(max_bitrate, edition.identifier, item["number"])
                        item["audioSecondary"] =  get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, item["number"])

                surahs.append({
                    "number": result[0].id,
                    "name": result[0].name,
                    "englishName": result[0].englishname,
                    "englishNameTranslation": result[0].englishtranslation,
                    "revelationType": result[0].revelationcity,
                    "numberOfAyahs": result[0].numberofayats,
                    "ayahs": ayahs
                })

        edition_data = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name,
            "englishName": edition.englishname,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        return {"surahs": surahs, "edition": edition_data}

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching Quran data."
