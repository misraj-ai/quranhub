

from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse
from utils.helpers import add_cache_headers

# Constants for repeated strings
ERROR_SOMETHING_WRONG = "Something went wrong"
ERROR_INVALID_REFERENCE = "Invalid reference format."
CACHE_NO_STORE = "no-store"
CACHE_NO_CACHE = "no-cache, no-store, must-revalidate"

import random
from repositories import ayah_repo  # Using the repository now
from .ayah_docs import (
getTheAyahbyEditionsResponse,
getTheAyahbyEditionResponse,
getTheAyahResponse,
getRandomAyahbyEditionsResponse,
getRandomAyahbyEditionResponse,
getRandomAyahResponse
)
from utils.logger import logger 
from utils.config import DEFAULT_EDITION_IDENTIFIER

ayah_router = APIRouter()


@ayah_router.get(
    "/random",
    responses=getRandomAyahResponse,
    tags=["Ayah"],
    name="Get Random Ayah",
    summary="Get a random ayah",
    description="Returns a random ayah from the Quran in the default edition. Use this to discover or display a random verse, or as a starting point for further exploration.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get a random ayah. Use the 'reference' or 'number' field in the response to fetch its translation, audio, or related metadata using other endpoints.",
        "x-mcp-example": {
            "name": "get_random_ayah_v1_ayah_random_get",
            "arguments": {}
        }
    }
)
async def get_random_ayah():
    try:
        random_number = random.randint(1, 6236)
        data = await ayah_repo.get_an_ayah(random_number, DEFAULT_EDITION_IDENTIFIER)

        if isinstance(data, str):
            logger.error("Error fetching random ayah: %s", data)
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        # Random endpoint: no cache
        response.headers["Cache-Control"] = CACHE_NO_CACHE
        return response

    except Exception:
        logger.exception("Unexpected error fetching random ayah")
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": ERROR_SOMETHING_WRONG},
            status_code=400
        )
        response.headers["Cache-Control"] = CACHE_NO_STORE
        return response
    

@ayah_router.get(
    "/random/{editionIdentifier}",
    responses=getRandomAyahbyEditionResponse,
    tags=["Ayah"],
    name="Get Random Ayah by Edition",
    summary="Get a random ayah by edition",
    description="Returns a random ayah from the Quran in the specified edition. The editionIdentifier (e.g., 'ar.abdulbasitmurattal.hafs') must be provided as a path parameter, not as a query parameter. Use this to discover a random verse in a particular translation or script.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get a random ayah in a specific edition. Use the 'editionIdentifier' parameter to select the edition, and use the response to fetch related resources.",
        "x-mcp-example": {
            "name": "get_random_ayah_by_edition_v1_ayah_random_editionIdentifier_get",
            "arguments": {"editionIdentifier": "quran-uthmani"}
        }
    }
)
async def get_random_ayah_by_edition(
    editionIdentifier: str = Path(..., description="Edition identifier (e.g., 'ar.abdulbasitmurattal.hafs') as a required path parameter, not a query parameter.", example="quran-uthmani")
):
    try:
        random_number = random.randint(1, 6236)
        data = await ayah_repo.get_an_ayah(random_number, editionIdentifier)

        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        # Random endpoint: no cache
        response.headers["Cache-Control"] = CACHE_NO_CACHE
        return response

    except Exception:
        logger.exception("Unexpected error fetching random ayah by edition")
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": ERROR_SOMETHING_WRONG},
            status_code=400
        )
        response.headers["Cache-Control"] = CACHE_NO_STORE
        return response
    

@ayah_router.get(
    "/random/editions/{editionIdentifiers}",
    responses=getRandomAyahbyEditionsResponse,
    tags=["Ayah"],
    name="Get Random Ayah by Multiple Editions",
    summary="Get a random ayah by multiple editions",
    description="Returns a random ayah from the Quran in multiple specified editions. Use this to compare a random verse across different translations or scripts.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get a random ayah in multiple editions. Provide a comma-separated list of edition identifiers, and use the response to compare translations or scripts.",
        "x-mcp-example": {
            "name": "get_random_ayah_by_editions_v1_ayah_random_editions_editionIdentifiers_get",
            "arguments": {"editionIdentifiers": "quran-uthmani,quran-simple-clean"}
        }
    }
)
async def get_random_ayah_by_editions(
    editionIdentifiers: str = Path(..., description="Valid edition identifiers, separated by commas", example="quran-uthmani,quran-simple-clean")
):
    try:
        random_number = random.randint(1, 6236)
        editionIdentifiers_list = editionIdentifiers.split(',')

        if not editionIdentifiers_list:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "At least one valid edition identifier must be provided."},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        data = await ayah_repo.get_an_ayah_by_multiple_editions(random_number, editionIdentifiers_list)

        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        # Random endpoint: no cache
        response.headers["Cache-Control"] = CACHE_NO_CACHE
        return response

    except Exception:
        logger.exception("Unexpected error fetching random ayah for multiple editions")
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": ERROR_SOMETHING_WRONG},
            status_code=400
        )
        response.headers["Cache-Control"] = CACHE_NO_STORE
        return response
    

