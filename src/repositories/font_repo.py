from sqlalchemy.future import select
from sqlalchemy import func, distinct
from db.models import Font, FontFile, FontPageFile
from db.session import AsyncSessionLocal

async def get_all_font_categories():
    async with AsyncSessionLocal() as session:
        stmt = select(distinct(Font.category)).order_by(Font.category)
        result = await session.execute(stmt)
        categories = [row[0] for row in result.fetchall() if row[0] is not None]
        return categories
# --- Canonical queries for unique font formats, kinds, and archive types ---

async def get_all_font_formats():
    async with AsyncSessionLocal() as session:
        stmt = select(distinct(FontFile.format)).order_by(FontFile.format)
        result = await session.execute(stmt)
        formats = [row[0] for row in result.fetchall() if row[0] is not None]
        return formats

async def get_all_font_kinds():
    async with AsyncSessionLocal() as session:
        stmt = select(distinct(FontFile.kind)).order_by(FontFile.kind)
        result = await session.execute(stmt)
        kinds = [row[0] for row in result.fetchall() if row[0] is not None]
        return kinds

async def get_all_font_archives():
    async with AsyncSessionLocal() as session:
        stmt = select(distinct(FontFile.archive_ext)).order_by(FontFile.archive_ext)
        result = await session.execute(stmt)
        # None means 'none' (unarchived)
        archives = [row[0] if row[0] is not None else 'none' for row in result.fetchall()]
        # Remove duplicates of 'none' if present
        return sorted(set(archives))

async def get_all_page_file_formats():
    async with AsyncSessionLocal() as session:
        stmt = select(distinct(FontPageFile.format)).order_by(FontPageFile.format)
        result = await session.execute(stmt)
        formats = [row[0] for row in result.fetchall() if row[0] is not None]
        return formats
# Font repository: data access and service layer for font, font_file, font_page_file

from sqlalchemy.future import select
from sqlalchemy import func
from db.models import Font, FontFile, FontPageFile
from db.session import AsyncSessionLocal

# Canonical repo pattern for font feature

def _build_font_filters(category=None, code=None):
    filters = []
    if category:
        filters.append(Font.category == category)
    if code:
        filters.append(Font.code == code)
    return filters

async def get_fonts(category=None, code=None, limit=20, offset=0):
    async with AsyncSessionLocal() as session:
        filters = _build_font_filters(category, code)
        stmt = select(Font).where(*filters).order_by(Font.font_id).limit(limit).offset(offset)
        result = await session.execute(stmt)
        items = result.scalars().all()
        total_stmt = select(func.count()).select_from(Font).where(*filters)
        total = (await session.execute(total_stmt)).scalar()
        return {"total": total, "items": items}

async def get_font_by_code(code: str):
    async with AsyncSessionLocal() as session:
        stmt = select(Font).where(Font.code == code)
        result = await session.execute(stmt)
        font = result.scalar_one_or_none()
        return font

async def get_font_files(font_id: int, kind=None, format=None, archive=None):
    async with AsyncSessionLocal() as session:
        filters = [FontFile.font_id == font_id]
        if kind:
            filters.append(FontFile.kind == kind)
        if format:
            filters.append(FontFile.format == format)
        if archive == 'none':
            filters.append(FontFile.archive_ext.is_(None))
        elif archive:
            filters.append(FontFile.archive_ext == archive)
        stmt = select(FontFile).where(*filters).order_by(FontFile.kind, FontFile.format)
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_font_page_files(font_id: int, page_number=None, format=None, limit=20, offset=0):
    async with AsyncSessionLocal() as session:
        filters = [FontPageFile.font_id == font_id]
        if page_number is not None:
            filters.append(FontPageFile.page_number == page_number)
        if format:
            filters.append(FontPageFile.format == format)
        stmt = select(FontPageFile).where(*filters).order_by(FontPageFile.page_number, FontPageFile.format)
        if page_number is None:
            stmt = stmt.limit(limit).offset(offset)
        result = await session.execute(stmt)
        items = result.scalars().all()
        if page_number is None:
            total_stmt = select(func.count()).select_from(FontPageFile).where(*filters)
            total = (await session.execute(total_stmt)).scalar()
            return {"total": total, "items": items}
        return items

async def get_font_page_range(font_id: int):
    async with AsyncSessionLocal() as session:
        stmt = select(func.min(FontPageFile.page_number), func.max(FontPageFile.page_number)).where(FontPageFile.font_id == font_id)
        result = await session.execute(stmt)
        return result.first()