from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import page_repo  # Using the repository now
from .page_docs import (
    getPagebyNumberResponse,
    getPagebyEditionResponse,
    getAllPagesMetadataResponse,
    getAllPagesMetadataByEditionResponse
)
from utils.logger import logger
from utils.helpers import add_cache_headers
from utils.config import DEFAULT_EDITION_IDENTIFIER

page_router = APIRouter()

# Add after the router definition and before existing routes

@page_router.get(
    "/metadata",
    responses=getAllPagesMetadataResponse,
    tags=["Page"],
    name="Get All Pages Metadata",
    description="Get metadata for all 604 Quran pages, including the first ayah, first surah, and hizb numbers for each page. Useful for navigation, search, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve metadata for all Quran pages for navigation, search, or to display page structure.",
        "x-mcp-example": {}
    }
)
async def get_all_pages_metadata():
    try:
        data = await page_repo.get_all_pages()

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
        add_cache_headers(response, cache_tag="page:metadata:all")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching all pages metadata: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

@page_router.get(
    "/metadata/{editionIdentifier}",
    responses=getAllPagesMetadataByEditionResponse,
    tags=["Page"],
    name="Get All Pages Metadata by Edition",
    description="Get metadata for all 604 Quran pages from a specific edition. The editionIdentifier (e.g., 'quran-uthmani') must be provided as a path parameter, not as a query parameter. Includes the first ayah, first surah, hizb numbers, and edition details. Useful for edition-specific navigation and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve page metadata for a specific edition for navigation or display.",
        "x-mcp-example": {"editionIdentifier": "quran-uthmani"}
    }
)
async def get_all_pages_metadata_by_edition(
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani') as a required path parameter, not a query parameter.", example="quran-uthmani")
):
    try:
        data = await page_repo.get_all_pages(editionIdentifier)

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
        add_cache_headers(response, cache_tag=f"page:metadata:edition:{editionIdentifier}")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching all pages metadata for edition %s: %s", editionIdentifier, str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

# ...existing routes...
 # Cache for 1 day
@page_router.get(
    "/{pageNumber}",
    responses=getPagebyNumberResponse,
    tags=["Page"],
    name="Get Page By Number",
    description="Get a specific Quran page (1-604) from the default edition, including all ayahs and metadata. Optionally include word breakdowns. Useful for page navigation, display, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a single Quran page by number for display, navigation, or LLM context.",
        "x-mcp-example": {"pageNumber": 1, "words": False, "limit": 7, "offset": 0}
    }
)
async def get_page_by_number(
    pageNumber: int = Path(..., ge=1, le=604, description="Page number (1-604)"),
    words: bool = Query(False, description="Include word breakdowns for each ayah."),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a page by the given number.", example=0)
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

        # Fetch page data
        data = await page_repo.get_page(pageNumber, DEFAULT_EDITION_IDENTIFIER, words, limit, offset)

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
        add_cache_headers(response, cache_tag=f"page:number:{pageNumber}")
        return response

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
    

 # Cache for 1 day
@page_router.get(
    "/{pageNumber}/{editionIdentifier}",
    responses=getPagebyEditionResponse,
    tags=["Page"],
    name="Get Page By Number and Edition",
    description="Get a specific Quran page (1-604) from a particular edition, including all ayahs and metadata. Optionally include word breakdowns. Useful for edition-specific navigation, display, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a Quran page by number and edition for display, navigation, or LLM context.",
        "x-mcp-example": {"pageNumber": 1, "editionIdentifier": "quran-uthmani", "words": False, "limit": 7, "offset": 0}
    }
)
async def get_page_by_edition(
    pageNumber: int = Path(..., ge=1, le=604, description="Page number (1-604)"),
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani')", example="quran-uthmani"),
    words: bool = Query(False, description="Include word breakdowns for each ayah."),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a page by the given number.", example=0)
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

        # Fetch page data from the specified edition
        data = await page_repo.get_page(pageNumber, editionIdentifier, words, limit, offset)

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
        add_cache_headers(response, cache_tag=f"page:number:{pageNumber}:edition:{editionIdentifier}")
        return response

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
