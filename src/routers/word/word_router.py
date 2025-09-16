
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select
from db.session import AsyncSessionLocal
from db.models import Word
from .word_docs import (
    get_word_tajweed_response,
    get_word_line_number_response,
    get_word_image_response
)
from utils.logger import logger

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
    location: str = Query(..., description="Location in the format surah:ayah:position", example="1:1:2")
):
    try:
        surah, ayah, position = map(int, location.split(":"))
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
                return JSONResponse(
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
            else:
                return JSONResponse(
                    content={"code": 404, "status": "Error", "data": f"Word not found for location {location}"},
                    status_code=404
                )
    except Exception as e:
        logger.error(f"Error in get_word_tajweed: {e}", exc_info=True)
        return JSONResponse(
            content={"code": 500, "status": "Error", "data": str(e)},
            status_code=500
        )

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
    location: str = Query(..., description="Location in the format surah:ayah:position", example="1:1:2")
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
                return JSONResponse(
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
            else:
                return JSONResponse(
                    content={"code": 404, "status": "Error", "data": f"Word not found for location {location}"},
                    status_code=404
                )
    except Exception as e:
        logger.error(f"Error in get_word_line_number: {e}", exc_info=True)
        return JSONResponse(
            content={"code": 500, "status": "Error", "data": str(e)},
            status_code=500
        )

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
    location: str = Query(..., description="Location in the format surah:ayah:position", example="1:1:2"),
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
                    return JSONResponse(
                        content={"code": 400, "status": "Error", "data": f"Invalid image type: {type}"},
                        status_code=400
                    )
                return JSONResponse(
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
            else:
                return JSONResponse(
                    content={"code": 404, "status": "Error", "data": f"Word not found for location {location}"},
                    status_code=404
                )
    except Exception as e:
        logger.error(f"Error in get_word_image: {e}", exc_info=True)
        return JSONResponse(
            content={"code": 500, "status": "Error", "data": str(e)},
            status_code=500
        )
