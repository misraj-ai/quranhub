"""
Global word numbering.

The global word number is the 1-based rank of a word in surah -> ayah -> position
order (1..77432), the word-level analogue of the global ayah number (1..6236).
It is derived from per-ayah word counts loaded once from the `word` table, not
from `word.id`, which is neither contiguous nor ordered.
"""

from typing import Dict, Optional, Tuple

from utils.logger import logger

# (surah, ayah) -> global number of that ayah's first word minus one
_offsets: Dict[Tuple[int, int], int] = {}
_total_words: int = 0


def set_word_counts(counts: Dict[Tuple[int, int], int]) -> None:
    """Build the offset table from {(surah, ayah): word_count}."""
    global _total_words
    _offsets.clear()
    running = 0
    for key in sorted(counts):
        _offsets[key] = running
        running += counts[key]
    _total_words = running


def is_loaded() -> bool:
    return bool(_offsets)


def total_words() -> int:
    return _total_words


def global_word_number(surah: int, ayah: int, position: int) -> Optional[int]:
    """Global word number for a location, or None if the ayah is unknown or not loaded."""
    offset = _offsets.get((surah, ayah))
    if offset is None:
        return None
    return offset + position


async def load_word_offsets() -> bool:
    """Load per-ayah word counts from the database. Returns True on success."""
    try:
        from sqlalchemy import func, select
        from db.models import Word
        from db.session import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Word.surat_id, Word.numberinsurat, func.count(Word.id))
                .group_by(Word.surat_id, Word.numberinsurat)
            )
            counts = {(surah, ayah): n for surah, ayah, n in result.all()}
        if not counts:
            logger.warning("Word numbering: the word table is empty; per-word audio will be unavailable")
            return False
        set_word_counts(counts)
        logger.info(f"Word numbering loaded: {len(counts)} ayahs, {_total_words} words")
        return True
    except Exception as e:
        logger.error(f"Word numbering failed to load: {e}", exc_info=True)
        return False
