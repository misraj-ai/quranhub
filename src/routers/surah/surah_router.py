from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

import random
from repositories import surah_repo  # Using the repository now
from .surah_docs import (
getTheSurahbyEditionsResponse,
getTheSurahbyEditionResponse,
getTheSurahResponse,
getAllSurahResponse
)

from utils.logger import logger
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import add_cache_headers

surah_router = APIRouter()


@surah_router.get(
    "/",
    responses=getAllSurahResponse,
    tags=["Surah"],
    name="Get Surahs in Quran",
    description="Get the complete list of all 114 Surahs (chapters) in the Quran, with metadata such as page ranges, revelation details, and structural information. Useful for navigation, search, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve the full list of Surahs for navigation, search, or to display chapter metadata.",
        "x-mcp-example": {
            "revelationOrder": False
        }
    }
)
async def get_all_surah(
    revelationOrder: bool = Query(False, description="If true, order by revelation order instead of canonical order.", example=False)
):
    try:
        data = await surah_repo.get_all_surahs(revelationOrder)
        if isinstance(data, str):
            logger.error("Something went wrong: %s", str(data))
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_duration=2592000, browser_cache=3600, cache_tag="surahs-list")
        return response
    except Exception as e:
        logger.exception("An exception occurred while fetching surahs: %s", str(e))
        error_response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        error_response.headers["Cache-Control"] = "no-store"
        return error_response


@surah_router.get(
    "/byRevelationCity",
    tags=["Surah"],
    name="Get Surahs by Revelation City",
    description="Get all Surahs grouped by their revelation city (Meccan or Medinan). Useful for filtering chapters by historical context.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to group Surahs by their place of revelation for historical or thematic analysis.",
        "x-mcp-example": {}
    }
)
async def get_surahs_by_revelation_city():
    try:
        data = await surah_repo.get_all_revelation_cities_with_surahs()
        if isinstance(data, str):
            logger.error("Something went wrong: %s", str(data))
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_duration=2592000, browser_cache=3600, cache_tag="surahs-by-revelation-city")
        return response
    except Exception as e:
        logger.exception("An exception occurred while fetching surahs by revelation city: %s", str(e))
        error_response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        error_response.headers["Cache-Control"] = "no-store"
        return error_response


@surah_router.get(
    "/byJuz",
    tags=["Surah"],
    name="Get Surahs by Juz",
    description="Get all Surahs grouped by the Juz (part) of the Quran they belong to. Useful for navigation and study by Juz.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to group Surahs by Juz for navigation or study plans.",
        "x-mcp-example": {}
    }
)
async def get_surahs_by_juz():
    try:
        data = await surah_repo.get_all_juzs_with_surahs()
        if isinstance(data, str):
            logger.error("Something went wrong: %s", str(data))
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_duration=2592000, browser_cache=3600, cache_tag="surahs-by-juz")
        return response
    except Exception as e:
        logger.exception("An exception occurred while fetching surahs by Juz: %s", str(e))
        error_response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        error_response.headers["Cache-Control"] = "no-store"
        return error_response


@surah_router.get(
    "/{surahNumber}",
    responses=getTheSurahResponse,
    tags=["Surah"],
    name="Get a Surah by Number",
    description="Get a specific Surah (chapter) by its number (1-114), including all ayahs and metadata. Useful for retrieving the full text and structure of a chapter.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a single Surah by number for display, study, or LLM context.",
        "x-mcp-example": {"surahNumber": 1, "limit": 7, "offset": 0}
    }
)
async def get_the_surah(
    surahNumber: int = Path(..., ge=1, le=114, description="Surah number (1-114)"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a surah by the given number.", example=0)
):
    try:
        if surahNumber < 1 or surahNumber > 114:
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Surah number must be between 1 and 114."},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        data = await surah_repo.get_surah(surahNumber, DEFAULT_EDITION_IDENTIFIER, limit, offset)
        if isinstance(data, str):
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_duration=2592000, browser_cache=3600, cache_tag=f"surah-{surahNumber},edition-{DEFAULT_EDITION_IDENTIFIER}")
        return response
    except Exception as e:
        logger.exception("An exception occurred while fetching surah number %d: %s", surahNumber, str(e))
        error_response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        error_response.headers["Cache-Control"] = "no-store"
        return error_response


@surah_router.get(
    "/{surahNumber}/{editionIdentifier}",
    responses=getTheSurahbyEditionResponse,
    tags=["Surah"],
    name="Get a Surah by Number and Edition",
    description="Get a specific Surah by number and edition identifier (e.g., translation, script, or recitation). The editionIdentifier (e.g., 'ar.abdulbasitmurattal.hafs') must be provided as a path parameter, not as a query parameter. Useful for retrieving a chapter in a particular format or language.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a Surah in a specific edition (translation, script, or recitation) for display or comparison.",
        "x-mcp-example": {"surahNumber": 1, "editionIdentifier": "en.sahih", "limit": 7, "offset": 0}
    }
)
async def get_the_surah_by_edition(
    surahNumber: int = Path(..., ge=1, le=114, description="Surah number (1-114)"),
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'ar.abdulbasitmurattal.hafs') as a required path parameter, not a query parameter.", example="quran-uthmani"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a surah by the given number.", example=0)
):
    try:
        if surahNumber < 1 or surahNumber > 114:
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Surah number must be between 1 and 114."},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        data = await surah_repo.get_surah(surahNumber, editionIdentifier, limit, offset)
        if isinstance(data, str):
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_duration=2592000, browser_cache=3600, cache_tag=f"surah-{surahNumber},edition-{editionIdentifier}")
        return response
    except Exception as e:
        logger.exception("An exception occurred while fetching surah number %d and edition %s: %s", surahNumber, editionIdentifier, str(e))
        error_response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        error_response.headers["Cache-Control"] = "no-store"
        return error_response


@surah_router.get(
    "/{surahNumber}/editions/{editionIdentifiers}",
    responses=getTheSurahbyEditionsResponse,
    tags=["Surah"],
    name="Get a Surah by Number and Multiple Editions",
    description="Get a specific Surah by number from multiple editions (comma-separated). Useful for comparing translations, scripts, or recitations side by side.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a Surah in multiple editions for comparison or multilingual display.",
        "x-mcp-example": {"surahNumber": 1, "editionIdentifiers": "quran-uthmani,en.sahih", "limit": 7, "offset": 0}
    }
)
async def get_the_surah_by_editions(
    surahNumber: int = Path(..., ge=1, le=114, description="Surah number (1-114)"),
    editionIdentifiers: str = Path(..., description="Comma-separated edition identifiers (e.g., 'quran-uthmani,en.sahih')", example="quran-uthmani,quran-simple-clean"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a surah by the given number.", example=0)
):
    try:
        if surahNumber < 1 or surahNumber > 114:
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Surah number must be between 1 and 114."},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        edition_list = editionIdentifiers.split(',')
        data = await surah_repo.get_surah_by_multiple_editions(surahNumber, edition_list, limit, offset)
        if isinstance(data, str):
            error_response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            error_response.headers["Cache-Control"] = "no-store"
            return error_response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_duration=2592000, browser_cache=3600, cache_tag=f"surah-{surahNumber},editions-{editionIdentifiers}")
        return response
    except Exception as e:
        logger.exception("An exception occurred while fetching surah number %d and editions %s: %s", surahNumber, editionIdentifiers, str(e))
        error_response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        error_response.headers["Cache-Control"] = "no-store"
        return error_response
