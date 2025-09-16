from sqlalchemy.future import select
from sqlalchemy import func, literal_column, and_
from sqlalchemy.orm import aliased
from db.models import Surat, Ayat
from db.session import AsyncSessionLocal
from utils.logger import logger
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls, get_surah_audio_url, get_surah_audio_secondary_urls

async def get_all_surahs(order_by_revelation_order=False):
    try:
        edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
        edition_id = edition.id

        surahs = []

        # Use async session
        async with AsyncSessionLocal() as session:
            # Build the query
            query = select(
                Surat.id,
                Surat.name,
                Surat.englishname,
                Surat.englishtranslation,
                Surat.numberofayats,
                Surat.revelationcity,
                Surat.revelation_order,
                func.min(literal_column("CASE WHEN ayat.numberinsurat = 1 THEN ayat.page_id END")).label('startingPage'),
                func.max(literal_column("CASE WHEN ayat.numberinsurat = ayat.numberinsurat THEN ayat.page_id END")).label('endingPage')
            ).outerjoin(Ayat, and_(Ayat.surat_id == Surat.id, Ayat.edition_id == edition_id)) \
            .group_by(Surat.id)

            # Apply ordering based on the flag
            if order_by_revelation_order:
                query = query.order_by(Surat.revelation_order)
            else:
                query = query.order_by(Surat.id)

            # Execute query and fetch the results asynchronously
            result = await session.execute(query)
            results = result.fetchall()

        # Process the results into the required format
        for item in results:
            surahs.append({
                "number": item.id,
                "startingPage": item.startingPage,
                "endingPage": item.endingPage,
                "name": item.name,
                "englishName": item.englishname,
                "englishNameTranslation": item.englishtranslation,
                "revelationType": item.revelationcity,
                "numberOfAyahs": item.numberofayats,
                "revelationOrder": item.revelation_order
            })
        return surahs
    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching surahs."



async def get_all_revelation_cities_with_surahs():
    try:
        # Fetch the edition asynchronously
        edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
        if isinstance(edition, str):  # Error occurred while fetching edition
            return edition

        edition_id = edition.id
        city_map = {}

        # Query for Surahs with associated revelation city details
        async with AsyncSessionLocal() as session:
            # Create aliased objects for complex join operations if needed
            ayat_alias = aliased(Ayat)

            # Perform the SQL query
            query = select(
                Surat.revelationcity,
                Surat.id,
                Surat.name,
                Surat.englishname,
                Surat.englishtranslation,
                Surat.numberofayats,
                func.min(ayat_alias.page_id).label('startingPage'),
                func.max(ayat_alias.page_id).label('endingPage')
            ).outerjoin(
                ayat_alias, and_(ayat_alias.surat_id == Surat.id, ayat_alias.edition_id == edition_id)
            ).group_by(
                Surat.revelationcity,
                Surat.id,
                Surat.name,
                Surat.englishname,
                Surat.englishtranslation,
                Surat.numberofayats
            ).order_by(
                Surat.revelationcity,
                Surat.id
            )

            result = await session.execute(query)
            results = result.fetchall()  # Fetch all results from query

            # Populate the city_map with surah data by revelation city
            for city, surah_id, name, en_name, en_translation, num_ayahs, starting_page, ending_page in results:
                if city not in city_map:
                    city_map[city] = {
                        "revelationCity": city,
                        "surahs": []
                    }
                city_map[city]["surahs"].append({
                    "number": surah_id,
                    "name": name,
                    "englishName": en_name,
                    "englishNameTranslation": en_translation,
                    "numberOfAyahs": num_ayahs,
                    "revelationType": city,
                    "startingPage": starting_page,
                    "endingPage": ending_page
                })

        return list(city_map.values())

    except Exception as e:
        logger.error("An error occurred while fetching Surahs by Revelation City: %s", str(e))
        return "An error occurred while fetching Surahs by Revelation City."



