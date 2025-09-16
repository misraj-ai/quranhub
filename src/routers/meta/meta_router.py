from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import meta_repo  # Using the repository now
from .meta_docs import (
getAllMetaResponse
)
from utils.logger import logger 

meta_router = APIRouter()

  # Cache for 1 day
@meta_router.get(
    "/",
    responses=getAllMetaResponse,
    tags=["Meta"],
    name="Get all meta data about Qur'an",
    summary="Get all meta data about the Qur'an",
    description="Returns all available meta data about the Qur'an, including ayahs, surahs, sajdas, rukus, pages, manzils, hizbquarters, and juzs. Use this to understand the structure and references for navigation or analysis.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to retrieve all meta data about the Qur'an. Use the returned references and counts to guide navigation, search, or to fetch specific resources in later steps.",
        "x-mcp-example": {
            "name": "get_all_meta_v1_meta__get",
            "arguments": {}
        }
    }
)
async def get_all_meta():
    try:
        # Fetch meta data
        data = await meta_repo.get_meta()

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