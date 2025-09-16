from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import manzil_repo  # Using the repository now
from .manzil_docs import (
    getManzilbyEditionResponse,
    getManzilbyNumberResponse
)
from utils.logger import logger 
from utils.config import DEFAULT_EDITION_IDENTIFIER
manzil_router = APIRouter()

  # Cache for 1 day
@manzil_router.get(
    "/{manzilNumber}",
    responses=getManzilbyNumberResponse,
    tags=["Manzil"],
    name="Get Manzil by Number",
    description="Get a specific Manzil (one of 7 weekly sections) by its number (1-7) from the default edition, including all ayahs and metadata. Useful for weekly reading plans, navigation, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a single Manzil by number for display, navigation, or LLM context.",
        "x-mcp-example": {"manzilNumber": 1, "limit": 100, "offset": 0}
    }
)
async def get_manzil_by_number(
    manzilNumber: int = Path(..., ge=1, le=7, description="Manzil number (1-7)"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a manzil by the given number.", example=0)
):
    try:
        # Validation (although Path already does ge/le, but you want extra safety log)
        if manzilNumber < 1 or manzilNumber > 7:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Manzil number should be between 1 and 7"},
                status_code=400
            )

        # Fetch manzil data
        data = await manzil_repo.get_manzil(manzilNumber, DEFAULT_EDITION_IDENTIFIER, limit, offset)

        # Check if data retrieval failed
        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Something went wrong: " + data},
                status_code=400
            )

        # Success response
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
@manzil_router.get(
    "/{manzilNumber}/{editionIdentifier}",
    responses=getManzilbyEditionResponse,
    tags=["Manzil"],
    name="Get Manzil by Number and Edition",
    description="Get a specific Manzil (one of 7 weekly sections) by number from a particular edition, including all ayahs and metadata. Useful for edition-specific weekly reading, navigation, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a Manzil by number and edition for display, navigation, or LLM context.",
        "x-mcp-example": {"manzilNumber": 1, "editionIdentifier": "quran-uthmani", "limit": 100, "offset": 0}
    }
)
async def get_manzil_by_edition(
    manzilNumber: int = Path(..., ge=1, le=7, description="Manzil number (1-7)"),
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani')", example="quran-uthmani"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a manzil by the given number.", example=0)
):
    try:
        # Manual Validation
        if manzilNumber < 1 or manzilNumber > 7:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Manzil number should be between 1 and 7"},
                status_code=400
            )

        # Fetch Manzil by Edition
        data = await manzil_repo.get_manzil(manzilNumber, editionIdentifier, limit, offset)

        # Check for error
        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Something went wrong: " + data},
                status_code=400
            )

        # Success Response
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