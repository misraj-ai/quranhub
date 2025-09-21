
from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse
from utils.helpers import add_cache_headers
from repositories.mushaf_layout_repo import get_layouts, get_layout_by_code, get_layout_font, get_lines_for_page, get_lines_for_surah, lookup_lines
from routers.mushaf_layout.mushaf_layout_docs import getMushafLayoutsResponse, getMushafLayoutDetailResponse, getMushafLayoutPageLinesResponse, getMushafLayoutSurahLinesResponse, getMushafLayoutLookupResponse


mushaf_layout_router = APIRouter()

@mushaf_layout_router.get(
    "/",
    tags=["Mushaf Layout"],
    summary="List mushaf layouts",
    description="Paginated list of mushaf layouts. Filter by code, linesPerPage, fontCode.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to list all mushaf layouts with pagination and filtering.",
        "x-mcp-example": {"code": "qpc-v1-15-lines", "linesPerPage": 15, "fontCode": "qpc-v1", "limit": 2, "offset": 0}
    },
    responses=getMushafLayoutsResponse
)
async def list_layouts(
    layoutCode: str = Query(None, alias="layoutCode"),
    linesPerPage: int = Query(None, alias="linesPerPage"),
    fontCode: str = Query(None, alias="fontCode"),
    limit: int = Query(20, ge=1, le=100, alias="limit"),
    offset: int = Query(0, ge=0, alias="offset")
):
    result = await get_layouts(layoutCode, linesPerPage, fontCode, limit, offset)
    items = []
    for l in result["items"]:
        font = await get_layout_font(l.font_id) if l.font_id else None
        items.append({
            "code": l.code,
            "name": l.name,
            "numberOfPages": l.number_of_pages,
            "linesPerPage": l.lines_per_page,
            "font": {"code": font.code, "name": font.name, "category": font.category} if font else None
        })
    response = JSONResponse(
        content={
            "code": 200,
            "status": "OK",
            "data": {
                "total": result["total"],
                "items": items
            }
        },
        status_code=200
    )
    add_cache_headers(response, cache_tag="mushaf_layout:list")
    return response

@mushaf_layout_router.get(
    "/{layoutCode}",
    tags=["Mushaf Layout"],
    summary="Get mushaf layout detail",
    description="Get mushaf layout detail with resolved font.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to get details for a specific mushaf layout by code.",
        "x-mcp-example": {"code": "qpc-v1-15-lines"}
    },
    responses=getMushafLayoutDetailResponse
)
async def layout_detail(
    layoutCode: str = Path(..., alias="layoutCode", description="Mushaf layout code (e.g., 'qpc-v1-15-lines')")
):
    layout = await get_layout_by_code(layoutCode)
    if not layout:
        response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Layout not found."})
        response.headers["Cache-Control"] = "no-store"
        return response
    font = await get_layout_font(layout.font_id) if layout.font_id else None
    response = JSONResponse(
        content={
            "code": 200,
            "status": "OK",
            "data": {
                "code": layout.code,
                "name": layout.name,
                "numberOfPages": layout.number_of_pages,
                "linesPerPage": layout.lines_per_page,
                "font": {"code": font.code, "name": font.name, "category": font.category} if font else None
            }
        },
        status_code=200
    )
    add_cache_headers(response, cache_tag=f"mushaf_layout:detail:{layoutCode}")
    return response

@mushaf_layout_router.get(
    "/{layoutCode}/pages/{pageNumber}",
    tags=["Mushaf Layout"],
    summary="Get lines for a page",
    description="Get all lines for a page in a mushaf layout.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to get all lines for a specific page in a mushaf layout.",
        "x-mcp-example": {"code": "qpc-v1-15-lines", "pageNumber": 1}
    },
    responses=getMushafLayoutPageLinesResponse
)
async def layout_page_lines(
    layoutCode: str = Path(..., alias="layoutCode", description="Mushaf layout code (e.g., 'qpc-v1-15-lines')"),
    pageNumber: int = Path(..., ge=1, alias="pageNumber")
):
    layout = await get_layout_by_code(layoutCode)
    if not layout:
        response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Layout not found."})
        response.headers["Cache-Control"] = "no-store"
        return response
    lines = await get_lines_for_page(layout.layout_id, pageNumber)
    if not lines:
        response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Layout or page not found."})
        response.headers["Cache-Control"] = "no-store"
        return response
    response = JSONResponse(
        content={
            "code": 200,
            "status": "OK",
            "data": [
                {"lineNumber": l.line_number, "lineType": l.line_type, "isCentered": l.is_centered, "surahNumber": l.surah_number} for l in lines
            ]
        },
        status_code=200
    )
    add_cache_headers(response, cache_tag=f"mushaf_layout:page:{layoutCode}:{pageNumber}")
    return response

