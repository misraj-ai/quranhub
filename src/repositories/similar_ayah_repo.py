
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import QuranAyahMatch, QuranAyahMatchSpan, Ayat, Surat, Word
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from repositories.narrations_numbering_repo import get_narration_numbering_from_narration
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls


from db.session import AsyncSessionLocal

async def get_similar_ayahs_for_ayah(
    surah_number: int,
    ayah_number: int,
    edition_identifier: str = "quran-hafs",
    limit: int = 20,
    offset: int = 0
):
    """
    Returns a list of similar ayahs for a given ayah, edition-aware.
    Supports pagination via limit and offset.
    """
    edition = await get_edition_by_identifier(edition_identifier)
    if isinstance(edition, str):
        return []
    elif isinstance(edition, list):
        edition = edition[0] if edition[0].type == "versebyverse" else edition[1]
    # For audio editions, use text edition for ayah lookup, but keep original edition for response
    if edition.format == "audio":
        text_edition = await get_text_edition_for_narrator(edition.identifier)
        if isinstance(text_edition, str):
            return []
        target_edition_id = text_edition.id
        response_edition = edition
    else:
        target_edition_id = edition.id
        response_edition = edition

    narrator_id = response_edition.narrator_identifier if response_edition.format == "audio" else response_edition.identifier
    is_hafs = narrator_id == "quran-hafs"

    # Map ayah_number to Hafs if needed
    hafs_ayah_numbers = [ayah_number]
    if not is_hafs:
        hafs_ayah_numbers = await get_narration_numbering_from_narration(
            surah_number, ayah_number, narrator_id, "quran-hafs"
        )
        if not hafs_ayah_numbers:
            return []

    ayah_objs = []
    async with AsyncSessionLocal() as db:
        for hafs_ayah_number in hafs_ayah_numbers:
            # Get all matches for this source ayah, paginated
            q = (
                select(QuranAyahMatch)
                .where(
                    QuranAyahMatch.source_surat_id == surah_number,
                    QuranAyahMatch.source_numberinsurat == hafs_ayah_number
                )
                .offset(offset)
                .limit(limit)
            )
            result = await db.execute(q)
            matches = result.scalars().all()
            if not matches:
                continue

            for match in matches:
                # Get matched ayah (must exist in this edition)
                ayah_q = select(Ayat).where(
                    Ayat.surat_id == match.matched_surat_id,
                    Ayat.numberinsurat == match.matched_numberinsurat,
                    Ayat.edition_id == target_edition_id
                )
                ayah_result = await db.execute(ayah_q)
                ayah = ayah_result.scalar_one_or_none()
                if not ayah:
                    continue
                # Get surah
                surah_q = select(Surat).where(Surat.id == match.matched_surat_id)
                surah_result = await db.execute(surah_q)
                surah = surah_result.scalar_one_or_none()
                # Get all spans for this match
                span_q = select(QuranAyahMatchSpan).where(
                    QuranAyahMatchSpan.source_surat_id == match.source_surat_id,
                    QuranAyahMatchSpan.source_numberinsurat == match.source_numberinsurat,
                    QuranAyahMatchSpan.matched_surat_id == match.matched_surat_id,
                    QuranAyahMatchSpan.matched_numberinsurat == match.matched_numberinsurat
                )
                span_result = await db.execute(span_q)
                spans = span_result.scalars().all()
                # For each span, get the matched text
                span_objs = []
                for span in spans:
                    word_q = select(Word).where(
                        Word.surat_id == span.matched_surat_id,
                        Word.numberinsurat == span.matched_numberinsurat,
                        Word.position >= span.start_pos,
                        Word.position <= span.end_pos
                    ).order_by(Word.position)
                    word_result = await db.execute(word_q)
                    words = word_result.scalars().all()
                    matched_text = ' '.join([w.text for w in words if w.text])
                    span_objs.append({
                        "startPos": span.start_pos,
                        "endPos": span.end_pos,
                        "matchedText": matched_text
                    })
                # Canonical ayah object + match info
                ayah_obj = {
                    "number": ayah.number,
                    "text": ayah.text,
                    "numberInSurah": ayah.numberinsurat,
                    "juz": ayah.juz_id,
                    "manzil": ayah.manzil_id,
                    "page": ayah.page_id,
                    "ruku": ayah.ruku_id,
                    "hizbQuarter": ayah.hizbquarter_id,
                    "hizb": ayah.hizb_id,
                    "sajda": ayah.sajda_id,
                    "surah": {
                        "id": surah.id if surah else match.matched_surat_id,
                        "name": surah.name if surah else None,
                        "englishName": surah.englishname if surah else None,
                        "englishTranslation": surah.englishtranslation if surah else None,
                        "revelationCity": surah.revelationcity if surah else None,
                        "numberOfAyahs": surah.numberofayats if surah else None,
                        "revelationOrder": surah.revelation_order if surah else None
                    },
                    "score": match.score,
                    "coverage": match.coverage,
                    "matchedWordsCount": match.matched_words_count,
                    "spans": span_objs
                }

                # Add audio fields if response edition is audio
                if response_edition.format == "audio":
                    bitrates = response_edition.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    ayah_obj["audio"] = get_ayah_audio_url(max_bitrate, response_edition.identifier, ayah.number)
                    ayah_obj["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, response_edition.identifier, ayah.number)

                ayah_objs.append(ayah_obj)
    return ayah_objs
