

# Standard library imports
# (none needed)

# Third-party imports
from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse

# Project imports
from repositories.font_repo import (
    get_font_by_code,
    get_font_files,
    get_font_page_files,
    get_font_page_range,
    get_all_font_formats,
    get_all_font_archives,
    get_all_font_categories,
    get_all_font_kinds
)
from routers.font.font_docs import (
    getFontsResponse,
    getFontDetailResponse,
    getFontFilesResponse,
    getFontPageFilesResponse,
    getFontCategoriesResponse,
    getFontKindsResponse,
    getFontFormatsResponse,
    getFontArchivesResponse
)

font_router = APIRouter()

@font_router.get(
    "/kinds",
    tags=["Font"],
    summary="List all font kinds",
    description="Lists all kinds of font files available (e.g., regular, pack, extras). Use this to discover supported kinds for filtering or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get all supported font kinds. Use the kind values in subsequent font file queries.",
        "x-mcp-example": {"name": "getFontKinds", "arguments": {}}
    },
    responses=getFontKindsResponse
)
async def get_font_kinds():
    kinds = await get_all_font_kinds()
    return {"code": 200, "status": "OK", "data": kinds}

@font_router.get(
    "/formats",
    tags=["Font"],
    summary="List all font formats",
    description="Lists all formats in which font files are available (e.g., ttf, woff, woff2, otf, json). Use this to discover supported formats for filtering or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get all supported font formats. Use the format values in subsequent font file queries.",
        "x-mcp-example": {"name": "getFontFormats", "arguments": {}}
    },
    # operation_id removed
)
async def get_font_formats():
    formats = await get_all_font_formats()
    return {"code": 200, "status": "OK", "data": formats}

@font_router.get(
    "/archives",
    tags=["Font"],
    summary="List all font archive types",
    description="Lists all archive types in which font files are available (e.g., zip, bz2, none). Use this to discover supported archive types for filtering or display.",
    openapi_extra={
        "x-agent-hints": "Call this endpoint to get all supported font archive types. Use the archive values in subsequent font file queries.",
        "x-mcp-example": {"name": "getFontArchives", "arguments": {}}
    },
    # operation_id removed
)
async def get_font_archives():
    archives = await get_all_font_archives()
    return {"code": 200, "status": "OK", "data": archives}

@font_router.get(
    "/categories",
    tags=["Font"],
    summary="List all font categories",
    description="Returns a list of all unique font categories. Useful for UIs, LLMs, and analytics.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to list all font categories.",
        "x-mcp-example": {"name": "getFontCategories", "arguments": {}}
    },
    responses=getFontCategoriesResponse
)
async def get_font_categories():
    categories = await get_all_font_categories()
    return {"code": 200, "status": "OK", "data": categories}



@font_router.get(
    "/{fontCode}",
    tags=["Font"],
    summary="Get font detail",
    description="Get font detail, files grouped by kind, and page range if available.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to get details for a specific font by code, including files and page range.",
        "x-mcp-example": {"fontCode": "digital-khatt-v1"}
    },
    responses=getFontDetailResponse
)
async def font_detail(
    fontCode: str = Path(..., alias="fontCode")
):
    font = await get_font_by_code(fontCode)
    if not font:
        return JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Font not found."})
    files = await get_font_files(font.font_id)
    files_by_kind = {k: [] for k in ["regular", "pack", "extras"]}
    for f in files:
        files_by_kind.setdefault(f.kind, []).append({"format": f.format, "url": f.url})
    page_range = await get_font_page_range(font.font_id)
    min_page, max_page = page_range if page_range else (None, None)
    return {
        "code": 200,
        "status": "OK",
        "data": {
            "code": font.code,
            "name": font.name,
            "category": font.category,
            "files": files_by_kind,
            "pageRange": {"min": min_page, "max": max_page} if min_page is not None else None
        }
    }

@font_router.get(
    "/{fontCode}/files",
    tags=["Font"],
    summary="List font files",
    description="List font files for a font. Filter by kind, format, archive.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to list all files for a specific font, with optional filtering by kind, format, or archive.",
        "x-mcp-example": {"fontCode": "digital-khatt-v1", "kind": "regular", "format": "ttf", "archive": "none"}
    },
    responses=getFontFilesResponse
)
async def font_files(
    fontCode: str = Path(..., alias="fontCode"),
    kind: str = Query(None, alias="kind"),
    format: str = Query(None, alias="format"),
    archive: str = Query(None, description="zip|bz2|none", alias="archive")
):
    font = await get_font_by_code(fontCode)
    if not font:
        return JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Font not found."})
    files = await get_font_files(font.font_id, kind, format, archive)
    return {
        "code": 200,
        "status": "OK",
        "data": [
            {"kind": f.kind, "format": f.format, "url": f.url} for f in files
        ]
    }

@font_router.get(
    "/{fontCode}/pages/{pageNumber}",
    tags=["Font"],
    summary="Get font page files",
    description="Get font page files for a given page (all formats).",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to get all font files for a specific page (all formats).",
        "x-mcp-example": {"fontCode": "digital-khatt-v1", "pageNumber": 1}
    },
    responses=getFontPageFilesResponse
)
async def font_page_files(
    fontCode: str = Path(..., alias="fontCode"),
    pageNumber: int = Path(..., ge=1, alias="pageNumber")
):
    font = await get_font_by_code(fontCode)
    if not font:
        return JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Font not found."})
    files = await get_font_page_files(font.font_id, page_number=pageNumber)
    if not files:
        return JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Font or page not found."})
    formats = {f.format: f.url for f in files}
    return {
        "code": 200,
        "status": "OK",
        "data": formats
    }

@font_router.get(
    "/{fontCode}/pages",
    tags=["Font"],
    summary="List font page files",
    description="Paginated list of font page files. Filter by format.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to list all font page files for a font, with pagination and optional format filter.",
        "x-mcp-example": {"fontCode": "digital-khatt-v1", "format": "ttf", "limit": 2, "offset": 0}
    },
    responses=getFontPageFilesResponse
)
async def list_font_page_files(
    fontCode: str = Path(..., alias="fontCode"),
    format: str = Query(None, alias="format"),
    limit: int = Query(20, ge=1, le=100, alias="limit"),
    offset: int = Query(0, ge=0, alias="offset")
):
    font = await get_font_by_code(fontCode)
    if not font:
        return JSONResponse(status_code=404, content={"code": 404, "status": "Not Found", "data": "Font not found."})
    result = await get_font_page_files(font.font_id, format=format, limit=limit, offset=offset)
    return {
        "code": 200,
        "status": "OK",
        "data": {
            "total": result["total"],
            "items": [
                {"pageNumber": f.page_number, "format": f.format, "url": f.url} for f in result["items"]
            ]
        }
    }
