# routes/search_router.py
from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse
from utils.helpers import add_cache_headers
from repositories import keyword_repo  # Using the refactored repository
from .search_docs import getKeywordbySurahAndLanguageOrEditionResponse
from utils.logger import logger 
import urllib.parse

    # Helper to sanitize cache tag for HTTP headers (percent-encode non-ASCII)
def sanitize_cache_tag(tag: str) -> str:
    return urllib.parse.quote(tag, safe=":")  # keep colons for readability

search_router = APIRouter()

@search_router.get(
    "/{keyword}",
    responses=getKeywordbySurahAndLanguageOrEditionResponse,
    tags=["Search"],
    name="Search the text of the Quran by Keyword and Surah Number and (Edition or Language)",
    description="Search the Quran for ayahs (verses) matching a keyword, with support for language detection, edition selection, exact/fuzzy matching, and Surah filtering. Returns detailed scoring and metadata for each match. Useful for LLMs, search UIs, and advanced workflows.",
    openapi_extra={
        "x-agent-hints": "Use this endpoint to search the Quran by keyword, with options for language, edition, Surah, and exact/fuzzy matching. Returns ayahs with scoring and metadata.",
        "x-mcp-example": {
            "keyword": "الحمد لله",
            "language": "ar",
            "edition": "quran-simple-clean",
            "surahNumber": 1,
            "exactSearch": True,
            "limit": 5,
            "offset": 0
        }
    }
)
async def search_quran_by_keyword(
    keyword: str = Path(..., description="Keyword to search in the Quran text", example="الحمد لله"),
    language: str = Query(None, description="Language code like 'en', 'ar', etc."),
    editionIdentifier: str = Query(None, description="Edition identifier like 'en.sahih', 'quran-simple-clean', etc."),
    surahNumber: int = Query(None, description="Surah number (1-114)", ge=1, le=114),
    exactSearch: bool = Query(True, description="Exact search match required or not", example=True),
    limit: int = Query(10, description="Number of ayahs to limit the response to.", example=10, le=20),
    offset: int = Query(0, description="Offset ayahs by the given number.", example=0, ge=0)
):
    """
    Enhanced search endpoint with pg_trgm support
    
    Features:
    - Automatic language detection (Arabic vs English)
    - Arabic text normalization (removes diacritics)
    - Exact search: Uses LIKE for substring matching
    - Fuzzy search: Uses pg_trgm for similarity matching
    - Multi-word support in fuzzy search
    - Returns verses from specified edition or default editions
    """
    try:
        # Validate Surah number if provided
        if surahNumber and (surahNumber < 1 or surahNumber > 114):
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Surah number should be between 1 and 114"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Log search request for monitoring
        logger.info(f"Search request: keyword='{keyword}', exact={exactSearch}, surah={surahNumber}, edition={editionIdentifier}")
        
        # Determine default edition based on keyword language if no edition specified
        if not editionIdentifier:
            # Simple Arabic detection - if contains Arabic characters, use Arabic edition
            import re
            is_arabic = bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', keyword))
            if is_arabic:
                edition_id = "quran-simple-clean"  # Default Arabic edition
            else:
                edition_id = "en.sahih"  # Default English edition (ID: 20)
        else:
            edition_id = editionIdentifier
        
        # Use enhanced search function directly for full similarity scoring
        data = await keyword_repo.search_ayahs_by_keyword(
            keyword=keyword,
            edition_identifier=edition_id,
            exact_search=exactSearch,
            limit=limit,
            offset=offset
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Search failed: {data}")
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": data},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        # Success response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        cache_tag = f"search:{keyword}:edition:{edition_id}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error during search: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response