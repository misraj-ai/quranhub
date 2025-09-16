from sqlalchemy.future import select
from db.session import AsyncSessionLocal  # Assuming AsyncSessionLocal is defined for async sessions
from utils.logger import logger
from db.models import Ayat, Surat, Sajda  # Assuming these are imported correctly
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls

async def get_sajdas(edition_identifier: str):
    try:
        # Retrieve edition asynchronously
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):
            return edition
        elif isinstance(edition, list):
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

        async with AsyncSessionLocal() as session:
            # Subquery to get relevant ayat details
            subquery = (
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
                .filter(Ayat.edition_id == edition_id, Ayat.sajda_id.isnot(None))
                .subquery()
            )

            # Final query joining the Sajda table
            final_query = (
                select(
                    subquery.c.number,
                    subquery.c.text,
                    subquery.c.numberinsurat,
                    subquery.c.juz_id,
                    subquery.c.manzil_id,
                    subquery.c.page_id,
                    subquery.c.ruku_id,
                    subquery.c.hizbquarter_id,
                    subquery.c.sajda_id,
                    subquery.c.id,
                    subquery.c.name,
                    subquery.c.englishname,
                    subquery.c.englishtranslation,
                    subquery.c.revelationcity,
                    subquery.c.numberofayats,
                    Sajda.recommended,
                    Sajda.obligatory
                )
                .join(Sajda, subquery.c.sajda_id == Sajda.id)
            )

            # Execute query asynchronously
            results = await session.execute(final_query)
            results = results.all()

        ayahs = []
        for item in results:
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
                "sajda": {
                    "id": item.sajda_id,
                    "recommended": True if item.recommended == 1 else False,
                    "obligatory": True if item.obligatory == 1 else False
                }
            })

        # Handle audio edition if applicable
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

        return {"ayahs": ayahs, "edition": edition_info}

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching Sajdas."
