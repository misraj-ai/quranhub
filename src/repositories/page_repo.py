from sqlalchemy.future import select
from sqlalchemy import tuple_
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls
from db.models import Ayat, Surat
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from repositories.hizb_repo import get_hizb_numbers
from repositories.word_repo import get_words, SPECIAL_NARRATION_PAGE_SPLITS
from repositories.mushaf_layout_repo import get_layout_by_code, get_page_ayahs_and_lines
from utils.logger import logger
from db.session import AsyncSessionLocal
from utils.config import DEFAULT_EDITION_IDENTIFIER

async def get_page(page_number: int, edition_identifier: str, words: bool, limit: int, offset: int, tajweed: bool = False, tajweed_level: str = "basic", layout_code: str = None):
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
                if isinstance(text_edition, str):
                    return text_edition
                edition_id = text_edition.id
                edition_identifier = text_edition.identifier
            else:
                text_edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
                if isinstance(text_edition, str):
                    return text_edition
                edition_id = text_edition.id
                edition_identifier = text_edition.identifier

        if words and (edition.language != "ar" or edition.type == "tafsir"):
            return "Words are not available for this edition. Words are available only for Arabic editions and not Tafsir editions."

        layout_id = None
        line_map = None
        layout_ayahs = None

        if layout_code:
            layout = await get_layout_by_code(layout_code)
            if not layout:
                return f"Layout with code '{layout_code}' not found."
            layout_id = layout.layout_id
            layout_ayahs, line_map = await get_page_ayahs_and_lines(layout_id, page_number)
            if not layout_ayahs:
                return f"No data found for layout '{layout_code}' page {page_number}."

        async with AsyncSessionLocal() as session:
            stmt = (
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
                .filter(Ayat.edition_id == edition_id)
            )

            if layout_ayahs is not None:
                # Create a mapping for sorting: (surat_id, numberinsurat) -> index
                order_map = {(s, a): i for i, (s, a) in enumerate(layout_ayahs)}
                stmt = stmt.filter(tuple_(Ayat.surat_id, Ayat.numberinsurat).in_(layout_ayahs))
                # Remove default ordering to ensure we can sort manually
                stmt = stmt.order_by(None)
                
                res = await session.execute(stmt)
                result = list(res.all())
                # Sort in memory based on layout sequence
                result.sort(key=lambda x: order_map.get((x.id, x.numberinsurat), 999))
            else:
                stmt = stmt.filter(Ayat.page_id == page_number)
                # Ensure deterministic ayah ordering for page responses.
                stmt = stmt.order_by(Ayat.number)
                res = await session.execute(stmt.limit(limit).offset(offset))
                result = res.all()

        if not result:
            # No ayahs found for this page and edition — return empty list to indicate success with no items
            return []

        ayahs = []
        surahs = []
        surah_ids = []
        surahs_ayat_counter = {}
        async with AsyncSessionLocal() as session2:
             for (spec_edition_id, spec_surah, spec_ayah), is_split in SPECIAL_NARRATION_PAGE_SPLITS.items():
                if spec_edition_id == edition_identifier:
                    prev_res = await session2.execute(
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
                            Surat.numberofayats,
                        )
                        .join(Surat, Ayat.surat_id == Surat.id)
                        .filter(
                            Ayat.surat_id == spec_surah,
                            Ayat.numberinsurat == spec_ayah,
                            Ayat.edition_id == edition_id,
                        )
                    )
                    prev_item = prev_res.first()

                    # Check if this special ayah is on the previous page
                    if prev_item and prev_item.page_id == page_number - 1:
                         # Build an ayah object but mark page as current page
                        extra_ayah = {
                            "number": prev_item.number,
                            "text": prev_item.text,
                            "surah": {
                                "number": prev_item.id,
                                "name": prev_item.name.get("ar") if isinstance(prev_item.name, dict) else None,
                                "englishName": prev_item.name.get("en") if isinstance(prev_item.name, dict) else None,
                                "englishNameTranslation": prev_item.englishtranslation,
                                "revelationType": prev_item.revelationcity,
                                "numberOfAyahs": prev_item.numberofayats,
                            },
                            "numberInSurah": prev_item.numberinsurat,
                            "juz": prev_item.juz_id,
                            "manzil": prev_item.manzil_id,
                            "page": page_number,  # override: this response is for current page
                            "ruku": prev_item.ruku_id,
                            "hizbQuarter": prev_item.hizbquarter_id,
                            "sajda": prev_item.sajda_id if prev_item.sajda_id else False,
                        }

                        # Get all words using its original page_id so split logic works
                        if edition.type == "narration" or edition.format == "audio":
                            extra_words = await get_words(
                                prev_item.id,
                                prev_item.numberinsurat,
                                prev_item.page_id,
                                prev_item.text,
                                edition_identifier,
                                last_ayah=None,
                                is_narration=True,
                                include_tajweed=tajweed,
                                tajweed_level=tajweed_level,
                                line_map=line_map
                            )
                        else:
                            extra_words = await get_words(
                                prev_item.id,
                                prev_item.numberinsurat,
                                prev_item.page_id,
                                prev_item.text,
                                edition_identifier,
                                last_ayah=None,
                                include_tajweed=tajweed,
                                tajweed_level=tajweed_level,
                                line_map=line_map
                            )

                        # Keep only the continuation part that belongs to this page
                        extra_words = [
                            w for w in extra_words
                            if w.get("page_number") == page_number
                        ]

                        if extra_words:
                            extra_ayah["words"] = extra_words
                            
                            # Put this ayah at the beginning of the list
                            ayahs.append(extra_ayah)

                            # Initialize surah tracking with this surah if not present
                            if prev_item.id not in surah_ids:
                                surahs.append({
                                    "number": prev_item.id,
                                    "name": prev_item.name.get("ar") if isinstance(prev_item.name, dict) else None,
                                    "englishName": prev_item.name.get("en") if isinstance(prev_item.name, dict) else None,
                                    "englishNameTranslation": prev_item.englishtranslation,
                                    "revelationType": prev_item.revelationcity,
                                    "numberOfAyahs": prev_item.numberofayats,
                                })
                                surah_ids.append(prev_item.id)
                                surahs_ayat_counter[prev_item.id] = 1
                            else:
                                surahs_ayat_counter[prev_item.id] += 1

        for item in result:
            ayah = {
                "number": item.number,
                "text": item.text,
                "surah": {
                    "number": item.id,
                    "name": item.name.get("ar") if isinstance(item.name, dict) else None,
                    "englishName": item.name.get("en") if isinstance(item.name, dict) else None,
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

            if words:
                last_ayah = ayahs[-1] if ayahs else None
                if edition.type == "narration" or edition.format == "audio":
                    ayah_words = await get_words(
                        item.id,
                        item.numberinsurat,
                        page_number,
                        item.text,
                        edition_identifier,
                        last_ayah,
                        is_narration=True,
                        include_tajweed=tajweed,
                        tajweed_level=tajweed_level,
                        line_map=line_map
                    )
                else:
                    ayah_words = await get_words(
                        item.id,
                        item.numberinsurat,
                        page_number,
                        item.text,
                        edition_identifier,
                        last_ayah,
                        include_tajweed=tajweed,
                        tajweed_level=tajweed_level,
                        line_map=line_map
                    )

                # IMPORTANT: keep only words that belong to this page
                ayah_words = [
                    w for w in ayah_words
                    if w.get("page_number") == page_number
                ]

                ayah["words"] = ayah_words


            ayahs.append(ayah)

            if item.id not in surah_ids:
                surahs.append({
                    "number": item.id,
                    "name": item.name.get("ar") if isinstance(item.name, dict) else None,
                    "englishName": item.name.get("en") if isinstance(item.name, dict) else None,
                    "englishNameTranslation": item.englishtranslation,
                    "revelationType": item.revelationcity,
                    "numberOfAyahs": item.numberofayats
                })
                surah_ids.append(item.id)
                surahs_ayat_counter[item.id] = 1
            else:
                surahs_ayat_counter[item.id] += 1

        if edition.format == "audio":
            bitrates = edition.bitrates
            max_bitrate = max(bitrates)
            remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
            for item in ayahs:
                verse_number = item["number"]
                item["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, verse_number)
                item["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, verse_number)

        # Always return ayahs ordered ascending by global ayah number.
        ayahs.sort(key=lambda x: x["number"])

        edition_info = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name.get("ar") if isinstance(edition.name, dict) else None,
            "englishName": edition.name.get("en") if isinstance(edition.name, dict) else None,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        hizb_numbers = await get_hizb_numbers(page_number, edition_id)
        max_juz_number = max((ayah.get("juz") for ayah in ayahs if ayah.get("juz") is not None), default=None)
        top_page_surah_number = max(surahs_ayat_counter, key=surahs_ayat_counter.get)
        top_page_surah = next(
            (surah for surah in surahs if surah["number"] == top_page_surah_number),
            {"number": top_page_surah_number}
        )

        return {
            "number": page_number,
            "topPageSurah": top_page_surah,
            "topPageJuz": max_juz_number,
            "hizbNumbers": hizb_numbers,
            "ayahs": ayahs,
            "surahs": surahs,
            "edition": edition_info
        }

    except Exception as e:
        logger.error("An exception occurred: %s", str(e), exc_info=True)
        return "An error occurred while fetching the page data."

async def get_all_pages(edition_identifier=DEFAULT_EDITION_IDENTIFIER):
    try:
        edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(edition, str):  # Error fetching edition
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
            # Query first ayah of each page in a single query
            result = await session.execute(
                select(
                    Ayat.page_id,
                    Ayat.number,
                    Ayat.text,
                    Ayat.numberinsurat,
                    Surat.id,
                    Surat.name,
                    Surat.englishname,
                    Surat.englishtranslation,
                    Surat.revelationcity,
                    Surat.numberofayats
                ).join(Surat, Ayat.surat_id == Surat.id).filter(
                    Ayat.edition_id == edition_id
                ).order_by(Ayat.page_id, Ayat.number)
            )

            fetched_data = result.fetchall()
            page_data_map = {}

            # Process the fetched data to group by page_id
            for item in fetched_data:
                page_id = item.page_id
                if page_id not in page_data_map:
                    page_data_map[page_id] = {
                        "number": page_id,
                        "firstAyah": {
                            "number": item.number,
                            "text": item.text,
                            "numberInSurah": item.numberinsurat,
                        },
                        "firstSurah": {
                            "number": item.id,
                            "name": item.name.get("ar") if isinstance(item.name, dict) else None,
                            "englishName": item.name.get("en") if isinstance(item.name, dict) else None,
                            "englishNameTranslation": item.englishtranslation,
                            "revelationType": item.revelationcity,
                            "numberOfAyahs": item.numberofayats
                        }
                    }

            pages_info = list(page_data_map.values())

        if not pages_info:
            # No pages found for this edition — return empty list
            return []

        edition_data = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name.get("ar") if isinstance(edition.name, dict) else None,
            "englishName": edition.name.get("en") if isinstance(edition.name, dict) else None,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        return {
            "pages": pages_info,
            "edition": edition_data
        }

    except Exception as e:
        logger.error("An exception occurred while fetching all pages: %s", str(e))
        return "An error occurred while fetching all pages data."