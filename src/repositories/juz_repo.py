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

async def get_all_juzs(edition_identifier=DEFAULT_EDITION_IDENTIFIER, include_hizbs: bool = False):
    try:
        # Resolve edition (and map audio → text edition id if needed)
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # error string
            return edition
        elif isinstance(edition, list):
            # Select the versebyverse/text edition from your pair
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]

        edition_id = edition.id
        if edition.format == "audio":
            text_edition = await get_text_edition_for_narrator(edition.identifier)
            if isinstance(text_edition, str):
                return text_edition
            edition_id = text_edition.id

        juzs_info = []

        async with AsyncSessionLocal() as session:
            # We need hizbquarter_id (and page_id) to build hizbs/halves when requested.
            result = await session.execute(
                select(
                    Ayat.juz_id,
                    Ayat.number,            # global ayah number (used to order quarter starts)
                    Ayat.text,
                    Ayat.numberinsurat,
                    Ayat.page_id,
                    Ayat.hizbquarter_id,    # used to detect quarter starts per Juz
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.revelationcity,
                    Surat.numberofayats
                ).join(Surat, Ayat.surat_id == Surat.id)
                 .filter(Ayat.edition_id == edition_id)
                 .order_by(Ayat.juz_id, Ayat.number)
            )

            fetched_rows = result.fetchall()

            if not fetched_rows:
                return "No Juzs found."

            # Build the base Juz metadata and (optionally) collect first-ayah per hizbquarter within each Juz
            juz_data_map = {}         # {juz_id: { base metadata ... }}
            # {juz_id: {quarter_id: { "_firstAyahNumber": int, "firstPage": int, "firstAyah": {...}, "firstSurah": {...} }}}
            first_quarter_starts = {}

            for row in fetched_rows:
                juz_id = row.juz_id

                # Initialize base Juz metadata on first encounter of this juz_id
                if juz_id not in juz_data_map:
                    juz_data_map[juz_id] = {
                        "number": juz_id,
                        "firstPage": row.page_id,
                        "firstAyah": {
                            "number": row.number,
                            "text": row.text,
                            "numberInSurah": row.numberinsurat,
                        },
                        "firstSurah": {
                            "number": row.id,
                            "name": row.name,
                            "englishName": row.englishname,
                            "englishNameTranslation": row.englishtranslation,
                            "revelationType": row.revelationcity,
                            "numberOfAyahs": row.numberofayats
                        }
                    }

                if include_hizbs:
                    qmap = first_quarter_starts.setdefault(juz_id, {})
                    qid = row.hizbquarter_id
                    # Save the *first* occurrence (lowest ayah number) of this quarter within the current Juz
                    # This guarantees we pick the correct "start" for each quarter in this Juz.
                    if qid is not None and qid not in qmap:
                        qmap[qid] = {
                            "_firstAyahNumber": row.number,  # for reliable ordering
                            "firstPage": row.page_id,        # <-- include firstPage per quarter
                            "firstAyah": {
                                "number": row.number,
                                "numberInSurah": row.numberinsurat,
                                "text": row.text
                            },
                            "firstSurah": {
                                "number": row.id,
                                "name": row.name,
                                "englishName": row.englishname
                            }
                        }

            # Convert to list while preserving natural Juz order
            juzs_info = list(juz_data_map.values())

        # If requested, compute hizbs (2 per Juz) from the first 4 quarters we observe in that Juz
        if include_hizbs:
            for juz in juzs_info:
                juz_id = juz["number"]
                qmap = first_quarter_starts.get(juz_id, {})

                # Order the quarters for this Juz by the first ayah's global number to ensure correct sequence
                ordered_quarters = sorted(
                    qmap.values(),
                    key=lambda d: d["_firstAyahNumber"]
                )

                # Expect 4 quarters per Juz. If data anomalies produce more, take the first 4.
                # If fewer are present, degrade gracefully.
                ordered_quarters = ordered_quarters[:4]

                hizbs = []
                if len(ordered_quarters) >= 2:
                    q1, q2 = ordered_quarters[0], ordered_quarters[1]
                    hizbs.append({
                        "number": 1,
                        "halves": [
                            {
                                "number": 1,
                                "firstPage": q1["firstPage"],              # <-- added
                                "firstSurah": q1["firstSurah"],
                                "firstAyah": q1["firstAyah"]
                            },
                            {
                                "number": 2,
                                "firstPage": q2["firstPage"],              # <-- added
                                "firstSurah": q2["firstSurah"],
                                "firstAyah": q2["firstAyah"]
                            },
                        ]
                    })
                if len(ordered_quarters) >= 4:
                    q3, q4 = ordered_quarters[2], ordered_quarters[3]
                    hizbs.append({
                        "number": 2,
                        "halves": [
                            {
                                "number": 1,
                                "firstPage": q3["firstPage"],              # <-- added
                                "firstSurah": q3["firstSurah"],
                                "firstAyah": q3["firstAyah"]
                            },
                            {
                                "number": 2,
                                "firstPage": q4["firstPage"],              # <-- added
                                "firstSurah": q4["firstSurah"],
                                "firstAyah": q4["firstAyah"]
                            },
                        ]
                    })

                if hizbs:
                    juz["hizbs"] = hizbs

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