
from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse
from utils.helpers import add_cache_headers

from repositories import hizb_repo  # Using the repository now
from .hizb_docs import (
getHizbbyNumberResponse,
getHizbbyEditionResponse,
getAllHizbsMetadataResponse,
getAllHizbsMetadataByEditionResponse
)
from utils.logger import logger 
from utils.config import DEFAULT_EDITION_IDENTIFIER

hizb_router = APIRouter()

@hizb_router.get(
    "/metadata",
    tags=["Hizb"],
    name="Get All Hizbs Metadata",
    summary="Get metadata for all Hizbs",
    description="Returns metadata for all 60 Hizbs of the Quran, including their first page, first ayah, and first surah. Use this to understand the structure and navigation of Hizbs.",
    responses=getAllHizbsMetadataResponse,
    openapi_extra={
        "x-agent-hints": "Call this endpoint to retrieve metadata for all Hizbs. Use the returned numbers and references to fetch specific Hizb content or for navigation.",
        "x-mcp-example": {
            "name": "get_all_hizbs_metadata_v1_hizb_metadata_get",
            "arguments": {}
        }
    }
)
async def get_all_hizbs_metadata():
    try:
        data = await hizb_repo.get_all_hizbs()

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
        add_cache_headers(response, cache_tag="hizb:all:metadata")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching all hizbs metadata: %s", str(e))
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response

@hizb_router.get(
    "/metadata/{editionIdentifier}",
    tags=["Hizb"],
    name="Get All Hizbs Metadata by Edition",
    summary="Get metadata for all Hizbs by edition",
    description="Returns metadata for all Hizbs from a specific edition. The editionIdentifier (e.g., 'quran-uthmani') must be provided as a path parameter, not as a query parameter. Use this to understand the structure and navigation of Hizbs in a particular edition.",
    responses=getAllHizbsMetadataByEditionResponse,
    openapi_extra={
        "x-agent-hints": "Call this endpoint to retrieve metadata for all Hizbs in a specific edition. Use the editionIdentifier to select the edition and returned references for navigation.",
        "x-mcp-example": {
            "name": "get_all_hizbs_metadata_by_edition_v1_hizb_metadata_editionIdentifier_get",
            "arguments": {"editionIdentifier": "quran-uthmani"}
        }
    }
)
async def get_all_hizbs_metadata_by_edition(
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani') as a required path parameter, not a query parameter.", example="quran-uthmani")
):
    try:
        data = await hizb_repo.get_all_hizbs(editionIdentifier)

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
        add_cache_headers(response, cache_tag=f"hizb:all:metadata:edition:{editionIdentifier}")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching all hizbs metadata for edition %s: %s", editionIdentifier, str(e))
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response

# ...existing routes...

  # Cache for 1 day
@hizb_router.get(
    "/{hizbNumber}",
    responses=getHizbbyNumberResponse,
    tags=["Hizb"],
    name="Get Hizb By Number",
    summary="Get Hizb by number",
    description="Returns the requested Hizb based on the Hizb number (1-60). Use this to fetch the content of a specific Hizb for display or analysis.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to fetch the content of a specific Hizb by its number. Use the returned data for display, navigation, or further processing.",
        "x-mcp-example": {
            "name": "get_hizb_by_number_v1_hizb_hizbNumber_get",
            "arguments": {"hizbNumber": 1, "limit": 2000, "offset": 0}
        }
    }
)
async def get_hizb_by_number(
    hizbNumber: int = Path(..., ge=1, le=60, description="An integer between 1 and 60"),
    limit: int = Query(None, description="The number of ayahs that the response will be limited to.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a hizb by the given number", example=0)
):
    try:
        # Validate hizbNumber range
        if hizbNumber < 1 or hizbNumber > 60:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Hizb number should be between 1 and 60"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        # Fetch hizb data
        data = await hizb_repo.get_hizb(hizbNumber, DEFAULT_EDITION_IDENTIFIER, limit, offset)

        # Check if data is an error message (string)
        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Something went wrong: " + data},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        # Return successful response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_tag=f"hizb:{hizbNumber}")
        return response

    except Exception as e:
        logger.error("An exception occurred: %s", str(e), exc_info=True)
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response
    

  # Cache for 1 day
@hizb_router.get(
    "/{hizbNumber}/{editionIdentifier}",
    responses=getHizbbyEditionResponse,
    tags=["Hizb"],
    name="Get Hizb By Number and Edition",
    summary="Get Hizb by number and edition",
    description="Returns the requested Hizb from a particular edition. Use this to fetch the content of a specific Hizb in a specific edition for display or analysis.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to fetch the content of a specific Hizb by its number and edition. Use the returned data for display, navigation, or further processing.",
        "x-mcp-example": {
            "name": "get_hizb_by_number_and_edition_v1_hizb_hizbNumber_editionIdentifier_get",
            "arguments": {"hizbNumber": 1, "editionIdentifier": "quran-uthmani", "limit": 2000, "offset": 0}
        }
    }
)
async def get_hizb_by_edition(
    hizbNumber: int = Path(..., ge=1, le=60, description="An integer between 1 and 60"),
    editionIdentifier: str = Path(..., description="A valid edition identifier for edition", example="quran-uthmani"),
    limit: int = Query(None, description="The number of ayahs that the response will be limited to.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a hizb by the given number", example=0)
):
    try:
        # Validate hizbNumber range
        if hizbNumber < 1 or hizbNumber > 60:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Hizb number should be between 1 and 60"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        # Fetch hizb data for a specific edition
        data = await hizb_repo.get_hizb(hizbNumber, editionIdentifier, limit, offset)

        # Check if data is an error message (string)
        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Something went wrong: " + data},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        # Return successful response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_tag=f"hizb:{hizbNumber}:edition:{editionIdentifier}")
        return response

    except Exception as e:
        logger.error("An exception occurred: %s", str(e), exc_info=True)
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response
