
from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from repositories.mutashabihat_repo import get_mutashabihat_for_ayah
from repositories.ayah_repo import get_an_ayah_by_surah_number
from .mutashabihat_docs import getMutashabihatPhrasesResponse

mutashabihat_router = APIRouter()


# Endpoint 1: /mutashabihat/{surahNumber}/{ayahNumber} (defaults to Hafs)
@mutashabihat_router.get(
    "/{surahNumber}/{ayahNumber}",
    tags=["Mutashabihat"],
    summary="Get Mutashabihat Phrases for an Ayah (Hafs)",
    description="Get all mutashabihat (similar/ambiguous) phrases for a given ayah in the Hafs narration. Returns canonical ayah objects with phrase spans and audio fields if edition is audio. Useful for LLMs, UIs, and advanced workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve all mutashabihat phrases for a specific ayah in the Hafs narration. Returns canonical ayah objects with phrase spans and audio fields if audio edition.",
        "x-mcp-example": {"surahNumber": 2, "ayahNumber": 23, "limit": 2, "offset": 0}
    },
    responses=getMutashabihatPhrasesResponse
)
async def get_mutashabihat_phrases_for_ayah_hafs(
    surah_number: int = Path(..., alias="surahNumber", ge=1, le=114, description="Surah number (1-114). The chapter of the Quran."),
    ayah_number: int = Path(..., alias="ayahNumber", ge=1, description="Ayah number (1-based, within the surah). The verse number in the chapter."),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return (default 20, max 100)."),
    offset: int = Query(0, ge=0, description="Number of results to skip for pagination (default 0).")
):
    data = await get_mutashabihat_for_ayah(surah_number, ayah_number, "quran-hafs", limit=limit, offset=offset)
    if not data:
        return JSONResponse(content={"code": 404, "status": "Not Found", "data": "No mutashabihat phrases found for the given parameters or ayah does not exist in this narration."}, status_code=404)

    ayah_meta = await get_an_ayah_by_surah_number(surah_number, ayah_number, "quran-hafs")
    if isinstance(ayah_meta, str):
        ayah_meta = None

    response = {
        "code": 200,
        "status": "OK",
        "data": data,
    }
    if ayah_meta:
        response["number"] = ayah_meta.get("number")
        response["numberInSurah"] = ayah_meta.get("numberInSurah")
        response["surah"] = ayah_meta.get("surah")
        response["edition"] = ayah_meta.get("edition")
    return JSONResponse(content=response)

# Endpoint 2: /mutashabihat/{surahNumber}/{ayahNumber}/{editionIdentifier}
@mutashabihat_router.get(
    "/{surahNumber}/{ayahNumber}/{editionIdentifier}",
    tags=["Mutashabihat"],
    summary="Get Mutashabihat Phrases for an Ayah (by Edition)",
    description="Get all mutashabihat (similar/ambiguous) phrases for a given ayah in the specified narration/edition. Returns canonical ayah objects with phrase spans and audio fields if edition is audio. Useful for LLMs, UIs, and advanced workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve all mutashabihat phrases for a specific ayah in a specific narration/edition. Returns canonical ayah objects with phrase spans and audio fields if audio edition.",
        "x-mcp-example": {"surahNumber": 2, "ayahNumber": 23, "editionIdentifier": "quran-uthmani", "limit": 2, "offset": 0},
        "x-arg-aliases": {"editionIdentifier": ["edition", "narration"]}
    },
    responses=getMutashabihatPhrasesResponse
)
async def get_mutashabihat_phrases_for_ayah_edition(
    surah_number: int = Path(..., alias="surahNumber", ge=1, le=114, description="Surah number (1-114). The chapter of the Quran."),
    ayah_number: int = Path(..., alias="ayahNumber", ge=1, description="Ayah number (1-based, within the surah). The verse number in the chapter."),
    edition_identifier: str = Path(..., alias="editionIdentifier", description="Edition identifier (e.g., 'quran-hafs', 'quran-uthmani', 'ar.abdulbasitmurattal.hafs', etc.). Determines the narration/edition for ayah mapping and text."),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return (default 20, max 100)."),
    offset: int = Query(0, ge=0, description="Number of results to skip for pagination (default 0).")
):
    data = await get_mutashabihat_for_ayah(surah_number, ayah_number, edition_identifier, limit=limit, offset=offset)
    if not data:
        return JSONResponse(content={"code": 404, "status": "Not Found", "data": "No mutashabihat phrases found for the given parameters or ayah does not exist in this narration."}, status_code=404)

    ayah_meta = await get_an_ayah_by_surah_number(surah_number, ayah_number, edition_identifier)
    if isinstance(ayah_meta, str):
        ayah_meta = None

    response = {
        "code": 200,
        "status": "OK",
        "data": data,
    }
    if ayah_meta:
        response["number"] = ayah_meta.get("number")
        response["numberInSurah"] = ayah_meta.get("numberInSurah")
        response["surah"] = ayah_meta.get("surah")
        response["edition"] = ayah_meta.get("edition")
    return JSONResponse(content=response)