async def get_all_juzs_with_surahs():
    try:
        # Fetch the edition asynchronously
        edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
        if isinstance(edition, str):  # Error occurred while fetching edition
            return edition

        edition_id = edition.id
        juz_map = {}

        # Query for Surahs grouped by Juz
        async with AsyncSessionLocal() as session:
            # Perform the SQL query to get Surah data grouped by Juz
            query = select(
                Ayat.juz_id,
                Surat.id,
                Surat.name,
                Surat.englishname,
                Surat.englishtranslation,
                Surat.numberofayats,
                Surat.revelationcity,
                func.min(Ayat.page_id).label('startingPage'),
                func.max(Ayat.page_id).label('endingPage')
            ).join(
                Surat, Surat.id == Ayat.surat_id
            ).filter(
                Ayat.edition_id == edition_id,
                Ayat.juz_id != None
            ).group_by(
                Ayat.juz_id,
                Surat.id,
                Surat.name,
                Surat.englishname,
                Surat.englishtranslation,
                Surat.numberofayats,
                Surat.revelationcity
            ).order_by(
                Ayat.juz_id,
                Surat.id
            )

            result = await session.execute(query)
            results = result.fetchall()  # Fetch all results

            # Populate the juz_map with Surah data for each Juz
            for juz_id, surah_id, name, en_name, en_translation, num_ayahs, city, starting_page, ending_page in results:
                if juz_id not in juz_map:
                    juz_map[juz_id] = {
                        "juzNumber": juz_id,
                        "surahs": []
                    }
                juz_map[juz_id]["surahs"].append({
                    "number": surah_id,
                    "name": name,
                    "englishName": en_name,
                    "englishNameTranslation": en_translation,
                    "numberOfAyahs": num_ayahs,
                    "revelationType": city,
                    "startingPage": starting_page,
                    "endingPage": ending_page
                })

        # Return the list of Juzs with Surahs
        return list(juz_map.values())


    except Exception as e:
        logger.error("An error occurred while fetching Juzs with Surahs: %s", str(e))
        return "An error occurred while fetching Juzs with Surahs."



async def get_surah(surah_number, edition_identifier, limit, offset):
    try:
        # Fetch the edition based on the provided identifier
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # Error occurred while fetching edition
            return edition

        # If edition is a list, we use the default edition for text
        if isinstance(edition, list):
            # For audio editions list, get text edition using narrator_identifier
            audio_edition = next((e for e in edition if e.format == "audio"), None)
            if audio_edition and audio_edition.narrator_identifier:
                text_edition = await get_text_edition_for_narrator(audio_edition.narrator_identifier)
            else:
                text_edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
            
            if isinstance(text_edition, str):
                return text_edition
            edition_id = text_edition.id
        else:
            edition_id = edition.id
            # If the edition is audio, get text edition for the same narrator
            if edition.format == "audio" and edition.narrator_identifier:
                text_edition = await get_text_edition_for_narrator(edition.narrator_identifier)
                if isinstance(text_edition, str):
                    return text_edition
                edition_id = text_edition.id
            elif edition.format == "audio":
                # Fallback to default if no narrator_identifier
                text_edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
                if isinstance(text_edition, str):
                    return text_edition
                edition_id = text_edition.id

        # Query Surah metadata
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.numberofayats,
                    Surat.revelationcity
                ).filter(Surat.id == surah_number)
            )
            surah_meta = result.fetchone()
            if not surah_meta:
                return "Surah not found."

            # Query Ayah data for the Surah
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
                    Ayat.sajda_id
                ).join(Surat, Ayat.surat_id == Surat.id).filter(
                    Ayat.surat_id == surah_number,
                    Ayat.edition_id == edition_id
                ).order_by(Ayat.number).limit(limit).offset(offset)
            )
            ayahs = []
            for item in result.fetchall():
                ayahs.append({
                    "number": item.number,
                    "text": item.text,
                    "numberInSurah": item.numberinsurat,
                    "juz": item.juz_id,
                    "manzil": item.manzil_id,
                    "page": item.page_id,
                    "ruku": item.ruku_id,
                    "hizbQuarter": item.hizbquarter_id,
                    "sajda": item.sajda_id if item.sajda_id else False
                })

        # Audio URLs for Surah and Ayahs
        surah_audio_url = ""
        surah_audio_secondary_urls = []

        if isinstance(edition, list):
            for item in edition:
                if item.type == "versebyverse":
                    bitrates = item.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    for ayah in ayahs:
                        ayah["audio"] =  get_ayah_audio_url(max_bitrate, item.identifier, ayah["number"])
                        ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, item.identifier, ayah["number"])
                elif item.type == "surah":
                    bitrates = item.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    surah_audio_url = get_surah_audio_url(max_bitrate, item.identifier, surah_number)
                    surah_audio_secondary_urls = get_surah_audio_secondary_urls(remaining_bitrates, item.identifier, surah_number)
            edition = edition[0]  # Use the first edition for other details
        else:
            if edition.format == "audio":
                if edition.type == "versebyverse":
                    bitrates = edition.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    for ayah in ayahs:
                        ayah["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, ayah["number"])
                        ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, ayah["number"])
                elif edition.type == "surah":
                    bitrates = edition.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    surah_audio_url = get_surah_audio_url(max_bitrate, edition.identifier, surah_number)
                    surah_audio_secondary_urls = get_surah_audio_secondary_urls(remaining_bitrates, edition.identifier, surah_number)

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
            "number": surah_meta.id,
            "name": surah_meta.name,
            "audio": surah_audio_url,
            "audioSecondary": surah_audio_secondary_urls,
            "englishName": surah_meta.englishname,
            "englishNameTranslation": surah_meta.englishtranslation,
            "revelationType": surah_meta.revelationcity,
            "numberOfAyahs": surah_meta.numberofayats,
            "ayahs": ayahs,
            "edition": edition_data
        }

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching the Surah data."

