

from db.session import AsyncSessionLocal
from db.models import QuranPhraseOccurrence, Word, Ayat, QuranPhrase, Surat
from sqlalchemy.future import select
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from repositories.narrations_numbering_repo import get_narration_numbering_from_narration
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls

async def get_mutashabihat_for_ayah(
    surah_number: int,
    ayah_number: int,
    edition_identifier: str = "quran-hafs",
    limit: int = 20,
    offset: int = 0
):
    """
    Returns a list of mutashabihat (ambiguous/similar phrases) for a given ayah, edition-aware.
    Supports pagination via limit and offset.
    """
    """
    Returns a list of mutashabihat (ambiguous/similar phrases) for a given ayah, edition-aware.
    Each item includes phrase_id, start_pos, end_pos, phrase_text, ayah_text, and source/target phrase metadata.
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

    ayah_results = []
    async with AsyncSessionLocal() as session:
        for hafs_ayah_number in hafs_ayah_numbers:
            occ_query = (
                select(QuranPhraseOccurrence)
                .where(
                    QuranPhraseOccurrence.surat_id == surah_number,
                    QuranPhraseOccurrence.numberinsurat == hafs_ayah_number
                )
                .order_by(QuranPhraseOccurrence.start_pos, QuranPhraseOccurrence.phrase_id)
                .offset(offset)
                .limit(limit)
            )
            occs = (await session.execute(occ_query)).scalars().all()

            for occ in occs:
                # Fetch phrase meta from QuranPhrase (source/target info)
                phrase = await session.execute(
                    select(QuranPhrase).where(QuranPhrase.phrase_id == occ.phrase_id)
                )
                phrase = phrase.scalar_one_or_none()
                # Default to requested ayah if no phrase meta
                source_surat_id = surah_number
                source_numberinsurat = hafs_ayah_number
                if phrase and phrase.source_surat_id and phrase.source_numberinsurat:
                    source_surat_id = phrase.source_surat_id
                    source_numberinsurat = phrase.source_numberinsurat

                words = (await session.execute(
                    select(Word)
                    .where(
                        Word.surat_id == occ.surat_id,
                        Word.numberinsurat == occ.numberinsurat,
                        Word.position >= occ.start_pos,
                        Word.position <= occ.end_pos
                    )
                    .order_by(Word.position)
                )).scalars().all()
                phrase_text = ' '.join([w.text for w in words if w.text])

                # Get ayah object for this phrase occurrence (match ayah_repo structure)
                if is_hafs:
                    hafs_edition = await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
                    if isinstance(hafs_edition, str):
                        continue
                    elif isinstance(hafs_edition, list):
                        hafs_edition = hafs_edition[0] if hafs_edition[0].type == "versebyverse" else hafs_edition[1]
                    hafs_edition_id = hafs_edition.id
                    ayah_obj = await session.execute(
                        select(Ayat, Surat)
                        .join(Surat, Ayat.surat_id == Surat.id)
                        .where(
                            Ayat.surat_id == source_surat_id,
                            Ayat.numberinsurat == source_numberinsurat,
                            Ayat.edition_id == hafs_edition_id
                        )
                    )
                    ayah_row = ayah_obj.first()
                else:
                    target_ayah_numbers = await get_narration_numbering_from_narration(
                        source_surat_id, source_numberinsurat, "quran-hafs", narrator_id
                    )
                    ayah_row = None
                    for target_ayah_number in target_ayah_numbers:
                        ayah_obj = await session.execute(
                            select(Ayat, Surat)
                            .join(Surat, Ayat.surat_id == Surat.id)
                            .where(
                                Ayat.surat_id == source_surat_id,
                                Ayat.numberinsurat == target_ayah_number,
                                Ayat.edition_id == target_edition_id
                            )
                        )
                        ayah_row = ayah_obj.first()
                        if ayah_row:
                            break

                if not ayah_row:
                    continue
                ayat, surat = ayah_row

                ayah_result = {
                    "number": ayat.number,
                    "text": ayat.text,
                    "numberInSurah": ayat.numberinsurat,
                    "juz": ayat.juz_id,
                    "manzil": ayat.manzil_id,
                    "page": ayat.page_id,
                    "ruku": ayat.ruku_id,
                    "hizbQuarter": ayat.hizbquarter_id,
                    "sajda": ayat.sajda_id if ayat.sajda_id else False,
                    "surah": {
                        "number": surat.id,
                        "name": surat.name,
                        "englishName": surat.englishname,
                        "englishNameTranslation": surat.englishtranslation,
                        "revelationType": surat.revelationcity,
                        "numberOfAyahs": surat.numberofayats
                    },
                    "startPos": occ.start_pos,
                    "endPos": occ.end_pos,
                    "phraseText": phrase_text
                }

                # Add audio fields if response edition is audio
                if response_edition.format == "audio":
                    bitrates = response_edition.bitrates
                    max_bitrate = max(bitrates)
                    remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                    ayah_result["audio"] = get_ayah_audio_url(max_bitrate, response_edition.identifier, ayat.number)
                    ayah_result["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, response_edition.identifier, ayat.number)

                ayah_results.append(ayah_result)
    return ayah_results