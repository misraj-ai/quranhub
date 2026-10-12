from sqlalchemy.future import select
from db.models import Ayat, Surat
from db.session import AsyncSessionLocal
from utils.logger import logger
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import add_ayah_audio


async def _text_edition_for_audio(edition):
    """Text edition whose ayat back an audio edition: the narrator's text (e.g. quran-warsh), else the default.

    The audio identifier itself (e.g. ar.abdulsamad.warsh) never matches a text edition, so it
    must not be used for this lookup: it silently fell back to quran-simple, which has Hafs
    numbering, and pointed non-Hafs reciters at the wrong audio file.
    """
    if edition.narrator_identifier:
        return await get_text_edition_for_narrator(edition.narrator_identifier)
    return await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)


async def get_an_ayah(ayah_number: int, edition_identifier: str):
    try:
        # Fetch the edition asynchronously
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # If it's an error message
            return edition
        elif isinstance(edition, list):
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]

        edition_id = edition.id
        if edition.format == "audio":
            # Fetch text edition for narrator-specific audio
            text_edition = await _text_edition_for_audio(edition)
            if isinstance(text_edition, str):  # If it's an error message
                return text_edition
            edition_id = text_edition.id

        # Query the Ayah and Surah details asynchronously
        async with AsyncSessionLocal() as session:
            query = select(
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
                Ayat.number == ayah_number,
                Ayat.edition_id == edition_id
            )
            result = await session.execute(query)
            result = result.first()  # Fetch the first result

        if not result:
            return "Ayah not found."

        # Construct the response
        ayah = {
            "number": result.number,
            "text": result.text,
            "edition": {
                "identifier": edition.identifier,
                "language": edition.language,
                "name": edition.name.get("ar") if isinstance(edition.name, dict) else None,
                "englishName": edition.name.get("en") if isinstance(edition.name, dict) else None,
                "format": edition.format,
                "type": edition.type,
                "direction": edition.direction
            },
            "surah": {
                "number": result.id,
                "name": result.name.get("ar") if isinstance(result.name, dict) else None,
                "englishName": result.name.get("en") if isinstance(result.name, dict) else None,
                "englishNameTranslation": result.englishtranslation,
                "revelationType": result.revelationcity,
                "numberOfAyahs": result.numberofayats
            },
            "numberInSurah": result.numberinsurat,
            "juz": result.juz_id,
            "manzil": result.manzil_id,
            "page": result.page_id,
            "ruku": result.ruku_id,
            "hizbQuarter": result.hizbquarter_id,
            "sajda": result.sajda_id if result.sajda_id else False
        }

        # Per-ayah audio URLs exist only for verse-by-verse editions
        add_ayah_audio(ayah, edition, ayah["number"])

        return ayah

    except Exception as e:
        logger.error("An exception occurred while fetching Ayah: %s", str(e))
        return "An error occurred while fetching this Ayah."



async def get_an_ayah_by_multiple_editions(ayah_number: int, edition_identifiers: list):
    try:
        # Fetch editions asynchronously
        editions = []
        for item in edition_identifiers:
            edition = await get_edition_by_identifier(item)
            if isinstance(edition, str):  # If it's an error message
                return edition
            elif isinstance(edition, list):
                edition = edition[0] if edition[0].type == "versebyverse" else edition[1]
            editions.append(edition)

        data = []
        results = []

        # Query Ayah and Surah details for each edition asynchronously
        async with AsyncSessionLocal() as session:
            for item in editions:
                edition_id = item.id
                if item.format == "audio":
                    text_edition = await _text_edition_for_audio(item)
                    if isinstance(text_edition, str):  # If it's an error message
                        return text_edition
                    edition_id = text_edition.id

                query = select(
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
                    Ayat.number == ayah_number,
                    Ayat.edition_id == edition_id
                )
                result = await session.execute(query)
                result = result.first()  # Fetch the first result
                results.append(result)

        for i in range(len(results)):
            ayah = {
                "number": results[i].number,
                "text": results[i].text,
                "edition": {
                    "identifier": editions[i].identifier,
                    "language": editions[i].language,
                    "name": editions[i].name.get("ar") if isinstance(editions[i].name, dict) else None,
                    "englishName": editions[i].name.get("en") if isinstance(editions[i].name, dict) else None,
                    "format": editions[i].format,
                    "type": editions[i].type,
                    "direction": editions[i].direction
                },
                "surah": {
                    "number": results[i].id,
                    "name": results[i].name,
                    "englishName": results[i].englishname,
                    "englishNameTranslation": results[i].englishtranslation,
                    "revelationType": results[i].revelationcity,
                    "numberOfAyahs": results[i].numberofayats
                },
                "numberInSurah": results[i].numberinsurat,
                "juz": results[i].juz_id,
                "manzil": results[i].manzil_id,
                "page": results[i].page_id,
                "ruku": results[i].ruku_id,
                "hizbQuarter": results[i].hizbquarter_id,
                "sajda": results[i].sajda_id if results[i].sajda_id else False
            }

            add_ayah_audio(ayah, editions[i], ayah["number"])

            data.append(ayah)

        return data

    except Exception as e:
        logger.error("An exception occurred while fetching Ayah: %s", str(e))
        return "An error occurred while fetching this Ayah."


