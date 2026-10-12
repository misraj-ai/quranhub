
from typing import Optional
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from utils.helpers import add_cache_headers, add_word_audio
from sqlalchemy import select
from db.session import AsyncSessionLocal
from db.models import Word
from repositories import edition_repo
from .word_docs import (
    get_word_tajweed_response,
    get_word_line_number_response,
    get_word_image_response,
    get_word_audio_response,
)
from utils.logger import logger
from utils.config import BASIC_TAJWEED_RULES


LOCATION_DESC = "Location in the format surah:ayah:position"
word_router = APIRouter()

@word_router.get(
    "/tajweed",
    responses=get_word_tajweed_response,
    tags=["Word"],
    name="Get Tajweed Rules by Location",
    summary="Get tajweed rules for a word by location",
    description="Returns the tajweed rules for a specific word in the Quran, identified by its location (surah:ayah:position). Use this to analyze or display tajweed for a word in context. The response includes the word's text and a list of tajweed rules.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint after identifying a word's location (surah:ayah:position) to retrieve its tajweed rules. Use the 'tajweed' field in the response to display or process tajweed information for the word.",
        "x-mcp-example": {
            "name": "get_word_tajweed_v1_word_tajweed_get",
            "arguments": {"location": "1:1:2"}
        }
    }
)
async def get_word_tajweed(
    location: str = Query(..., description=LOCATION_DESC, example="1:1:2"),
    level: str = Query("basic", description="Tajweed rules level ('basic' or 'advanced'). 'basic' filters for common rules, 'advanced' returns all.", regex="^(basic|advanced)$")
):
    try:
        parts = list(map(int, location.split(":")))
        if len(parts) == 3:
            surah, ayah, position = parts
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(Word.tajweed).filter(
                        Word.surat_id == surah,
                        Word.numberinsurat == ayah,
                        Word.position == position
                    )
                )
                tajweed = result.scalar_one_or_none()
                if tajweed is not None:
                    # Filter tajweed rules
                    if level == "basic" and tajweed and "rules" in tajweed:
                        tajweed["rules"] = [
                            rule for rule in tajweed["rules"]
                            if rule.get("cls") in BASIC_TAJWEED_RULES
                        ]

                    response = JSONResponse(
                        content={
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "location": location,
                                "tajweed": tajweed
                            }
                        },
                        status_code=200
                    )
                    add_cache_headers(response, cache_tag=f"word:tajweed:{location}")
                    return response
                else:
                    response = JSONResponse(
                        content={"code": 404, "status": "Error", "data": f"Word not found for location {location}"},
                        status_code=404
                    )
                    response.headers["Cache-Control"] = "no-store"
                    return response
        elif len(parts) == 2:
            surah, ayah = parts
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(Word.position, Word.tajweed).filter(
                        Word.surat_id == surah,
                        Word.numberinsurat == ayah
                    ).order_by(Word.position)
                )
                rows = result.all()
                if rows:
                    words_tajweed = []
                    for row in rows:
                        t_data = row.tajweed
                        if level == "basic" and t_data and "rules" in t_data:
                            # Create a copy to avoid mutating if necessary (though here it's fresh from DB)
                            t_data = t_data.copy()
                            t_data["rules"] = [
                                rule for rule in t_data["rules"]
                                if rule.get("cls") in BASIC_TAJWEED_RULES
                            ]
                        words_tajweed.append({"position": row.position, "tajweed": t_data})
                    
                    response = JSONResponse(
                        content={
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "location": location,
                                "words": words_tajweed
                            }
                        },
                        status_code=200
                    )
                    add_cache_headers(response, cache_tag=f"word:tajweed:ayah:{location}")
                    return response
                else:
                    response = JSONResponse(
                        content={"code": 404, "status": "Error", "data": f"No words found for ayah {location}"},
                        status_code=404
                    )
                    response.headers["Cache-Control"] = "no-store"
                    return response
        else:
            return JSONResponse(
                content={"code": 400, "status": "Error", "data": "Invalid location format. Expected surah:ayah or surah:ayah:position"},
                status_code=400
            )
    except Exception as e:
        logger.error(f"Error in get_word_tajweed: {e}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": str(e)},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response

