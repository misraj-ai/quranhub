from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

from repositories import edition_repo  # Using the repository now
from .edition_docs import (
    getTheEditionLanguagesResponse,
    getTheEditionResponse,
    getTheEditionByLanguageResponse,
    getTheEditionTypesResponse,
    getTheEditionByTypeResponse,
    getTheEditionNarratorIdentifiersResponse,
    getTheEditionFormatsResponse,
    getTheEditionByFormatResponse,
    getTheEditionByFormatAndTypeResponse,
    getTheAudioEditionByNarratorIdentifierResponse,
    getEditionsAnalysisResponse,
    # Add canonical docs for tafsir edition by identifier
)


from utils.logger import logger
from utils.helpers import add_cache_headers

edition_router = APIRouter()


@edition_router.get(
    "/",
    responses=getTheEditionResponse,
    tags=["Edition"],
    name="Get All Available Editions",
    summary="List all available editions (filterable)",
    description="Lists all available editions of the Quran, including text, audio, translations, and tafsir. Editions can be filtered by language, type, or format. Use this to discover available resources for further queries or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to list all available editions. Use the filters to narrow down by language, type, or format, and use the edition identifiers in subsequent calls to fetch Quranic content.",
        "x-mcp-example": {
            "name": "get_all_editions_v1_edition__get",
            "arguments": {"format": "text", "language": "ar", "type": "quran"}
        }
    }
)
async def get_the_edition(
    format: str = Query(None, description="Specify a format. 'text' or 'audio'", example='text'),
    language: str = Query(None, min_length=2, max_length=2, description="A 2-digit language code", example="ar"),
    type: str = Query(None, description="A valid type for edition", example="quran")
):
    try:
        data = await edition_repo.get_edition(language=language, type=type, format=format)
        if isinstance(data, str):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": f"Something wrong happened: {data}"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_tag="edition:all")
        return response
        
    except Exception as e:
        logger.exception("An exception occurred while fetching editions - %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something wrong happened"},
            status_code=400
        )

  # Cache for 1 day
@edition_router.get(
    "/language",
    responses=getTheEditionLanguagesResponse,
    tags=["Edition"],
    name="Lists all languages",
    summary="List all languages for editions",
    description="Lists all languages in which Quranic editions are available. Use this to discover supported languages for filtering or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get all supported languages for editions. Use the language codes in subsequent edition queries.",
        "x-mcp-example": {
            "name": "get_edition_languages_v1_edition_language_get",
            "arguments": {}
        }
    }
)
async def get_the_edition_languages():
    try:
        data = await edition_repo.get_editions_languages()
        if isinstance(data, str):
            logger.error("Something wrong happened: %s", data)
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Something wrong happened: " + data},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        add_cache_headers(response, cache_tag="edition:languages")
        return response
    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something wrong happened"},
            status_code=400
        )

  # Cache for 1 day
@edition_router.get(
    "/language/{language}",
    responses=getTheEditionByLanguageResponse,
    tags=["Edition"],
    name="Get All Available Editions by Language",
    summary="List all editions by language",
    description="Lists all available editions for a given language. Use this to discover resources in a specific language for further queries or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to list all editions for a specific language. Use the language code to filter editions and use the identifiers in subsequent calls.",
        "x-mcp-example": {
            "name": "get_editions_by_language_v1_edition_language_language_get",
            "arguments": {"language": "fr"}
        }
    }
)
async def get_the_edition_by_language(
    language: str = Path(..., min_length=2, max_length=2, description="A 2 digit language code", example="fr")
):
    try:
        data = await edition_repo.get_edition(language=language)
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
        add_cache_headers(response, cache_tag=f"edition:language:{language}")
        return response
    except Exception as e:
        # Log unexpected exceptions and return a generic error response
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

  # Cache for 1 day
@edition_router.get(
    "/type",
    responses=getTheEditionTypesResponse,
    tags=["Edition"],
    name="Lists all types",
    summary="List all edition types",
    description="Lists all types in which Quranic editions are available. Use this to discover supported types for filtering or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get all supported edition types. Use the type values in subsequent edition queries.",
        "x-mcp-example": {
            "name": "get_edition_types_v1_edition_type_get",
            "arguments": {}
        }
    }
)
async def get_the_edition_types():
    try:
        data = await edition_repo.get_editions_types()
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
        add_cache_headers(response, cache_tag="edition:types")
        return response
    except Exception as e:
        # Log unexpected exceptions and return a generic error response
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

  # Cache for 1 day
@edition_router.get(
    "/type/{type}",
    responses=getTheEditionByTypeResponse,
    tags=["Edition"],
    name="Get All Available Editions by Type",
    summary="List all editions by type",
    description="Lists all available editions for a given type. Use this to discover resources of a specific type for further queries or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to list all editions for a specific type. Use the type value to filter editions and use the identifiers in subsequent calls.",
        "x-mcp-example": {
            "name": "get_editions_by_type_v1_edition_type_type_get",
            "arguments": {"type": "quran"}
        }
    }
)
async def get_the_edition_by_type(type: str = Path(..., description="A valid type for edition", example="quran")):
    try:
        data = await edition_repo.get_edition(type=type)
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
        add_cache_headers(response, cache_tag=f"edition:type:{type}")
        return response
    except Exception as e:
        # Log unexpected exceptions and return a generic error response
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )


  # Cache for 1 day