async def get_an_ayah_by_surah_number(surah_number: int, ayah_number: int, edition_identifier: str):
    try:
        # Fetch edition asynchronously
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # Error occurred while fetching edition
            return edition
        elif isinstance(edition, list):
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]
        
        edition_id = edition.id
        
        # If the format is audio, use the narrator-specific text edition
        if edition.format == "audio":
            text_edition = await _text_edition_for_audio(edition)
            if isinstance(text_edition, str):  # Error occurred while fetching text edition
                return text_edition
            edition_id = text_edition.id
        
        # Query Ayah and Surah details asynchronously
        async with AsyncSessionLocal() as session:
            query = select(
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
                Ayat.numberinsurat == ayah_number,
                Ayat.surat_id == surah_number,
                Ayat.edition_id == edition_id
            )
            result = await session.execute(query)
            result = result.first()  # Fetch the first result
            
            if not result:
                return "Ayah not found."
        
        # Construct the response data
        ayah = {
            "number": result.number,
            "text": result.text,
            "edition": {
                "identifier": edition.identifier,
                "language": edition.language,
                "name": edition.name.get("ar") if isinstance(edition.name, dict) else None,
                "englishName": edition.name.get("en") if isinstance(edition.name, dict) else None,
                "format": edition.format,
                "type": edition.type,
                "direction": edition.direction
            },
            "surah": {
                "number": result.id,
                "name": result.name.get("ar") if isinstance(result.name, dict) else None,
                "englishName": result.name.get("en") if isinstance(result.name, dict) else None,
                "englishNameTranslation": result.englishtranslation,
                "revelationType": result.revelationcity,
                "numberOfAyahs": result.numberofayats
            },
            "numberInSurah": result.numberinsurat,
            "juz": result.juz_id,
            "manzil": result.manzil_id,
            "page": result.page_id,
            "ruku": result.ruku_id,
            "hizbQuarter": result.hizbquarter_id,
            "sajda": result.sajda_id if result.sajda_id else False
        }

        add_ayah_audio(ayah, edition, ayah["number"])

        return ayah

    except Exception as e:
        logger.error("An exception occurred while fetching Ayah by Surah number: %s", str(e))
        return "An error occurred while fetching this Ayah."



async def get_an_ayah_by_surah_number_and_multiple_editions(surah_number: int, ayah_number: int, edition_identifiers: list):
    try:
        editions = []
        # Fetch editions asynchronously
        for item in edition_identifiers:
            edition = await get_edition_by_identifier(item)
            if isinstance(edition, str):  # Error occurred while fetching edition
                return edition
            elif isinstance(edition, list):
                edition = edition[0] if edition[0].type == "versebyverse" else edition[1]
            editions.append(edition)

        data = []
        results = []

        # Query for each edition asynchronously
        async with AsyncSessionLocal() as session:
            for edition in editions:
                edition_id = edition.id
                if edition.format == "audio":
                    text_edition = await _text_edition_for_audio(edition)
                    if isinstance(text_edition, str):  # Error occurred while fetching text edition
                        return text_edition
                    edition_id = text_edition.id

                query = select(
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
                    Ayat.numberinsurat == ayah_number,
                    Ayat.surat_id == surah_number,
                    Ayat.edition_id == edition_id
                )
                result = await session.execute(query)
                result = result.first()  # Fetch the first result
                
                if not result:
                    return "Ayah not found."
                results.append(result)

        # Construct the response data
        for i in range(len(results)):
            ayah = {
                "number": results[i].number,
                "text": results[i].text,
                "edition": {
                    "identifier": editions[i].identifier,
                    "language": editions[i].language,
                    "name": editions[i].name.get("ar") if isinstance(editions[i].name, dict) else None,
                    "englishName": editions[i].name.get("en") if isinstance(editions[i].name, dict) else None,
                    "format": editions[i].format,
                    "type": editions[i].type,
                    "direction": editions[i].direction
                },
                "surah": {
                    "number": results[i].id,
                    "name": results[i].name,
                    "englishName": results[i].englishname,
                    "englishNameTranslation": results[i].englishtranslation,
                    "revelationType": results[i].revelationcity,
                    "numberOfAyahs": results[i].numberofayats
                },
                "numberInSurah": results[i].numberinsurat,
                "juz": results[i].juz_id,
                "manzil": results[i].manzil_id,
                "page": results[i].page_id,
                "ruku": results[i].ruku_id,
                "hizbQuarter": results[i].hizbquarter_id,
                "sajda": results[i].sajda_id if results[i].sajda_id else False
            }

            add_ayah_audio(ayah, editions[i], ayah["number"])

            data.append(ayah)

        return data

    except Exception as e:
        logger.error("An exception occurred while fetching Ayah by Surah number and multiple editions: %s", str(e))
        return "An error occurred while fetching this Ayah."