@word_router.get(
    "/line-number",
    responses=get_word_line_number_response,
    tags=["Word"],
    name="Get Line Number by Location",
    summary="Get line number for a word by location",
    description="Returns the line number on the page for a specific word in the Quran, identified by its location (surah:ayah:position). Use this to map a word to its printed line in a Mushaf or digital display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint after determining a word's location to find its line number in the printed or digital Quran. Use the 'line_number' field in the response for layout or highlighting.",
        "x-mcp-example": {
            "name": "get_word_line_number_v1_word_line_number_get",
            "arguments": {"location": "1:1:2"}
        }
    }
)
async def get_word_line_number(
    location: str = Query(..., description=LOCATION_DESC, example="1:1:2")
):
    try:
        surah, ayah, position = map(int, location.split(":"))
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Word.line_number).filter(
                    Word.surat_id == surah,
                    Word.numberinsurat == ayah,
                    Word.position == position
                )
            )
            line_number = result.scalar_one_or_none()
            if line_number is not None:
                response = JSONResponse(
                    content={
                        "code": 200,
                        "status": "OK",
                        "data": {
                            "location": location,
                            "line_number": line_number
                        }
                    },
                    status_code=200
                )
                add_cache_headers(response, cache_tag=f"word:line_number:{location}")
                return response
            else:
                response = JSONResponse(
                    content={"code": 404, "status": "Error", "data": f"Word not found for location {location}"},
                    status_code=404
                )
                response.headers["Cache-Control"] = "no-store"
                return response
    except Exception as e:
        logger.error(f"Error in get_word_line_number: {e}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": str(e)},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response

@word_router.get(
    "/image",
    responses=get_word_image_response,
    tags=["Word"],
    name="Get Word Image by Location",
    summary="Get per-word image by location and type",
    description=(
        "Returns the image URL for a specific word in the Quran, identified by its location (surah:ayah:position) and image type (v4, rq, qa). "
        "Use this to display a rendered image of the word in different tajweed styles or color schemes. "
        "The response includes the image URL and type."
    ),
    openapi_extra={
        "x-agent-hints": "Call this endpoint after identifying a word's location and desired image type (v4, rq, qa) to retrieve a rendered image URL for display or download.",
        "x-mcp-example": {
            "name": "get_word_image_v1_word_image_get",
            "arguments": {"location": "1:1:2", "type": "v4"}
        }
    }
)
async def get_word_image(
    location: str = Query(..., description=LOCATION_DESC, example="1:1:2"),
    type: str = Query(
        "v4",
        description = (
            "Image type: v4, rq, or qa.\n\n"
            "- rq: The ReciteQuran (QPC Hafs) tajweed image for the specific word, using the ReciteQuran color palette.\n"
            "- v4: A per-word render of the 'V4 tajweed' glyph (font-driven) that supports multiple themes (light/dark/sepia).\n"
            "- qa: The Quran Academy tajweed image for the word, using QA’s color scheme and rendering pipeline."
        ),
        example="v4"
    )
):
    try:
        surah, ayah, position = map(int, location.split(":"))
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Word.v4_img_url, Word.rq_img_url, Word.qa_img_url).filter(
                    Word.surat_id == surah,
                    Word.numberinsurat == ayah,
                    Word.position == position
                )
            )
            row = result.first()
            if row:
                img_url = None
                if type == "v4":
                    img_url = row[0]
                elif type == "rq":
                    img_url = row[1]
                elif type == "qa":
                    img_url = row[2]
                else:
                    response = JSONResponse(
                        content={"code": 400, "status": "Error", "data": f"Invalid image type: {type}"},
                        status_code=400
                    )
                    response.headers["Cache-Control"] = "no-store"
                    return response
                response = JSONResponse(
                    content={
                        "code": 200,
                        "status": "OK",
                        "data": {
                            "location": location,
                            "type": type,
                            "img_url": img_url
                        }
                    },
                    status_code=200
                )
                add_cache_headers(response, cache_tag=f"word:image:{location}:{type}")
                return response
            else:
                response = JSONResponse(
                    content={"code": 404, "status": "Error", "data": f"Word not found for location {location}"},
                    status_code=404
                )
                response.headers["Cache-Control"] = "no-store"
                return response
    except Exception as e:
        logger.error(f"Error in get_word_image: {e}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": str(e)},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


