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
            edition = edition[0] if edition[0].type == "versebyverse" else edition[1]

        edition_id = edition.id
        if edition.format == "audio":
            text_edition = await get_text_edition_for_narrator(edition.identifier)
            if isinstance(text_edition, str):
                return text_edition
            edition_id = text_edition.id

        juzs_info = []

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    Ayat.juz_id,
                    Ayat.hizb_id,           # Use hizb_id directly!
                    Ayat.hizbquarter_id,
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
                ).join(Surat, Ayat.surat_id == Surat.id)
                 .filter(Ayat.edition_id == edition_id)
                 .order_by(Ayat.juz_id, Ayat.number)
            )

            fetched_rows = result.fetchall()

            if not fetched_rows:
                return "No Juzs found."

            juz_data_map = {}
            # {juz_id: {hizb_id: {"_firstAyahNumber": int, ...}}}
            first_hizb_starts = {}
            # {juz_id: {hizbquarter_id: {"_firstAyahNumber": int, ...}}}
            first_quarter_starts = {}

            for row in fetched_rows:
                juz_id = row.juz_id

                # Initialize base Juz metadata on first encounter
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
                    # Track first ayah of each HIZB within this juz
                    hizb_map = first_hizb_starts.setdefault(juz_id, {})
                    hizb_id = row.hizb_id
                    if hizb_id is not None and hizb_id not in hizb_map:
                        hizb_map[hizb_id] = {
                            "_firstAyahNumber": row.number,
                            "_hizb_id": hizb_id,
                            "firstPage": row.page_id,
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

                    # Track first ayah of each QUARTER within this juz (for halves)
                    quarter_map = first_quarter_starts.setdefault(juz_id, {})
                    quarter_id = row.hizbquarter_id
                    if quarter_id is not None and quarter_id not in quarter_map:
                        quarter_map[quarter_id] = {
                            "_firstAyahNumber": row.number,
                            "_quarter_id": quarter_id,
                            "_hizb_id": hizb_id,  # Track which hizb this quarter belongs to
                            "firstPage": row.page_id,
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

            juzs_info = list(juz_data_map.values())

        # Build hizbs structure: 2 hizbs per juz, each with 2 halves (4 quarters total per juz = 8 quarter-starts)
        if include_hizbs:
            for juz in juzs_info:
                juz_id = juz["number"]
                hizb_map = first_hizb_starts.get(juz_id, {})
                quarter_map = first_quarter_starts.get(juz_id, {})

                # Get the 2 hizbs for this juz, ordered by hizb_id
                ordered_hizbs = sorted(
                    hizb_map.values(),
                    key=lambda d: d["_hizb_id"]
                )[:2]  # Should be exactly 2 hizbs per juz

                # Get all quarters for this juz, ordered
                ordered_quarters = sorted(
                    quarter_map.values(),
                    key=lambda d: d["_quarter_id"]
                )

                # Group quarters by their hizb_id
                quarters_by_hizb = {}
                for q in ordered_quarters:
                    h_id = q["_hizb_id"]
                    if h_id not in quarters_by_hizb:
                        quarters_by_hizb[h_id] = []
                    quarters_by_hizb[h_id].append(q)

                hizbs = []
                for idx, hizb_data in enumerate(ordered_hizbs, start=1):
                    hizb_id = hizb_data["_hizb_id"]
                    hizb_quarters = quarters_by_hizb.get(hizb_id, [])

                    # Each hizb has 4 quarters; we create 2 halves (quarters 1-2 and 3-4)
                    halves = []
                    if len(hizb_quarters) >= 1:
                        halves.append({
                            "number": 1,
                            "firstPage": hizb_quarters[0]["firstPage"],
                            "firstSurah": hizb_quarters[0]["firstSurah"],
                            "firstAyah": hizb_quarters[0]["firstAyah"]
                        })
                    if len(hizb_quarters) >= 3:
                        # Second half starts at quarter 3
                        halves.append({
                            "number": 2,
                            "firstPage": hizb_quarters[2]["firstPage"],
                            "firstSurah": hizb_quarters[2]["firstSurah"],
                            "firstAyah": hizb_quarters[2]["firstAyah"]
                        })

                    hizbs.append({
                        "number": idx,  # 1 or 2 within this juz
                        "hizbNumber": hizb_id,  # Global hizb number (1-60)
                        "firstPage": hizb_data["firstPage"],
                        "firstSurah": hizb_data["firstSurah"],
                        "firstAyah": hizb_data["firstAyah"],
                        "halves": halves
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