@edition_router.get(
    "/format",
    responses=getTheEditionFormatsResponse,
    tags=["Edition"],
    name="Lists all formats",
    summary="List all edition formats",
    description="Lists all formats in which Quranic editions are available. Use this to discover supported formats for filtering or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get all supported edition formats. Use the format values in subsequent edition queries.",
        "x-mcp-example": {
            "name": "get_edition_formats_v1_edition_format_get",
            "arguments": {}
        }
    }
)
async def get_the_edition_formats():
    try:
        data = await edition_repo.get_editions_formats()
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
        add_cache_headers(response, cache_tag="edition:formats")
        return response
    except Exception as e:
        # Log unexpected exceptions and return a generic error response
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

  # Cache for 1 day
@edition_router.get(
    "/format/{format}",
    responses=getTheEditionByFormatResponse,
    tags=["Edition"],
    name="Get All Available Editions by Format",
    summary="List all editions by format",
    description="Lists all available editions for a given format. Use this to discover resources of a specific format for further queries or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to list all editions for a specific format. Use the format value to filter editions and use the identifiers in subsequent calls.",
        "x-mcp-example": {
            "name": "get_editions_by_format_v1_edition_format_format_get",
            "arguments": {"format": "audio"}
        }
    }
)
async def get_edition_by_format(format: str = Path(..., description="A valid format for edition", example="audio")):
    try:
        data = await edition_repo.get_edition(format=format)
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
        add_cache_headers(response, cache_tag=f"edition:format:{format}")
        return response
    except Exception as e:
        # Log unexpected exceptions and return a generic error response
        logger.error("An exception occurred: %s", str(e))
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

  # Cache for 1 day
@edition_router.get(
    "/format/{format}/type/{type}",
    responses=getTheEditionByFormatAndTypeResponse,
    tags=["Edition"],
    name="Get All Available Editions by Format and Type",
    summary="List all editions by format and type",
    description="Lists all available editions for a given format and type. Use this to discover resources matching both criteria for further queries or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to list all editions for a specific format and type. Use the values to filter editions and use the identifiers in subsequent calls.",
        "x-mcp-example": {
            "name": "get_editions_by_format_and_type_v1_edition_format_format_type_type_get",
            "arguments": {"format": "text", "type": "narration"}
        }
    }
)
async def get_edition_by_format_and_type(
    format: str = Path(..., description="A valid format for edition", example="text"),
    type: str = Path(..., description="A valid type for edition", example="narration")
):
    try:
        data = await edition_repo.get_edition(format=format, type=type)
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
        add_cache_headers(response, cache_tag=f"edition:format:{format}:type:{type}")
        return response
    except Exception:
        # Log unexpected exceptions and return a generic error response
        logger.error("An exception occurred")
        return JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )

@edition_router.get(
    "/audio/distinct",
    tags=["Edition"],
    name="Get Distinct Audio Editions by English Name",
    summary="List distinct audio editions by English name",
    description="Returns a list of distinct audio editions using englishName. Use this to discover unique audio recitations for further queries or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get a list of unique audio recitations by English name. Use the results to select reciters for audio playback or download.",
        "x-mcp-example": {
            "name": "get_distinct_audio_editions_v1_edition_audio_distinct_get",
            "arguments": {}
        }
    }
)
async def get_distinct_audio_editions():
    data = await edition_repo.get_distinct_audio_editions_by_englishname()
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
    add_cache_headers(response, cache_tag="edition:audio:distinct")
    return response

# Canonical: Call repo function to get distinct audio edition by identifier
@edition_router.get(
    "/audio/edition/{editionIdentifier}",
    tags=["Edition"],
    summary="Get distinct audio edition by edition identifier",
    description="Given an audio edition identifier, returns the same object shape as the distinct audio editions endpoint, but for a single edition. Returns 404 if not found or not an audio edition.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get a distinct audio edition object for a specific audio edition identifier.",
        "x-mcp-example": {"editionIdentifier": "ar.abdulbasitmurattal.hafs"}
    }
)
async def get_audio_edition_by_identifier(
    editionIdentifier: str = Path(..., description="Audio edition identifier (e.g., ar.abdulbasitmurattal.hafs)")
):
    try:
        data = await edition_repo.get_distinct_audio_edition_by_identifier(editionIdentifier)
        if data == "not_found":
            response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Edition not found."})
            response.headers["Cache-Control"] = "no-store"
            return response
        if data == "not_audio":
            response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Edition is not audio."})
            response.headers["Cache-Control"] = "no-store"
            return response
        if not data:
            response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Edition not found."})
            response.headers["Cache-Control"] = "no-store"
            return response
        response = JSONResponse(status_code=200, content={"code": 200, "status": "OK", "data": data})
        add_cache_headers(response, cache_tag=f"edition:audio:{editionIdentifier}")
        return response
    except Exception as e:
        logger.error(f"An exception occurred in get_audio_edition_by_identifier: {str(e)}")
        response = JSONResponse(status_code=400, content={"code": 400, "status": "Error", "data": "Something went wrong"})
        response.headers["Cache-Control"] = "no-store"
        return response
    