@ayah_router.get(
    "/{reference}",
    responses=getTheAyahResponse,
    tags=["Ayah"],
    name="Get Ayah by Number or Number in Surah",
    summary="Get ayah by reference (number or surah:ayah)",
    description="Returns an ayah by its global number or by surah:ayah format (e.g., 2:255). Use this to fetch a specific verse for display, analysis, or further processing.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to fetch a specific ayah by its global number or surah:ayah reference. Use the response to display the verse or to fetch related resources.",
        "x-mcp-example": {
            "name": "get_ayah_by_reference_v1_ayah_reference_get",
            "arguments": {"reference": "2:255"}
        }
    }
)
async def get_the_ayah(
    reference: str = Path(..., description="Reference can be global ayah number or surah:ayah format", example="2:255")
):
    try:
        if ":" in reference:
            ayah_number_list = reference.split(":")
            data = await ayah_repo.get_an_ayah_by_surah_number(
                int(ayah_number_list[0]),
                int(ayah_number_list[1]),
                DEFAULT_EDITION_IDENTIFIER
            )
        elif reference.isdigit():
            data = await ayah_repo.get_an_ayah(int(reference), DEFAULT_EDITION_IDENTIFIER)
        else:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": ERROR_INVALID_REFERENCE},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        # Static ayah: cache for 30 days, tag by ayah
        add_cache_headers(response, cache_tag=f"ayah:{reference}")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching ayah. Reference: %s", e)
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": ERROR_SOMETHING_WRONG},
            status_code=400
        )
        response.headers["Cache-Control"] = CACHE_NO_STORE
        return response
    

@ayah_router.get(
    "/{reference}/{editionIdentifier}",
    responses=getTheAyahbyEditionResponse,
    tags=["Ayah"],
    name="Get Ayah by Number or Number in Surah and Edition",
    summary="Get ayah by reference and edition",
    description="Returns an ayah by its global number or surah:ayah format for a specified edition. Use this to fetch a specific verse in a particular translation or script.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to fetch a specific ayah by reference and edition. Use the response to display the verse in the desired edition or to fetch related resources.",
        "x-mcp-example": {
            "name": "get_ayah_by_reference_and_edition_v1_ayah_reference_editionIdentifier_get",
            "arguments": {"reference": "2:255", "editionIdentifier": "quran-uthmani"}
        }
    }
)
async def get_the_ayah_by_edition(
    reference: str = Path(..., description="A valid reference for ayah number or surahNumber:ayahNumberInSurah", example="2:255"),
    editionIdentifier: str = Path(..., description="A valid edition identifier for edition", example="quran-uthmani")
):
    try:
        if ":" in reference:
            ayah_number_list = reference.split(":")
            data = await ayah_repo.get_an_ayah_by_surah_number(
                int(ayah_number_list[0]),
                int(ayah_number_list[1]),
                editionIdentifier
            )
        elif reference.isdigit():
            data = await ayah_repo.get_an_ayah(int(reference), editionIdentifier)
        else:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": ERROR_INVALID_REFERENCE},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        # Static ayah: cache for 30 days, tag by ayah+edition
        add_cache_headers(response, cache_tag=f"ayah:{reference}:edition:{editionIdentifier}")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching ayah by edition. Reference: %s", e)
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": ERROR_SOMETHING_WRONG},
            status_code=400
        )
        response.headers["Cache-Control"] = CACHE_NO_STORE
        return response


@ayah_router.get(
    "/{reference}/editions/{editionIdentifiers}",
    responses=getTheAyahbyEditionsResponse,
    tags=["Ayah"],
    name="Get Ayah by Number or Number in Surah and Multiple Editions",
    summary="Get ayah by reference and multiple editions",
    description="Returns an ayah by its global number or surah:ayah format for multiple specified editions. Use this to compare a specific verse across different translations or scripts.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to fetch a specific ayah by reference in multiple editions. Provide a comma-separated list of edition identifiers, and use the response to compare translations or scripts.",
        "x-mcp-example": {
            "name": "get_ayah_by_reference_and_editions_v1_ayah_reference_editions_editionIdentifiers_get",
            "arguments": {"reference": "2:255", "editionIdentifiers": "quran-uthmani,quran-simple-clean"}
        }
    }
)
async def get_the_ayah_by_editions(
    reference: str = Path(..., description="A valid reference for ayah number or surahNumber:ayahNumberInSurah", example="2:255"),
    editionIdentifiers: str = Path(..., description="Valid edition identifiers", example="quran-uthmani,quran-simple-clean")
):
    try:
        editionIdentifiers_list = editionIdentifiers.split(',')

        if ":" in reference:
            ayah_number_list = reference.split(":")
            data = await ayah_repo.get_an_ayah_by_surah_number_and_multiple_editions(
                int(ayah_number_list[0]),
                int(ayah_number_list[1]),
                editionIdentifiers_list
            )
        elif reference.isdigit():
            data = await ayah_repo.get_an_ayah_by_multiple_editions(int(reference), editionIdentifiers_list)
        else:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": ERROR_INVALID_REFERENCE},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = CACHE_NO_STORE
            return response

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        # Static ayah: cache for 30 days, tag by ayah+editions
        add_cache_headers(response, cache_tag=f"ayah:{reference}:editions:{editionIdentifiers}")
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching ayah by editions. Reference: %s", e)
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": ERROR_SOMETHING_WRONG},
            status_code=400
        )
        response.headers["Cache-Control"] = CACHE_NO_STORE
        return response
