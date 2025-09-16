from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import ruku_repo  # Using the repository now
from .ruku_docs import (
    getRukubyNumberResponse,
    getRukubyEditionResponse
)
from utils.logger import logger 
from utils.config import DEFAULT_EDITION_IDENTIFIER

ruku_router = APIRouter()

  # Cache for 1 day
@ruku_router.get(
    "/{rukuNumber}",
    responses=getRukubyNumberResponse,
    tags=["Ruku"],
    name="Get Ruku By Number",
    description="Get a specific Ruku (section) by its number (1-556) from the default edition, including all ayahs and metadata. Useful for navigation, study, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a single Ruku by number for display, navigation, or LLM context.",
        "x-mcp-example": {"rukuNumber": 1, "limit": 7, "offset": 0}
    }
)
async def get_ruku_by_number(
    rukuNumber: int = Path(..., ge=1, le=556, description="Ruku number (1-556)"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a ruku by the given number.", example=0)
):
    try:
        # Validate rukuNumber range
        if rukuNumber < 1 or rukuNumber > 556:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Ruku number should be between 1 and 556"},
                status_code=400
            )

        # Fetch ruku data
        data = await ruku_repo.get_ruku(rukuNumber, DEFAULT_EDITION_IDENTIFIER, limit, offset)
        
        # Check if data is an error message (string)
        if isinstance(data, str):
            logger.error("Something went wrong: %s", data)
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
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

  # Cache for 1 day
@ruku_router.get(
    "/{rukuNumber}/{editionIdentifier}",
    responses=getRukubyEditionResponse,
    tags=["Ruku"],
    name="Get Ruku By Number and Edition",
    description="Get a specific Ruku (section) by number from a particular edition, including all ayahs and metadata. Useful for edition-specific navigation, study, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a Ruku by number and edition for display, navigation, or LLM context.",
        "x-mcp-example": {"rukuNumber": 1, "editionIdentifier": "quran-uthmani", "limit": 7, "offset": 0}
    }
)
async def get_ruku_by_edition(
    rukuNumber: int = Path(..., ge=1, le=556, description="Ruku number (1-556)"),
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani')", example="quran-uthmani"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a ruku by the given number.", example=0)
):
    try:
        # Validate rukuNumber range
        if rukuNumber < 1 or rukuNumber > 556:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Ruku number should be between 1 and 556"},
                status_code=400
            )

        # Fetch ruku data
        data = await ruku_repo.get_ruku(rukuNumber, editionIdentifier, limit, offset)

        # Check if data is an error message (string)
        if isinstance(data, str):
            logger.error("Something went wrong: %s", data)
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
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