# Canonical: Call repo function to get distinct audio edition by identifier
@edition_router.get(
    "/tafsir/{editionIdentifier}",
    tags=["Edition"],
    summary="Get tafsir edition by edition identifier",
    description="Given a tafsir edition identifier, returns the canonical tafsir edition metadata object. Returns 404 if not found or not a tafsir edition.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get a tafsir edition object for a specific tafsir edition identifier.",
        "x-mcp-example": {"editionIdentifier": "ar.mukhtasar"}
    }
)
async def get_tafsir_edition_by_identifier(
    editionIdentifier: str = Path(..., description="Tafsir edition identifier (e.g., ar.mukhtasar)")
):
    try:
        data = await edition_repo.get_tafsir_edition_by_identifier(editionIdentifier)
        if data == "not_found":
            response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Edition not found."})
            response.headers["Cache-Control"] = "no-store"
            return response
        if data == "not_tafsir":
            response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Edition is not tafsir."})
            response.headers["Cache-Control"] = "no-store"
            return response
        if not data:
            response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Edition not found."})
            response.headers["Cache-Control"] = "no-store"
            return response
        response = JSONResponse(status_code=200, content={"code": 200, "status": "OK", "data": data})
        add_cache_headers(response, cache_tag=f"edition:tafsir:{editionIdentifier}")
        return response
    except Exception as e:
        logger.error(f"An exception occurred in get_tafsir_edition_by_identifier: {str(e)}")
        response = JSONResponse(status_code=400, content={"code": 400, "status": "Error", "data": "Something went wrong"})
        response.headers["Cache-Control"] = "no-store"
        return response
    
@edition_router.get(
    "/narratorIdentifier",
    responses=getTheEditionNarratorIdentifiersResponse,
    tags=["Edition"],
    name="Lists all Narrator Identifiers",
    summary="List all narrator identifiers for editions",
    description="Lists all narrator identifiers in which editions are available. Use this to discover available reciters for filtering or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get all available narrator identifiers for editions. Use the results to filter or select reciters in subsequent queries.",
        "x-mcp-example": {
            "name": "get_narrator_identifiers_v1_edition_narratorIdentifier_get",
            "arguments": {}
        }
    }
)
async def get_edition_narrator_identifiers():
    try:
        data = await edition_repo.get_editions_narrator_identifiers()
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
        add_cache_headers(response, cache_tag="edition:narratorIdentifiers")
        return response
    except Exception:
        logger.error("An exception occurred")
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response

@edition_router.get(
    "/audio/narrator/{narratorIdentifier}",
    responses=getTheAudioEditionByNarratorIdentifierResponse,
    tags=["Edition"],
    name="Get All Available Audio Editions by Narrator Identifier",
    summary="List all audio editions by narrator identifier",
    description="Lists all available audio editions for a given narrator. Use this to discover audio resources for a specific reciter for playback or download.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to list all audio editions for a specific narrator. Use the narrator identifier to filter editions and use the results for playback or download.",
        "x-mcp-example": {
            "name": "get_audio_editions_by_narrator_v1_edition_audio_narratorIdentifier_get",
            "arguments": {"narratorIdentifier": "quran-warsh"}
        }
    }
)
async def get_audio_edition_by_narrator_identifier(narratorIdentifier: str = Path(..., description="A valid narrator identifier for edition", example="quran-warsh")):
    try:
        data = await edition_repo.get_edition(format="audio", narrator=narratorIdentifier, type="versebyverse")
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
        add_cache_headers(response, cache_tag=f"edition:audio:narrator:{narratorIdentifier}")
        return response
    except Exception:
        logger.error("An exception occurred")
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response

@edition_router.get(
    "/analysis",
    responses=getEditionsAnalysisResponse,
    tags=["Edition"],
    name="Get Editions Analysis",
    summary="Get statistical analysis of all editions",
    description="Provides clean and organized statistical analysis of all editions in the database. Returns logical groupings of data including overview statistics, format/type/language distributions, narration analysis, reciter statistics, and comprehensive audio edition analysis with bitrate information. Use this to understand the distribution and characteristics of available editions.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get a statistical overview of all editions. Use the results to guide resource selection, display analytics, or inform further queries.",
        "x-mcp-example": {
            "name": "get_editions_analysis_v1_edition_analysis_get",
            "arguments": {}
        }
    }
)
async def get_editions_statistics():
    try:
        data = await edition_repo.get_edition_analysis()
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
        add_cache_headers(response, cache_tag="edition:analysis")
        return response
    except Exception as e:
        logger.error("An exception occurred during editions analysis: %s", str(e))
        response = JSONResponse(
            content={"code": 400, "status": "Error", "data": "Something went wrong"},
            status_code=400
        )
        response.headers["Cache-Control"] = "no-store"
        return response