async def get_surah_by_multiple_editions(surah_number, edition_identifiers, limit, offset):
    try:
        editions = []
        for edition_identifier in edition_identifiers:
            result = await get_edition_by_identifier(edition_identifier)
            if isinstance(result, str):  # Error fetching edition
                return result
            elif isinstance(result, list):
                # Select the appropriate edition based on type
                if result[0].type == "versebyverse":
                    result = result[0]
                else:
                    result = result[1]
            editions.append(result)

        results = []
        data = []

        # Query Surah metadata asynchronously
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.numberofayats,
                    Surat.revelationcity
                ).filter(Surat.id == surah_number)
            )
            surah_meta = result.fetchone()
            if not surah_meta:
                return "Surah not found."

            # For each edition, get the Ayahs and process audio URLs
            for item in editions:
                edition_id = item.id
                if item.format == "audio":
                    # Get text edition for the same narrator_identifier
                    if item.narrator_identifier:
                        text_edition = await get_text_edition_for_narrator(item.narrator_identifier)
                    else:
                        text_edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
                    
                    if isinstance(text_edition, str):
                        return text_edition
                    edition_id = text_edition.id

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
                        Ayat.sajda_id
                    ).join(Surat, Ayat.surat_id == Surat.id).filter(
                        Ayat.surat_id == surah_number,
                        Ayat.edition_id == edition_id
                    ).order_by(Ayat.number).limit(limit).offset(offset)
                )
                fetched_results = result.fetchall()
                if not fetched_results:  # Changed to fetchall() to check for empty results
                    return "Ayahs not found."
                results.append(fetched_results)

        # Process each edition and generate the data with audio URLs
        for i in range(len(editions)):
            ayahs = []
            for j in range(len(results[i])):
                ayah = {
                    "number": results[i][j].number,
                    "text": results[i][j].text,
                    "numberInSurah": results[i][j].numberinsurat,
                    "juz": results[i][j].juz_id,
                    "manzil": results[i][j].manzil_id,
                    "page": results[i][j].page_id,
                    "ruku": results[i][j].ruku_id,
                    "hizbQuarter": results[i][j].hizbquarter_id,
                    "sajda": results[i][j].sajda_id if results[i][j].sajda_id else False
                }
                ayahs.append(ayah)

            # If edition format is audio, add audio URLs for the Ayahs
            if editions[i].format == "audio":
                bitrates = editions[i].bitrates
                max_bitrate = max(bitrates)
                remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                for item in ayahs:
                    item["audio"] = get_ayah_audio_url(max_bitrate, editions[i].identifier, item["number"])
                    item["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, editions[i].identifier, item["number"])

            edition_data = {
                "identifier": editions[i].identifier,
                "language": editions[i].language,
                "name": editions[i].name,
                "englishName": editions[i].englishname,
                "format": editions[i].format,
                "type": editions[i].type,
                "direction": editions[i].direction
            }

            # Add the final data for the edition
            data.append({
                "number": surah_meta.id,
                "name": surah_meta.name,
                "englishName": surah_meta.englishname,
                "englishNameTranslation": surah_meta.englishtranslation,
                "revelationType": surah_meta.revelationcity,
                "numberOfAyahs": surah_meta.numberofayats,
                "ayahs": ayahs,
                "edition": edition_data
            })

        return data

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching the Surah data."