from sqlalchemy import select
from db.models import QuranTheme, QuranAyahTheme, Ayat, Surat
from db.session import AsyncSessionLocal
from typing import List, Optional

# Canonical repo pattern for ayah theme feature

async def get_all_themes(limit: int = 20, offset: int = 0) -> List[QuranTheme]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(QuranTheme).order_by(QuranTheme.theme_id).limit(limit).offset(offset)
        )
        return result.scalars().all()

async def get_ayahs_for_theme(theme_id: int, limit: int = 20, offset: int = 0) -> List[dict]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(QuranAyahTheme, Ayat, Surat)
            .join(Ayat, (QuranAyahTheme.surat_id == Ayat.surat_id) & (QuranAyahTheme.numberinsurat == Ayat.numberinsurat))
            .join(Surat, Ayat.surat_id == Surat.id)
            .where(QuranAyahTheme.theme_id == theme_id)
            .order_by(QuranAyahTheme.surat_id, QuranAyahTheme.numberinsurat)
            .limit(limit).offset(offset)
        )
        # Return canonical ayah object with surah metadata
        return [
            {
                "number": ayat.number,
                "text": ayat.text,
                "numberInSurah": ayat.numberinsurat,
                "surah": {
                    "number": surat.id,
                    "name": surat.name,
                    "englishName": surat.englishname,
                    "englishNameTranslation": surat.englishtranslation,
                    "revelationType": surat.revelationcity,
                    "numberOfAyahs": surat.numberofayats
                }
            }
            for _, ayat, surat in result.all()
        ]

async def get_themes_for_ayah(surat_id: int, numberinsurat: int, limit: int = 20, offset: int = 0) -> List[QuranTheme]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(QuranTheme)
            .join(QuranAyahTheme, QuranTheme.theme_id == QuranAyahTheme.theme_id)
            .where(QuranAyahTheme.surat_id == surat_id, QuranAyahTheme.numberinsurat == numberinsurat)
            .order_by(QuranTheme.theme_id)
            .limit(limit).offset(offset)
        )
        return result.scalars().all()