def _no_store(response: JSONResponse) -> JSONResponse:
    response.headers["Cache-Control"] = "no-store"
    return response


@word_router.get(
    "/audio",
    responses=get_word_audio_response,
    tags=["Word"],
    name="Get Word Audio by Location",
    summary="Get per-word audio URLs by location",
    description=(
        "Returns per-word audio URLs from a word-by-word audio edition, for a specific word "
        "(surah:ayah:position) or for every word in an ayah (surah:ayah). Positions follow the Hafs word "
        "breakdown. The `audio` field is the highest-bitrate MP3 and `audioSecondary` lists lower bitrates; "
        "`audio` is null for the few words that have no recording."
    ),
    openapi_extra={
        "x-agent-hints": "Call this endpoint with a word location (surah:ayah:position) or an ayah (surah:ayah) to get MP3 URLs for pronouncing individual Quranic words, e.g. for tap-to-hear word features.",
        "x-mcp-example": {
            "name": "get_word_audio_v1_word_audio_get",
            "arguments": {"location": "1:1:2"}
        }
    }
)
async def get_word_audio(
    location: str = Query(..., description="Location in the format surah:ayah:position or surah:ayah", example="1:1:2"),
    edition: Optional[str] = Query(None, description="Word-by-word audio edition identifier. Defaults to the first available word-by-word audio edition.", example="ar.wordbyword.hafs"),
):
    try:
        try:
            parts = [int(part) for part in location.split(":")]
        except ValueError:
            parts = []
        if len(parts) not in (2, 3):
            return _no_store(JSONResponse(
                content={"code": 400, "status": "Error", "data": "Invalid location format. Expected surah:ayah or surah:ayah:position"},
                status_code=400
            ))

        audio_edition = await edition_repo.get_word_audio_edition(edition)
        if audio_edition is None:
            suffix = f" for identifier '{edition}'" if edition else ""
            return _no_store(JSONResponse(
                content={"code": 404, "status": "Error", "data": f"No word-by-word audio edition found{suffix}"},
                status_code=404
            ))

        name = audio_edition.name if isinstance(audio_edition.name, dict) else {}
        edition_info = {
            "identifier": audio_edition.identifier,
            "name": name.get("ar"),
            "englishName": name.get("en"),
            "format": audio_edition.format,
            "type": audio_edition.type,
            "narratorIdentifier": audio_edition.narrator_identifier,
        }

        surah, ayah = parts[0], parts[1]
        async with AsyncSessionLocal() as session:
            query = select(Word.position, Word.text).filter(
                Word.surat_id == surah,
                Word.numberinsurat == ayah,
            )
            if len(parts) == 3:
                query = query.filter(Word.position == parts[2])
            result = await session.execute(query.order_by(Word.position))
            rows = result.all()

        if not rows:
            message = f"Word not found for location {location}" if len(parts) == 3 else f"No words found for ayah {location}"
            return _no_store(JSONResponse(content={"code": 404, "status": "Error", "data": message}, status_code=404))

        if len(parts) == 3:
            row = rows[0]
            data = {"location": location, "text": row.text}
            add_word_audio(data, audio_edition, surah, ayah, row.position)
            data["edition"] = edition_info
        else:
            words = []
            for row in rows:
                word = {"position": row.position, "location": f"{surah}:{ayah}:{row.position}", "text": row.text}
                add_word_audio(word, audio_edition, surah, ayah, row.position)
                words.append(word)
            data = {"location": location, "edition": edition_info, "words": words}

        response = JSONResponse(content={"code": 200, "status": "OK", "data": data}, status_code=200)
        add_cache_headers(response, cache_tag=f"word:audio:{location}:{audio_edition.identifier}")
        return response
    except Exception as e:
        logger.error(f"Error in get_word_audio: {e}", exc_info=True)
        return _no_store(JSONResponse(content={"code": 500, "status": "Error", "data": str(e)}, status_code=500))
