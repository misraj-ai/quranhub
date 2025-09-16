from sqlalchemy.future import select
from db.models import Ayat, Surat
from db.session import AsyncSessionLocal
from utils.logger import logger
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls

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
            text_edition = await get_text_edition_for_narrator(edition.identifier)
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
                "name": edition.name,
                "englishName": edition.englishname,
                "format": edition.format,
                "type": edition.type,
                "direction": edition.direction
            },
            "surah": {
                "number": result.id,
                "name": result.name,
                "englishName": result.englishname,
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

        # If the edition is audio, add the audio details
        if edition.format == "audio":
            bitrates = edition.bitrates
            max_bitrate = max(bitrates)
            remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
            ayah["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, ayah["number"])
            ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, ayah["number"])

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
                    text_edition = await get_text_edition_for_narrator(item.identifier)
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
                    "name": editions[i].name,
                    "englishName": editions[i].englishname,
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

            edition_format = ayah['edition']['format']
            if edition_format == "audio":
                # Find the edition with the correct identifier
                edition = next((item for item in editions if item.identifier == ayah['edition']['identifier']), None)
                if edition:
                    bitrates = edition.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    ayah["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, ayah["number"])
                    ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, ayah["number"])

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
            text_edition = await get_text_edition_for_narrator(edition.identifier)
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
                "name": edition.name,
                "englishName": edition.englishname,
                "format": edition.format,
                "type": edition.type,
                "direction": edition.direction
            },
            "surah": {
                "number": result.id,
                "name": result.name,
                "englishName": result.englishname,
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

        # If the format is audio, add the audio URLs
        if edition.format == "audio":
            bitrates = edition.bitrates
            max_bitrate = max(bitrates)
            remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
            ayah["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, ayah["number"])
            ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, ayah["number"])

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
                    text_edition = await get_text_edition_for_narrator(edition.identifier)
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
                    "name": editions[i].name,
                    "englishName": editions[i].englishname,
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

            # If the format is audio, add the audio URLs
            edition_format = ayah['edition']['format']
            if edition_format == "audio":
                for item in editions:
                    if item.identifier == ayah['edition']['identifier']:
                        edition = item
                        break
                bitrates = edition.bitrates
                max_bitrate = max(bitrates)
                remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                ayah["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, ayah["number"])
                ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, ayah["number"])

            data.append(ayah)

        return data

    except Exception as e:
        logger.error("An exception occurred while fetching Ayah by Surah number and multiple editions: %s", str(e))
        return "An error occurred while fetching this Ayah."