@mushaf_layout_router.get(
    "/{layoutCode}/surah/{surahNumber}",
    tags=["Mushaf Layout"],
    summary="Get lines for a surah",
    description="Get all lines for a surah in a mushaf layout.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to get all lines for a specific surah in a mushaf layout.",
        "x-mcp-example": {"code": "qpc-v1-15-lines", "surahNumber": 1}
    },
    responses=getMushafLayoutSurahLinesResponse
)
async def layout_surah_lines(
    layoutCode: str = Path(..., alias="layoutCode", description="Mushaf layout code (e.g., 'qpc-v1-15-lines')"),
    surahNumber: int = Path(..., ge=1, alias="surahNumber")
):
    layout = await get_layout_by_code(layoutCode)
    if not layout:
        response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Layout not found."})
        response.headers["Cache-Control"] = "no-store"
        return response
    lines = await get_lines_for_surah(layout.layout_id, surahNumber)
    if not lines:
        response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Layout or surah not found."})
        response.headers["Cache-Control"] = "no-store"
        return response
    response = JSONResponse(
        content={
            "code": 200,
            "status": "OK",
            "data": [
                {
                    "pageNumber": l.page_number,
                    "lineNumber": l.line_number,
                    "lineType": l.line_type,
                    "isCentered": l.is_centered,
                    "fromWord": l.ext_first_word_id,
                    "toWord": l.ext_last_word_id
                } for l in lines
            ]
        },
        status_code=200
    )
    add_cache_headers(response, cache_tag=f"mushaf_layout:surah:{layoutCode}:{surahNumber}")
    return response

@mushaf_layout_router.get(
    "/{layoutCode}/word/{fromWord}/{toWord}",
    tags=["Mushaf Layout"],
    summary="Lookup page/line spans",
    description="Lookup page/line spans by word id range. The maximum allowed range (toWord - fromWord) is 20.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to lookup page/line spans by word id range in a mushaf layout.",
        "x-mcp-example": {"code": "qpc-v1-15-lines", "fromWord": 100, "toWord": 120}
    },
    responses=getMushafLayoutLookupResponse
)
async def layout_lookup(
    layoutCode: str = Path(..., alias="layoutCode", description="Mushaf layout code (e.g., 'qpc-v1-15-lines')"),
    fromWord: int = Path(..., alias="fromWord", description="Start word id (inclusive)"),
    toWord: int = Path(..., alias="toWord", description="End word id (inclusive)")
):
    if toWord - fromWord > 20:
        response = JSONResponse(status_code=400, content={"code": 400, "status": "Bad Request", "data": "The difference between toWord and fromWord must not be greater than 20."})
        response.headers["Cache-Control"] = "no-store"
        return response
    layout = await get_layout_by_code(layoutCode)
    if not layout:
        response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Layout not found."})
        response.headers["Cache-Control"] = "no-store"
        return response
    lines = await lookup_lines(layout.layout_id, fromWord, toWord)
    if not lines:
        response = JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "No lines found for lookup."})
        response.headers["Cache-Control"] = "no-store"
        return response
    response = JSONResponse(
        content={
            "code": 200,
            "status": "OK",
            "data": [
                {
                    "pageNumber": l.page_number,
                    "lineNumber": l.line_number,
                    "lineType": l.line_type,
                    "isCentered": l.is_centered,
                    "fromWord": l.ext_first_word_id,
                    "toWord": l.ext_last_word_id
                } for l in lines
            ]
        },
        status_code=200
    )
    add_cache_headers(response, cache_tag=f"mushaf_layout:lookup:{layoutCode}:{fromWord}:{toWord}")
    return response
