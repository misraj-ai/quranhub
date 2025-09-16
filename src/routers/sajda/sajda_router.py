from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import sajda_repo  # Using the repository now
from .sajda_docs import (
getSajdabyEditionResponse,
getAllSajdaResponse

)
from utils.logger import logger 
from utils.config import DEFAULT_EDITION_IDENTIFIER

sajda_router = APIRouter()

  # Cache for 1 day
@sajda_router.get(
    "/",
    responses=getAllSajdaResponse,
    tags=["Sajda"],
    name="Get All Sajdas",
    description="Get all ayahs (verses) in the Quran that require Sajda (prostration), including their metadata and sajda type. Useful for study, navigation, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve all Sajda ayahs for display, study, or LLM context.",
        "x-mcp-example": {}
    }
)
async def get_all_sajda():
    try:
        # Fetch all sajdas
        data = await sajda_repo.get_sajdas(DEFAULT_EDITION_IDENTIFIER)

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
@sajda_router.get(
    "/{editionIdentifier}",
    responses=getSajdabyEditionResponse,
    tags=["Sajda"],
    name="Get All Sajdas by Edition",
    description="Get all ayahs (verses) requiring Sajda from a particular edition, including their metadata and sajda type. Useful for edition-specific study, navigation, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve all Sajda ayahs for a specific edition for display, study, or LLM context.",
        "x-mcp-example": {"editionIdentifier": "quran-uthmani"}
    }
)
async def get_sajda_by_edition(
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani')", example="quran-uthmani")
):
    try:
        # Fetch sajdas by edition
        data = await sajda_repo.get_sajdas(editionIdentifier)

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