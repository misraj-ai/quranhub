from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import quran_repo  # Using the repository now
from .quran_docs import (
getTheQuranbyEditionResponse,
getTheQuranResponse

)
from utils.logger import logger
from utils.helpers import add_cache_headers
from utils.config import DEFAULT_EDITION_IDENTIFIER

quran_router = APIRouter()


@quran_router.get(
    "/",
    responses=getTheQuranResponse,
    tags=["Quran"],
    name="Get Complete Quran",
    summary="Get the complete Quran (default edition)",
    description="Returns the complete Quran in the default edition. Use this to retrieve all surahs and ayahs for display, analysis, or further processing. The response includes all Quranic text and metadata.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to retrieve the entire Quran in the default edition. Use the returned surah and ayah data for navigation, search, or to fetch specific ayahs or surahs in later steps.",
        "x-mcp-example": {
            "name": "get_complete_quran_v1_quran__get",
            "arguments": {}
        }
    }
)
async def get_the_quran():
    try:
        data = await quran_repo.get_quran(DEFAULT_EDITION_IDENTIFIER)

        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_tag="quran:all:default")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching the Quran: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )


@quran_router.get(
    "/{editionIdentifier}",
    responses=getTheQuranbyEditionResponse,
    tags=["Quran"],
    name="Get Complete Quran by Edition",
    summary="Get the complete Quran by edition",
    description="Returns the complete Quran for a specified edition. Use this to retrieve all surahs and ayahs in a particular text or translation edition. The response includes all Quranic text and metadata for the chosen edition.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to retrieve the entire Quran in a specific edition (e.g., translation or script). Use the editionIdentifier to select the desired edition, and use the returned data for navigation, search, or further processing.",
        "x-mcp-example": {
            "name": "get_complete_quran_by_edition_v1_quran_editionIdentifier_get",
            "arguments": {"editionIdentifier": "quran-uthmani"}
        }
    }
)
async def get_the_quran_by_edition(editionIdentifier: str = Path(..., description="A valid edition identifier for the edition", example="quran-uthmani")):
    try:
        data = await quran_repo.get_quran(editionIdentifier)

        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_tag=f"quran:all:edition:{editionIdentifier}")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching the Quran for edition %s: %s", editionIdentifier, str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
