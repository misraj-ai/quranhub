

from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from utils.helpers import add_cache_headers

from repositories.similar_ayah_repo import get_similar_ayahs_for_ayah
from repositories.ayah_repo import get_an_ayah_by_surah_number
from .similar_ayah_docs import getSimilarAyahsResponse

similar_ayah_router = APIRouter()

# Endpoint 1: /similar-ayah/{surahNumber}/{ayahNumber} (defaults to Hafs)
@similar_ayah_router.get(
    "/{surahNumber}/{ayahNumber}",
    tags=["Similar Ayah"],
    summary="Get Similar Ayahs for an Ayah (Hafs)",
    description="Get all similar ayahs for a given ayah in the Hafs narration. Returns canonical ayah objects with match spans, score, and coverage. Useful for LLMs, UIs, and advanced workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve all similar ayahs for a specific ayah in the Hafs narration. Returns canonical ayah objects with match spans, score, and coverage.",
        "x-mcp-example": {"surahNumber": 2, "ayahNumber": 23, "limit": 10, "offset": 0}
    },
    responses=getSimilarAyahsResponse
)
async def get_similar_ayahs_for_ayah_hafs(
    surah_number: int = Path(..., alias="surahNumber", ge=1, le=114, description="Surah number (1-114). The chapter of the Quran."),
    ayah_number: int = Path(..., alias="ayahNumber", ge=1, description="Ayah number (1-based, within the surah). The verse number in the chapter."),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return (default 20, max 100)."),
    offset: int = Query(0, ge=0, description="Number of results to skip for pagination (default 0).")
):
    data = await get_similar_ayahs_for_ayah(surah_number, ayah_number, "quran-hafs", limit=limit, offset=offset)
    if not data:
        response = JSONResponse(content={"code": 404, "status": "Not Found", "data": "No similar ayahs found for the given parameters or ayah does not exist in this narration."}, status_code=404)
        response.headers["Cache-Control"] = "no-store"
        return response

    ayah_meta = await get_an_ayah_by_surah_number(surah_number, ayah_number, "quran-hafs")
    if isinstance(ayah_meta, str):
        ayah_meta = None

    response_data = {
        "code": 200,
        "status": "OK",
        "data": data,
    }
    if ayah_meta:
        response_data["number"] = ayah_meta.get("number")
        response_data["numberInSurah"] = ayah_meta.get("numberInSurah")
        response_data["surah"] = ayah_meta.get("surah")
        response_data["edition"] = ayah_meta.get("edition")
    response = JSONResponse(content=response_data, status_code=200)
    add_cache_headers(response, cache_tag=f"similar_ayah:{surah_number}:{ayah_number}:hafs")
    return response

# Endpoint 2: /similar-ayah/{surahNumber}/{ayahNumber}/{editionIdentifier}
@similar_ayah_router.get(
    "/{surahNumber}/{ayahNumber}/{editionIdentifier}",
    tags=["Similar Ayah"],
    summary="Get Similar Ayahs for an Ayah (by Edition)",
    description="Get all similar ayahs for a given ayah in the specified narration/edition. Returns canonical ayah objects with match spans, score, and coverage. Useful for LLMs, UIs, and advanced workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve all similar ayahs for a specific ayah in a specific narration/edition. Returns canonical ayah objects with match spans, score, and coverage.",
        "x-mcp-example": {"surahNumber": 2, "ayahNumber": 23, "editionIdentifier": "quran-uthmani", "limit": 10, "offset": 0},
        "x-arg-aliases": {"editionIdentifier": ["edition", "narration"]}
    },
    responses=getSimilarAyahsResponse
)
async def get_similar_ayahs_for_ayah_edition(
    surahNumber: int = Path(..., alias="surahNumber", ge=1, le=114, description="Surah number (1-114). The chapter of the Quran."),
    ayahNumber: int = Path(..., alias="ayahNumber", ge=1, description="Ayah number (1-based, within the surah). The verse number in the chapter."),
    editionIdentifier: str = Path(..., alias="editionIdentifier", description="Edition identifier (e.g., 'quran-hafs', 'quran-uthmani', etc.). Determines the narration/edition for ayah mapping and text."),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return (default 20, max 100)."),
    offset: int = Query(0, ge=0, description="Number of results to skip for pagination (default 0).")
):
    data = await get_similar_ayahs_for_ayah(surahNumber, ayahNumber, editionIdentifier, limit=limit, offset=offset)
    if not data:
        response = JSONResponse(content={"code": 404, "status": "Not Found", "data": "No similar ayahs found for the given parameters or ayah does not exist in this narration."}, status_code=404)
        response.headers["Cache-Control"] = "no-store"
        return response

    ayah_meta = await get_an_ayah_by_surah_number(surahNumber, ayahNumber, editionIdentifier)
    if isinstance(ayah_meta, str):
        ayah_meta = None

    response_data = {
        "code": 200,
        "status": "OK",
        "data": data,
    }
    if ayah_meta:
        response_data["number"] = ayah_meta.get("number")
        response_data["numberInSurah"] = ayah_meta.get("numberInSurah")
        response_data["surah"] = ayah_meta.get("surah")
        response_data["edition"] = ayah_meta.get("edition")
    response = JSONResponse(content=response_data, status_code=200)
    add_cache_headers(response, cache_tag=f"similar_ayah:{surahNumber}:{ayahNumber}:{editionIdentifier}")
    return response
