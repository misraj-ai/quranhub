


from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse
from repositories.ayah_theme_repo import get_all_themes, get_themes_for_ayah
from .ayah_theme_docs import getAyahThemesResponse, getThemesForAyahResponse
from utils.helpers import add_cache_headers

ayah_theme_router = APIRouter()


@ayah_theme_router.get(
    "/themes",
    tags=["Ayah Theme"],
    summary="Get all ayah themes",
    description="Returns a paginated list of all ayah themes. Useful for UIs, LLMs, and analytics.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to list all ayah themes with pagination.",
        "x-mcp-example": {"limit": 2, "offset": 0}
    },
    responses=getAyahThemesResponse
)
async def get_ayah_themes(
    limit: int = Query(20, ge=1, le=100, alias="limit", description="Maximum number of themes to return (default 20, max 100)."),
    offset: int = Query(0, ge=0, alias="offset", description="Number of themes to skip for pagination (default 0).")
):
    themes = await get_all_themes(limit=limit, offset=offset)
    response = JSONResponse(
        content={
            "code": 200,
            "status": "OK",
            "data": [
                {
                    "name": t.name,
                    "keywords": t.keywords,
                    "totalAyahs": t.total_ayahs
                } for t in themes
            ]
        },
        status_code=200
    )
    add_cache_headers(response, cache_tag=f"ayah_theme:themes:{limit}:{offset}")
    return response





@ayah_theme_router.get(
    "/{surahId}/{ayahNumber}",
    tags=["Ayah Theme"],
    summary="Get themes for an ayah",
    description="Returns a paginated list of themes for a given ayah (by surah and ayah number).",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to get all themes for a specific ayah (by surah and ayah number) with pagination.",
        "x-mcp-example": {"surahId": 2, "ayahNumber": 30, "limit": 20, "offset": 0}
    },
    responses=getThemesForAyahResponse
)
async def get_themes_for_ayah_endpoint(
    surahId: int = Path(..., ge=1, le=114, alias="surahId", description="Surah number (1-114)"),
    ayahNumber: int = Path(..., ge=1, alias="ayahNumber", description="Ayah number in surah"),
    limit: int = Query(20, ge=1, le=100, alias="limit", description="Maximum number of themes to return (default 20, max 100)."),
    offset: int = Query(0, ge=0, alias="offset", description="Number of themes to skip for pagination (default 0).")
):
    themes = await get_themes_for_ayah(surahId, ayahNumber, limit=limit, offset=offset)
    if not themes:
        response = JSONResponse(
            content={"code": 404, "status": "Not Found", "data": "No themes found for this ayah."},
            status_code=404
        )
        response.headers["Cache-Control"] = "no-store"
        return response
    response = JSONResponse(
        content={
            "code": 200,
            "status": "OK",
            "data": [
                {
                    "name": t.name,
                    "keywords": t.keywords,
                    "totalAyahs": t.total_ayahs
                } for t in themes
            ]
        },
        status_code=200
    )
    add_cache_headers(response, cache_tag=f"ayah_theme:{surahId}:{ayahNumber}:{limit}:{offset}")
    return response
