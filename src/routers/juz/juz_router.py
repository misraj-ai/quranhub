from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import juz_repo  # Using the repository now
from .juz_docs import (
getTheJuzbyEditionResponse,
getTheJuzResponse,
getAllJuzsMetadataResponse,
getAllJuzsMetadataByEditionResponse
)
from utils.logger import logger 
from utils.config import DEFAULT_EDITION_IDENTIFIER

juz_router = APIRouter()


@juz_router.get(
    "/metadata",
    responses=getAllJuzsMetadataResponse,
    tags=["Juz"],
    name="Get All Juzs Metadata",
    description="Get metadata for all 30 Juzs (sections) of the Quran, including first/last ayah, surah, page, and ayah count. Useful for navigation, study, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve metadata for all Juzs for navigation, study, or to display section structure.",
        "x-mcp-example": {}
    }
)
async def get_all_juzs_metadata():
    try:
        data = await juz_repo.get_all_juzs()

        if isinstance(data, str):
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching all juzs metadata: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

@juz_router.get(
    "/metadata/{editionIdentifier}",
    responses=getAllJuzsMetadataByEditionResponse,
    tags=["Juz"],
    name="Get All Juzs Metadata by Edition",
    description="Get metadata for all 30 Juzs from a specific edition. The editionIdentifier (e.g., 'quran-uthmani') must be provided as a path parameter, not as a query parameter. Includes first/last ayah, surah, page, ayah count, and edition details. Useful for edition-specific navigation and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to retrieve Juz metadata for a specific edition for navigation or display.",
        "x-mcp-example": {"editionIdentifier": "quran-uthmani"}
    }
)
async def get_all_juzs_metadata_by_edition(
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani') as a required path parameter, not a query parameter.", example="quran-uthmani")
):
    try:
        data = await juz_repo.get_all_juzs(editionIdentifier)

        if isinstance(data, str):
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching all juzs metadata for edition %s: %s", editionIdentifier, str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

@juz_router.get(
    "/{juzNumber}",
    tags=["Juz"],
    responses=getTheJuzResponse,
    name="Get a Juz by Number",
    description="Get a specific Juz (section) by its number (1-30) from the default edition, including all ayahs and metadata. Useful for navigation, study, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a single Juz by number for display, navigation, or LLM context.",
        "x-mcp-example": {"juzNumber": 1, "limit": 100, "offset": 0}
    }
)
async def get_the_juz(
    juzNumber: int = Path(..., ge=1, le=30, description="Juz number (1-30)"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a juz by the given number.", example=0)
):
    try:
        if juzNumber < 1 or juzNumber > 30:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Juz number must be between 1 and 30."},
                status_code=400
            )

        data = await juz_repo.get_juz(juzNumber, DEFAULT_EDITION_IDENTIFIER, limit, offset)

        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching juz number %d: %s", juzNumber, str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )


@juz_router.get(
    "/{juzNumber}/{editionIdentifier}",
    responses=getTheJuzbyEditionResponse,
    tags=["Juz"],
    name="Get a Juz by Number and Edition",
    description="Get a specific Juz (section) by number from a particular edition, including all ayahs and metadata. Useful for edition-specific navigation, study, and LLM workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to fetch a Juz by number and edition for display, navigation, or LLM context.",
        "x-mcp-example": {"juzNumber": 1, "editionIdentifier": "quran-uthmani", "limit": 100, "offset": 0}
    }
)
async def get_the_juz_by_edition(
    juzNumber: int = Path(..., ge=1, le=30, description="Juz number (1-30)"),
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'quran-uthmani')", example="quran-uthmani"),
    limit: int = Query(None, description="Limit the number of ayahs returned.", example=2000),
    offset: int = Query(None, description="Offset ayahs in a juz by the given number.", example=0)
):
    try:
        if juzNumber < 1 or juzNumber > 30:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Juz number must be between 1 and 30."},
                status_code=400
            )

        data = await juz_repo.get_juz(juzNumber, editionIdentifier, limit, offset)

        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something went wrong: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching juz number %d for edition %s: %s", juzNumber, editionIdentifier, str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

