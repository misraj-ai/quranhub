from sqlalchemy.future import select
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls
from db.models import Ayat, Surat
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from repositories.hizb_repo import get_hizb_numbers
from repositories.word_repo import get_words
from utils.logger import logger
from db.session import AsyncSessionLocal
from utils.config import DEFAULT_EDITION_IDENTIFIER

async def get_page(page_number: int, edition_identifier: str, words: bool, limit: int, offset: int):
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
                .filter(Ayat.page_id == page_number, Ayat.edition_id == edition_id)
                .order_by(Ayat.number)
                .limit(limit)
                .offset(offset)
            )
            result = result.all()

        if not result:
            return "No ayahs found for this page and edition"

        ayahs = []
        surahs = []
        surah_ids = []
        surahs_ayat_counter = {}
        # Special case: in quran-aldouri, ayah 2:219 is split between pages 34 and 35.
        # For page 35 we need to also show the continuation of 2:219, but only its words
        # that are marked with page_number == 35 by word_repo.
        if words and edition_identifier == "quran-aldouri" and page_number == 35:
            async with AsyncSessionLocal() as session2:
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
                        Ayat.surat_id == 2,          # Surah al-Baqarah
                        Ayat.numberinsurat == 219,   # Ayah 219
                        Ayat.edition_id == edition_id,
                    )
                )
                prev_item = prev_res.first()

            if prev_item:
                # Build an ayah object for 2:219, but mark page as 35
                extra_ayah = {
                    "number": prev_item.number,
                    "text": prev_item.text,
                    "surah": {
                        "number": prev_item.id,
                        "name": prev_item.name,
                        "englishName": prev_item.englishname,
                        "englishNameTranslation": prev_item.englishtranslation,
                        "revelationType": prev_item.revelationcity,
                        "numberOfAyahs": prev_item.numberofayats,
                    },
                    "numberInSurah": prev_item.numberinsurat,
                    "juz": prev_item.juz_id,
                    "manzil": prev_item.manzil_id,
                    "page": page_number,  # override: this response is for page 35
                    "ruku": prev_item.ruku_id,
                    "hizbQuarter": prev_item.hizbquarter_id,
                    "sajda": prev_item.sajda_id if prev_item.sajda_id else False,
                }

                # Get all words for 2:219 using its original page_id (34)
                if edition.type == "narration" or edition.format == "audio":
                    extra_words = await get_words(
                        prev_item.id,
                        prev_item.numberinsurat,
                        prev_item.page_id,   # 34, so SPECIAL SPLIT in word_repo works
                        prev_item.text,
                        edition_identifier,
                        last_ayah=None,
                        is_narration=True,
                    )
                else:
                    extra_words = await get_words(
                        prev_item.id,
                        prev_item.numberinsurat,
                        prev_item.page_id,
                        prev_item.text,
                        edition_identifier,
                        last_ayah=None,
                    )

                # Keep only the continuation part that belongs to page 35
                extra_words = [
                    w for w in extra_words
                    if w.get("page_number") == page_number
                ]
                extra_ayah["words"] = extra_words

                # Put this ayah at the beginning of the list
                ayahs.append(extra_ayah)

                # Initialize surah tracking with this surah (usually Surah 2)
                surahs.append({
                    "number": prev_item.id,
                    "name": prev_item.name,
                    "englishName": prev_item.englishname,
                    "englishNameTranslation": prev_item.englishtranslation,
                    "revelationType": prev_item.revelationcity,
                    "numberOfAyahs": prev_item.numberofayats,
                })
                surah_ids.append(prev_item.id)
                surahs_ayat_counter[prev_item.id] = 1

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
                    )
                else:
                    ayah_words = await get_words(
                        item.id,
                        item.numberinsurat,
                        page_number,
                        item.text,
                        edition_identifier,
                        last_ayah,
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
                    "name": item.name,
                    "englishName": item.englishname,
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

        edition_info = {
            "identifier": edition.identifier,
            "language": edition.language,
            "name": edition.name,
            "englishName": edition.englishname,
            "format": edition.format,
            "type": edition.type,
            "direction": edition.direction
        }

        hizb_numbers = await get_hizb_numbers(page_number, edition_id)
        top_page_surah = max(surahs_ayat_counter, key=surahs_ayat_counter.get)
        for surah in surahs:
            if surah["number"] == top_page_surah:
                top_page_surah = surah
                break

        return {
            "number": page_number,
            "topPageSurah": top_page_surah,
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
                            "name": item.name,
                            "englishName": item.englishname,
                            "englishNameTranslation": item.englishtranslation,
                            "revelationType": item.revelationcity,
                            "numberOfAyahs": item.numberofayats
                        }
                    }

            pages_info = list(page_data_map.values())

        if not pages_info:
            return "No Pages found."

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
            "pages": pages_info,
            "edition": edition_data
        }

    except Exception as e:
        logger.error("An exception occurred while fetching all pages: %s", str(e))
        return "An error occurred while fetching all pages data."