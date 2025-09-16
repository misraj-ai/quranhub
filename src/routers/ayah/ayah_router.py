from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

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
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception:
        logger.exception("Unexpected error fetching random ayah")
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
    

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
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception:
        logger.exception("Unexpected error fetching random ayah by edition")
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
    

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
        edition_identifiers_list = editionIdentifiers.split(',')

        if not edition_identifiers_list:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "At least one valid edition identifier must be provided."},
                status_code=400
            )

        data = await ayah_repo.get_an_ayah_by_multiple_editions(random_number, edition_identifiers_list)

        if isinstance(data, str):
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception:
        logger.exception("Unexpected error fetching random ayah for multiple editions")
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
    

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
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Invalid reference format."},
                status_code=400
            )

        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching ayah. Reference: %s", e)
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
    

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
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Invalid reference format."},
                status_code=400
            )

        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching ayah by edition. Reference: %s", e)
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )


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
        edition_identifiers_list = editionIdentifiers.split(',')
        
        if ":" in reference:
            ayah_number_list = reference.split(":")
            data = await ayah_repo.get_an_ayah_by_surah_number_and_multiple_editions(
                int(ayah_number_list[0]),
                int(ayah_number_list[1]),
                edition_identifiers_list
            )
        elif reference.isdigit():
            data = await ayah_repo.get_an_ayah_by_multiple_editions(int(reference), edition_identifiers_list)
        else:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Invalid reference format."},
                status_code=400
            )

        if isinstance(data, str):
            
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )

        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
          # Cache for 1 day (86400 seconds)
        return response

    except Exception as e:
        logger.exception("An exception occurred while fetching ayah by editions. Reference: %s", e)
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
