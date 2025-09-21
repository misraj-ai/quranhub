from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import narrations_differences_repo  # Using the repository now
from .narrations_differences_docs import (
getNarrationsDifferencesByPageResponse
)

from utils.logger import logger
from utils.helpers import add_cache_headers

narrations_differences_router = APIRouter()

  # Cache for 1 day
@narrations_differences_router.get(
    "/",
    responses=getNarrationsDifferencesByPageResponse,
    tags=["Narrations Differences"],
    name="Get Narrations Differences By Page Number and Narrations Identifiers",
    description=(
        'Get a comprehensive comparison of different Quranic narrations (Hafs, Warsh, Qaloon, etc.) for a given page, showing textual differences with precise word-level positioning, audio recitation URLs, and detailed scholarly commentary. Useful for advanced study, LLMs, and agent workflows.'
    ),
    openapi_extra={
        "x-agent-hints": "Use this endpoint to compare narrations for a given page, with word-level differences, audio, and scholarly commentary. Specify source and target narration identifiers.",
        "x-mcp-example": {
            "pageNumber": 1,
            "sourceNarrationEditionIdentifier": "quran-hafs",
            "targetNarrationsEditionsIdentifiers": "quran-warsh,quran-qunbul"
        }
    }
)
async def get_narrations_differences_by_page(
    pageNumber: int = Query(..., ge=1, le=604, description="Page number (1-604)"),
    sourceNarrationEditionIdentifier: str = Query(..., description="Source narration identifier (e.g., 'quran-hafs')", example="quran-hafs"),
    targetNarrationsEditionsIdentifiers: str = Query(
        ..., 
        description="Comma-separated target narration identifiers (e.g., 'quran-warsh,quran-qunbul')", 
        example="quran-warsh,quran-qunbul,quran-qaloon"
    )
):
    try:
        # Validate pageNumber range
        if pageNumber < 1 or pageNumber > 604:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Page number should be between 1 and 604"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Parse and clean the target narrations edition identifiers
        editionIdentifiersList = targetNarrationsEditionsIdentifiers.split(',') if ',' in targetNarrationsEditionsIdentifiers else [targetNarrationsEditionsIdentifiers]
        editionIdentifiersList = list(set(editionIdentifiersList))  # Remove duplicates
        
        # Ensure source narration is not in the target list
        if sourceNarrationEditionIdentifier in editionIdentifiersList:
            editionIdentifiersList.remove(sourceNarrationEditionIdentifier)
            if not editionIdentifiersList:  # If no target editions remain
                response = JSONResponse(
                    content={"code": 400, "status": "Error", "data": "Source narration should be different from target narration"},
                    status_code=400
                )
                response.headers["Cache-Control"] = "no-store"
                return response
        
        # Fetch narrations differences
        data = await narrations_differences_repo.get_narrations_differences(
            pageNumber, sourceNarrationEditionIdentifier, editionIdentifiersList
        )

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
        add_cache_headers(
            response,
            cache_tag=f"narrations_differences:page:{pageNumber}:source:{sourceNarrationEditionIdentifier}:targets:{'-'.join(sorted(editionIdentifiersList))}"
        )
        return response

    except Exception as e:
        logger.error("An exception occurred: %s", str(e), exc_info=True)
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong: "},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response
