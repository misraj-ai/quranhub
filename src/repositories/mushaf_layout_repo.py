from sqlalchemy.future import select
from sqlalchemy import func
from db.models import MushafLayout, MushafLine, Font, Word
from db.session import AsyncSessionLocal
from typing import Dict, List, Tuple, Optional

# Canonical repo pattern for mushaf layout feature

def _build_layout_filters(code=None, lines_per_page=None, font_code=None):
    filters = []
    if code:
        filters.append(MushafLayout.code == code)
    if lines_per_page:
        filters.append(MushafLayout.lines_per_page == lines_per_page)
    if font_code:
        filters.append(Font.code == font_code)
    return filters

async def get_layouts(code=None, lines_per_page=None, font_code=None, limit=20, offset=0):
    async with AsyncSessionLocal() as session:
        filters = _build_layout_filters(code, lines_per_page, font_code)
        stmt = select(MushafLayout).join(Font, isouter=True)
        if filters:
            stmt = stmt.where(*filters)
        stmt = stmt.order_by(MushafLayout.layout_id).limit(limit).offset(offset)
        result = await session.execute(stmt)
        items = result.scalars().all()
        total_stmt = select(func.count()).select_from(MushafLayout).join(Font, isouter=True)
        if filters:
            total_stmt = total_stmt.where(*filters)
        total = (await session.execute(total_stmt)).scalar()
        return {"total": total, "items": items}

async def get_layout_by_code(code: str):
    async with AsyncSessionLocal() as session:
        stmt = select(MushafLayout).where(MushafLayout.code == code)
        result = await session.execute(stmt)
        layout = result.scalar_one_or_none()
        return layout

async def get_layout_font(font_id: int):
    async with AsyncSessionLocal() as session:
        stmt = select(Font).where(Font.font_id == font_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def get_lines_for_page(layout_id: int, page: int):
    async with AsyncSessionLocal() as session:
        stmt = select(MushafLine).where(MushafLine.layout_id == layout_id, MushafLine.page_number == page).order_by(MushafLine.line_number)
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_lines_for_surah(layout_id: int, surah_number: int):
    async with AsyncSessionLocal() as session:
        stmt = select(MushafLine).where(MushafLine.layout_id == layout_id, MushafLine.surah_number == surah_number).order_by(MushafLine.page_number, MushafLine.line_number)
        result = await session.execute(stmt)
        return result.scalars().all()

async def lookup_lines(layout_id: int, from_word_id=None, to_word_id=None):
    async with AsyncSessionLocal() as session:
        filters = [MushafLine.layout_id == layout_id]
        # Overlap logic: only consider lines with non-null word ids
        if from_word_id is not None or to_word_id is not None:
            filters.append(MushafLine.ext_first_word_id.isnot(None))
            filters.append(MushafLine.ext_last_word_id.isnot(None))
        if from_word_id is not None and to_word_id is not None:
            filters.append(MushafLine.ext_last_word_id >= from_word_id)
            filters.append(MushafLine.ext_first_word_id <= to_word_id)
        elif from_word_id is not None:
            filters.append(MushafLine.ext_last_word_id >= from_word_id)
        elif to_word_id is not None:
            filters.append(MushafLine.ext_first_word_id <= to_word_id)
        stmt = select(MushafLine).where(*filters).order_by(MushafLine.page_number, MushafLine.line_number)
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_page_ayahs_and_lines(layout_id: int, page_number: int) -> Tuple[List[Tuple[int, int]], Dict[int, int]]:
    """
    Returns a list of unique ayahs (surat_id, numberinsurat) and a map of {word_id: line_number}
    for a specific page in a given layout.
    """
    async with AsyncSessionLocal() as session:
        # 1. Fetch all lines for the page
        stmt = (
            select(
                MushafLine.line_number, 
                MushafLine.ext_first_word_id, 
                MushafLine.ext_last_word_id
            )
            .where(
                MushafLine.layout_id == layout_id,
                MushafLine.page_number == page_number,
                MushafLine.ext_first_word_id.isnot(None),
                MushafLine.ext_last_word_id.isnot(None)
            )
            .order_by(MushafLine.line_number)
        )
        result = await session.execute(stmt)
        lines = result.all()

        if not lines:
            return [], {}

        word_id_to_line = {}
        all_word_ids = []
        for line in lines:
            # Add all word IDs in the range to our mapping
            for word_id in range(line.ext_first_word_id, line.ext_last_word_id + 1):
                word_id_to_line[word_id] = line.line_number
                all_word_ids.append(word_id)

        if not all_word_ids:
            return [], {}

        # 2. Find unique ayahs for these word IDs
        ayah_stmt = (
            select(Word.surat_id, Word.numberinsurat)
            .where(Word.id.in_(all_word_ids))
            .distinct()
            .order_by(Word.surat_id, Word.numberinsurat)
        )
        ayah_result = await session.execute(ayah_stmt)
        ayahs = ayah_result.all()

        return ayahs, word_id_to_line