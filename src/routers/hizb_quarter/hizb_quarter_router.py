from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import hizb_quarter_repo  # Using the repository now
from .hizb_quarter_docs import (
getHizbQuarterbyEditionResponse,
getHizbQuarterbyNumberResponse
)
from utils.logger import logger 
from utils.config import DEFAULT_EDITION_IDENTIFIER

hizb_quarter_router = APIRouter()

  # Cache for 1 day
@hizb_quarter_router.get(
    "/{hizbQuarterNumber}",
    responses=getHizbQuarterbyNumberResponse,
    tags=["HizbQuarter"],
    name="Get Hizb Quarter By Number",
    summary="Get Hizb Quarter by number",
    description="Returns the requested Hizb Quarter by its number (1-240). Use this to fetch the content of a specific Hizb Quarter for display or analysis.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to fetch the content of a specific Hizb Quarter by its number. Use the returned data for display, navigation, or further processing.",
        "x-mcp-example": {
            "name": "get_hizb_quarter_by_number_v1_hizb_quarter_hizbQuarterNumber_get",
            "arguments": {"hizbQuarterNumber": 240, "limit": 2000, "offset": 0}
        }
    }
)
async def get_hizb_quarter_by_number(
    hizbQuarterNumber: int = Path(..., ge=1, le=240, description="An integer between 1 and 240"),
    limit: int = Query(None, description="The number of ayahs that the response will be limited to.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a hizb quarter by the given number", example=0)
):
    try:
        # Validate hizbQuarterNumber range
        if hizbQuarterNumber < 1 or hizbQuarterNumber > 240:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "HizbQuarter number should be between 1 and 240"},
                status_code=400
            )

        # Fetch hizb quarter data
        data = await hizb_quarter_repo.get_hizb_quarter(hizbQuarterNumber, DEFAULT_EDITION_IDENTIFIER, limit, offset)

        # Check if data is an error message (string)
        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Something went wrong: " + data},
                status_code=400
            )

        # Return successful response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception as e:
        logger.error("An exception occurred: %s", str(e), exc_info=True)
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
    
  # Cache for 1 day
@hizb_quarter_router.get(
    "/{hizbQuarterNumber}/{editionIdentifier}",
    responses=getHizbQuarterbyEditionResponse,
    tags=["HizbQuarter"],
    name="Get Hizb Quarter By Number and Edition",
    summary="Get Hizb Quarter by number and edition",
    description="Returns the requested Hizb Quarter from a particular edition. Use this to fetch the content of a specific Hizb Quarter in a specific edition for display or analysis.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to fetch the content of a specific Hizb Quarter by its number and edition. Use the returned data for display, navigation, or further processing.",
        "x-mcp-example": {
            "name": "get_hizb_quarter_by_number_and_edition_v1_hizb_quarter_hizbQuarterNumber_editionIdentifier_get",
            "arguments": {"hizbQuarterNumber": 240, "editionIdentifier": "quran-uthmani", "limit": 2000, "offset": 0}
        }
    }
)
async def get_hizb_quarter_by_edition(
    hizbQuarterNumber: int = Path(..., ge=1, le=240, description="An integer between 1 and 240"),
    editionIdentifier: str = Path(..., description="A valid edition identifier for edition", example="quran-uthmani"),
    limit: int = Query(None, description="The number of ayahs that the response will be limited to.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a hizb quarter by the given number", example=0)
):
    try:
        # Validate hizbQuarterNumber range
        if hizbQuarterNumber < 1 or hizbQuarterNumber > 240:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "HizbQuarter number should be between 1 and 240"},
                status_code=400
            )

        # Fetch hizb quarter data
        data = await hizb_quarter_repo.get_hizb_quarter(hizbQuarterNumber, editionIdentifier, limit, offset)

        # Check if data is an error message (string)
        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Something went wrong: " + data},
                status_code=400
            )

        # Return successful response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception as e:
        logger.error("An exception occurred: %s", str(e), exc_info=True)
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )