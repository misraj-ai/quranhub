# routes/morphology_router.py
"""
Morphology Router - API endpoints for Quranic morphological analysis
Provides 12 endpoints for comprehensive morphological search and analysis
"""
from fastapi import APIRouter, Query, Path, Body
from fastapi.responses import JSONResponse
from typing import List, Optional
import urllib.parse

from utils.helpers import add_cache_headers
from repositories import morphology_repo
from utils.logger import logger
from .morphology_docs import (
    getWordMorphologyResponse,
    searchByTagsResponse,
    searchByCategoryResponse,
    searchByRootResponse,
    getAllRootsResponse,
    getAllTagsResponse,
    getTagDetailsResponse,
    getMorphologyStatsResponse,
    getSurahProfileResponse,
    searchByPatternResponse,
    compareWordsResponse,
    getAllCategoriesResponse,
    getAyahMorphologyResponse
)
from enum import Enum

# Enum for category validation
class MorphologyCategory(str, Enum):
    ROOT = "Root"
    SARF = "Sarf"
    IRAB = "Irab"
    AFAL = "Afal"
    LAWAHIQ = "Lawahiq"
    HOROF = "Horof"
    TAJWID = "Tajwid"
    ASMA = "Asma"
    AAM = "Aam"
    SAWABIQ = "Sawabiq"
    MONAWAEAT = "Monawaeat"

# Helper to sanitize cache tag for HTTP headers
def sanitize_cache_tag(tag: str) -> str:
    return urllib.parse.quote(tag, safe=":")


morphology_router = APIRouter()

@morphology_router.get(
    "/categories",
    responses=getAllCategoriesResponse,
    tags=["Morphology"],
    name="Get All Morphological Categories",
    description="Get list of all morphological categories with Arabic and English names.",
    openapi_extra={
        "x-agent-hints": "List all morphological categories available in the system with their names in Arabic and English, descriptions, and tag counts.",
        "x-mcp-example": {}
    }
)
async def get_all_categories():
    """
    Get list of all morphological categories.
    
    Returns:
    - 11 unique categories
    - Arabic and English names
    - Description of each category
    - Number of tags in each category
    
    Categories include:
    - Root (الجذور): Arabic root letters
    - Sarf (الصرف): Morphological patterns
    - Irab (الإعراب): Grammatical cases
    - Afal (الأفعال): Verb forms
    - Lawahiq (اللواحق): Suffixes
    - Horof (الحروف): Particles
    - Tajwid (التجويد): Recitation rules
    - Asma (الأسماء): Noun forms
    - Aam (عام): General markers
    - Sawabiq (السوابق): Prefixes
    - Monawaeat (المنوعات): Miscellaneous
    """
    try:
        logger.info("Get all categories request")
        
        # Get all categories
        data = await morphology_repo.get_all_categories()
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Get categories failed: {data}")
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
        cache_tag = "morphology:categories:all"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_all_categories: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response
    
# ============================================
# 1. GET WORD MORPHOLOGY BY LOCATION
# ============================================

@morphology_router.get(
    "/word/{location}",
    responses=getWordMorphologyResponse,
    tags=["Morphology"],
    name="Get Word Morphological Analysis",
    description="Get complete morphological breakdown for a specific word by its location (surah:ayah:position). Returns all morphological tags grouped by category with meanings.",
    openapi_extra={
        "x-agent-hints": "Use this to analyze the morphological structure of any word in the Quran. Location format: 'surah:ayah:position' (e.g., '1:1:1' for the first word of Al-Fatiha).",
        "x-mcp-example": {
            "location": "1:1:1",
            "category": "Root",
            "include_meaning": True
        }
    }
)
async def get_word_morphology(
    location: str = Path(
        ...,
        description="Word location in format 'surah:ayah:position'",
        example="1:1:1",
        pattern=r"^\d+:\d+:\d+$"
    ),
    category: Optional[MorphologyCategory] = Query(
        None,
        description="Filter tags by category (Root, Sarf, Irab, Afal, Lawahiq, Horof, Tajweed, Asma, Aam, Sawabiq, Monawaeat)",
        example="Root"
    ),
    include_meaning: bool = Query(
        True,
        description="Include tag meanings in response",
        example=True
    )
):
    """
    Get morphological analysis for a specific word.
    
    Location format: surah:ayah:position
    - surah: 1-114
    - ayah: verse number within surah
    - position: word position within verse (1-indexed)
    
    Example: "1:1:1" = first word of first verse of Al-Fatiha (بِسْمِ)
    """
    try:
        # Parse location
        parts = location.split(':')
        if len(parts) != 3:
            response = JSONResponse(
                content={
                    "code": 400,
                    "status": "Error",
                    "data": "Invalid location format. Use 'surah:ayah:position'"
                },
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        try:
            surah_id, ayah_number, position = map(int, parts)
        except ValueError:
            response = JSONResponse(
                content={
                    "code": 400,
                    "status": "Error",
                    "data": "Location parts must be numeric"
                },
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Validate ranges
        if not (1 <= surah_id <= 114):
            response = JSONResponse(
                content={
                    "code": 400,
                    "status": "Error",
                    "data": "Surah number must be between 1 and 114"
                },
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        logger.info(f"Morphology request: location={location}, category={category}")
        
        # Get morphology data
        data = await morphology_repo.get_word_morphology_by_location(
            surah_id=surah_id,
            ayah_number=ayah_number,
            position=position,
            category=category,
            include_meaning=include_meaning
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Morphology lookup failed: {data}")
            response = JSONResponse(
                content={"code": 404, "status": "Error", "data": data},
                status_code=404
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Success response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        cache_tag = f"morphology:word:{location}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_word_morphology: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 1.5 GET AYAH MORPHOLOGY BY REFERENCE
# ============================================

@morphology_router.get(
    "/ayah/{reference}",
    responses=getAyahMorphologyResponse,
    tags=["Morphology"],
    name="Get Ayah Morphological Analysis",
    description="Get complete morphological breakdown for all words in a specific ayah by its reference (surah:ayah or global number).",
    openapi_extra={
        "x-agent-hints": "Use this to analyze the morphological structure of an entire ayah. Reference format: 'surah:ayah' (e.g., '1:1') or global number (e.g., '1').",
        "x-mcp-example": {
            "reference": "1:1",
            "category": "Irab",
            "include_meaning": True
        }
    }
)
async def get_ayah_morphology(
    reference: str = Path(..., description="Ayah reference (surah:ayah or global number)", example="1:1"),
    category: Optional[MorphologyCategory] = Query(
        None,
        description="Filter tags by category",
        example="Irab"
    ),
    include_meaning: bool = Query(
        True,
        description="Include tag meanings in response",
        example=True
    )
):
    """
    Get morphological analysis for all words in an ayah.
    
    Reference can be:
    - surah:ayah (e.g., 1:1)
    - global ayah number (e.g., 1)
    """
    try:
        logger.info(f"Ayah morphology request: reference={reference}, category={category}")
        
        if ":" in reference:
            parts = reference.split(":")
            if len(parts) != 2:
                response = JSONResponse(
                    content={"code": 400, "status": "Error", "data": "Invalid reference format. Use 'surah:ayah'"},
                    status_code=400
                )
                response.headers["Cache-Control"] = "no-store"
                return response
            
            try:
                surah_id, ayah_number = map(int, parts)
                data = await morphology_repo.get_ayah_morphology(
                    surah_id=surah_id,
                    ayah_number=ayah_number,
                    category=category,
                    include_meaning=include_meaning
                )
            except ValueError:
                response = JSONResponse(
                    content={"code": 400, "status": "Error", "data": "Reference parts must be numeric"},
                    status_code=400
                )
                response.headers["Cache-Control"] = "no-store"
                return response
        elif reference.isdigit():
            data = await morphology_repo.get_ayah_morphology_by_id(
                ayah_id=int(reference),
                category=category,
                include_meaning=include_meaning
            )
        else:
            response = JSONResponse(
                content={"code": 400, "status": "Error", "data": "Invalid reference format. Use 'surah:ayah' or global number"},
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Ayah morphology lookup failed: {data}")
            status_code = 404 if "not found" in data.lower() else 400
            response = JSONResponse(
                content={"code": status_code, "status": "Error", "data": data},
                status_code=status_code
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Success response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        cache_tag = f"morphology:ayah:{reference}"
        if category:
            cache_tag += f":category:{category}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_ayah_morphology: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 2. SEARCH BY TAGS
# ============================================

@morphology_router.get(
    "/search/tags",
    responses=searchByTagsResponse,
    tags=["Morphology"],
    name="Search Words by Morphological Tags",
    description="Find words matching specific morphological tags. Supports AND/OR logic for multiple tags.",
    openapi_extra={
        "x-agent-hints": "Search for words with specific morphological features. Use match_all=true for words that have ALL tags (AND), or false for ANY tag (OR).",
        "x-mcp-example": {
            "tags": "فع,ضي",
            "match_all": True,
            "surah_number": 2,
            "limit": 20
        }
    }
)
async def search_by_tags(
    tags: str = Query(
        ...,
        description="Comma-separated list of tag codes to search for",
        example="فع,ضي"
    ),
    match_all: bool = Query(
        True,
        description="If true, word must have ALL tags (AND). If false, ANY tag (OR)",
        example=True
    ),
    surah_number: Optional[int] = Query(
        None,
        description="Filter by specific surah (1-114)",
        example=None,
        ge=1,
        le=114
    ),
    category: Optional[MorphologyCategory] = Query(
        None,
        description="Filter tags by category",
        example=None
    ),
    limit: int = Query(
        20,
        description="Maximum number of results",
        example=20,
        ge=1,
        le=100
    ),
    offset: int = Query(
        0,
        description="Offset for pagination",
        example=0,
        ge=0
    )
):
    """
    Search words by morphological tags.
    
    Examples:
    - tags="فع,ضي" with match_all=true → words that are verbs AND past tense
    - tags="فع,اسم" with match_all=false → words that are verbs OR nouns
    """
    try:
        # Parse tags
        tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        
        if not tag_list:
            response = JSONResponse(
                content={
                    "code": 400,
                    "status": "Error",
                    "data": "At least one tag is required"
                },
                status_code=400
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        logger.info(f"Tag search request: tags={tag_list}, match_all={match_all}, surah={surah_number}")
        
        # Search by tags
        data = await morphology_repo.search_words_by_tags(
            tags=tag_list,
            match_all=match_all,
            surah_number=surah_number,
            category=category,
            limit=limit,
            offset=offset
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Tag search failed: {data}")
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
        cache_tag = f"morphology:tags:{tags}:match_all:{match_all}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in search_by_tags: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 3. SEARCH BY CATEGORY
# ============================================

@morphology_router.get(
    "/search/category/{category}",
    responses=searchByCategoryResponse,
    tags=["Morphology"],
    name="Search Words by Tag Category",
    description="Find words with tags from a specific morphological category.",
    openapi_extra={
        "x-agent-hints": "Search for words by morphological category (Root, Sarf, Irab, etc.). Optionally filter by specific tag within category.",
        "x-mcp-example": {
            "category": "Afal",
            "tag_code": "فع",
            "surah_number": 1,
            "limit": 20
        }
    }
)
async def search_by_category(
    category: MorphologyCategory = Path(
        ...,
        description="Morphological category",
        example="Afal"
    ),
    tag_code: Optional[str] = Query(
        None,
        description="Specific tag code within category",
        example="فع"
    ),
    surah_number: Optional[int] = Query(
        None,
        description="Filter by specific surah (1-114)",
        example=None,
        ge=1,
        le=114
    ),
    limit: int = Query(
        20,
        description="Maximum number of results",
        example=20,
        ge=1,
        le=100
    ),
    offset: int = Query(
        0,
        description="Offset for pagination",
        example=0,
        ge=0
    )
):
    """
    Search words by morphological category.
    
    Valid categories:
    - Root: Arabic roots
    - Sarf: Morphological patterns
    - Irab: Grammatical case markers
    - Afal: Verb forms
    - Lawahiq: Suffixes
    - Horof: Particles
    - Tajweed: Tajweed rules
    - Asma: Noun forms
    - Aam: General markers
    - Sawabiq: Prefixes
    - Monawaeat: Prohibitions
    """
    try:
        logger.info(f"Category search request: category={category}, tag={tag_code}, surah={surah_number}")
        
        # Search by category
        data = await morphology_repo.search_words_by_category(
            category=category,
            tag_code=tag_code,
            surah_number=surah_number,
            limit=limit,
            offset=offset
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Category search failed: {data}")
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
        cache_tag = f"morphology:category:{category}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in search_by_category: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 4. SEARCH BY ROOT
# ============================================

@morphology_router.get(
    "/roots/{root}",
    responses=searchByRootResponse,
    tags=["Morphology"],
    name="Search Words by Arabic Root",
    description="Find all words derived from a specific Arabic root.",
    openapi_extra={
        "x-agent-hints": "Find all words derived from an Arabic root (e.g., 'كتب', 'حمد', 'رحم'). Returns root statistics and all derivative words.",
        "x-mcp-example": {
            "root": "حمد",
            "surah_number": None,
            "limit": 50
        }
    }
)
async def search_by_root(
    root: str = Path(
        ...,
        description="Arabic root (3 or 4 letter)",
        example="حمد"
    ),
    surah_number: Optional[int] = Query(
        None,
        description="Filter by specific surah (1-114)",
        example=None,
        ge=1,
        le=114
    ),
    limit: int = Query(
        50,
        description="Maximum number of results",
        example=50,
        ge=1,
        le=200
    ),
    offset: int = Query(
        0,
        description="Offset for pagination",
        example=0,
        ge=0
    )
):
    """
    Search for all words derived from a specific Arabic root.
    
    Returns:
    - Root information and statistics
    - All derivative words with their locations
    - Ayah context for each word
    """
    try:
        logger.info(f"Root search request: root={root}, surah={surah_number}")
        
        # Search by root
        data = await morphology_repo.search_words_by_root(
            root=root,
            surah_number=surah_number,
            limit=limit,
            offset=offset
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Root search failed: {data}")
            response = JSONResponse(
                content={"code": 404, "status": "Error", "data": data},
                status_code=404
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Success response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        cache_tag = f"morphology:root:{root}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in search_by_root: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 5. GET ALL ROOTS
# ============================================

@morphology_router.get(
    "/roots",
    responses=getAllRootsResponse,
    tags=["Morphology"],
    name="Get All Arabic Roots",
    description="Get list of all Arabic roots in the Quran with statistics.",
    openapi_extra={
        "x-agent-hints": "List all Arabic roots found in the Quran. Sort by frequency or alphabetically. Filter by minimum occurrence count.",
        "x-mcp-example": {
            "sort_by": "frequency",
            "min_occurrences": 1,
            "limit": 50
        }
    }
)
async def get_all_roots(
    sort_by: str = Query(
        "frequency",
        description="Sort order: 'frequency' (most common first) or 'alphabetical'",
        example="frequency",
        regex="^(frequency|alphabetical)$"
    ),
    min_occurrences: int = Query(
        1,
        description="Minimum word count to include",
        example=1,
        ge=1
    ),
    limit: int = Query(
        50,
        description="Maximum number of results",
        example=50,
        ge=1,
        le=200
    ),
    offset: int = Query(
        0,
        description="Offset for pagination",
        example=0,
        ge=0
    )
):
    """
    Get list of all Arabic roots in the Quran.
    
    Returns ~1,805 unique roots with statistics:
    - Root occurrence count
    - Number of surahs containing the root
    - Sorted by frequency or alphabetically
    """
    try:
        logger.info(f"Get all roots request: sort={sort_by}, min={min_occurrences}")
        
        # Get all roots
        data = await morphology_repo.get_all_roots(
            sort_by=sort_by,
            min_occurrences=min_occurrences,
            limit=limit,
            offset=offset
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Get all roots failed: {data}")
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
        cache_tag = f"morphology:roots:all:{sort_by}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_all_roots: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 6. GET ALL TAGS
# ============================================

@morphology_router.get(
    "/tags",
    responses=getAllTagsResponse,
    tags=["Morphology"],
    name="Get All Morphological Tags",
    description="Get list of all morphological tags (2,468 total) with usage statistics.",
    openapi_extra={
        "x-agent-hints": "List all morphological tags. Filter by category or search in code/meaning. Returns category counts.",
        "x-mcp-example": {
            "category": "Root",
            "search": "فعل",
            "limit": 100
        }
    }
)
async def get_all_tags(
    category: Optional[MorphologyCategory] = Query(
        None,
        description="Filter by category",
        example=None
    ),
    search: Optional[str] = Query(
        None,
        description="Search in tag code or meaning",
        example=None
    ),
    limit: int = Query(
        100,
        description="Maximum number of results",
        example=100,
        ge=1,
        le=500
    ),
    offset: int = Query(
        0,
        description="Offset for pagination",
        example=0,
        ge=0
    )
):
    """
    Get list of all morphological tags in the system.
    
    Returns:
    - 2,468 unique morphological tags
    - Usage count for each tag
    - Category distribution
    - Searchable by code or meaning
    """
    try:
        logger.info(f"Get all tags request: category={category}, search={search}")
        
        # Get all tags
        data = await morphology_repo.get_all_tags(
            category=category,
            search=search,
            limit=limit,
            offset=offset
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Get all tags failed: {data}")
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
        cache_tag = f"morphology:tags:all"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_all_tags: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 7. GET TAG DETAILS
# ============================================

@morphology_router.get(
    "/tags/{tag_code}",
    responses=getTagDetailsResponse,
    tags=["Morphology"],
    name="Get Tag Details",
    description="Get detailed information about a specific morphological tag including statistics, related tags, and examples.",
    openapi_extra={
        "x-agent-hints": "Get comprehensive information about a specific tag: statistics, related tags that commonly appear with it, and example words.",
        "x-mcp-example": {
            "tag_code": "فع"
        }
    }
)
async def get_tag_details(
    tag_code: str = Path(
        ...,
        description="Morphological tag code",
        example="فع"
    )
):
    """
    Get detailed information about a specific morphological tag.
    
    Returns:
    - Tag information (code, meaning, category)
    - Usage statistics (word count, surah count, percentage)
    - Related tags (co-occurrence analysis)
    - Example words with context
    """
    try:
        logger.info(f"Get tag details request: tag={tag_code}")
        
        # Get tag details
        data = await morphology_repo.get_tag_details(tag_code=tag_code)
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Get tag details failed: {data}")
            response = JSONResponse(
                content={"code": 404, "status": "Error", "data": data},
                status_code=404
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Success response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        cache_tag = f"morphology:tag:{tag_code}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_tag_details: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 8. GET MORPHOLOGY STATISTICS
# ============================================

@morphology_router.get(
    "/stats",
    responses=getMorphologyStatsResponse,
    tags=["Morphology"],
    name="Get Morphology Statistics",
    description="Get overall morphological statistics for the Quran or specific surah.",
    openapi_extra={
        "x-agent-hints": "Get comprehensive statistics about morphological features in the Quran. Optionally filter by surah or category.",
        "x-mcp-example": {
            "surah_number": None,
            "category": None
        }
    }
)
async def get_morphology_stats(
    surah_number: Optional[int] = Query(
        None,
        description="Filter by specific surah (1-114)",
        example=None,
        ge=1,
        le=114
    ),
    category: Optional[MorphologyCategory] = Query(
        None,
        description="Filter by tag category",
        example=None
    )
):
    """
    Get comprehensive morphological statistics.
    
    Returns:
    - Overview: total words, coverage, average tags per word
    - Category breakdown: unique tags and occurrences per category
    - Top roots: most frequently used roots
    - Top tags: most frequently used morphological tags
    """
    try:
        logger.info(f"Get stats request: surah={surah_number}, category={category}")
        
        # Get statistics
        data = await morphology_repo.get_morphology_statistics(
            surah_number=surah_number,
            category=category
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Get stats failed: {data}")
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
        cache_tag = f"morphology:stats"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_morphology_stats: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 9. GET SURAH MORPHOLOGY PROFILE
# ============================================

@morphology_router.get(
    "/stats/surah/{surah_number}",
    responses=getSurahProfileResponse,
    tags=["Morphology"],
    name="Get Surah Morphological Profile",
    description="Get detailed morphological analysis for a specific surah.",
    openapi_extra={
        "x-agent-hints": "Analyze the morphological characteristics of a specific surah: root diversity, verb tense distribution, complexity score.",
        "x-mcp-example": {
            "surah_number": 1
        }
    }
)
async def get_surah_profile(
    surah_number: int = Path(
        ...,
        description="Surah number (1-114)",
        example=1,
        ge=1,
        le=114
    )
):
    """
    Get morphological profile for a specific surah.
    
    Returns:
    - Surah information
    - Unique root count
    - Most common root
    - Verb tense distribution
    - Linguistic complexity score
    """
    try:
        logger.info(f"Get surah profile request: surah={surah_number}")
        
        # Get surah profile
        data = await morphology_repo.get_surah_morphology_profile(
            surah_number=surah_number
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Get surah profile failed: {data}")
            response = JSONResponse(
                content={"code": 404, "status": "Error", "data": data},
                status_code=404
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Success response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        cache_tag = f"morphology:surah:{surah_number}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in get_surah_profile: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 10. SEARCH BY PATTERN
# ============================================

@morphology_router.get(
    "/patterns/{pattern}",
    responses=searchByPatternResponse,
    tags=["Morphology"],
    name="Search Words by Morphological Pattern",
    description="Find words matching a specific morphological pattern (وزن).",
    openapi_extra={
        "x-agent-hints": "Search for words matching Arabic morphological patterns like 'فَعَلَ', 'فَاعِل', 'مَفْعُول'.",
        "x-mcp-example": {
            "pattern": "فَعَلَ",
            "surah_number": None,
            "limit": 50
        }
    }
)
async def search_by_pattern(
    pattern: str = Path(
        ...,
        description="Arabic morphological pattern (وزن)",
        example="فَعَلَ"
    ),
    surah_number: Optional[int] = Query(
        None,
        description="Filter by specific surah (1-114)",
        example=None,
        ge=1,
        le=114
    ),
    limit: int = Query(
        50,
        description="Maximum number of results",
        example=50,
        ge=1,
        le=200
    ),
    offset: int = Query(
        0,
        description="Offset for pagination",
        example=0,
        ge=0
    )
):
    """
    Search for words matching a morphological pattern (وزن).
    
    Common patterns:
    - فَعَلَ (fa'ala): basic past tense verb
    - فَاعِل (faa'il): active participle
    - مَفْعُول (maf'ool): passive participle
    - فَعِيل (fa'eel): intensive adjective
    """
    try:
        logger.info(f"Pattern search request: pattern={pattern}, surah={surah_number}")
        
        # Search by pattern
        data = await morphology_repo.search_words_by_pattern(
            pattern=pattern,
            surah_number=surah_number,
            limit=limit,
            offset=offset
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Pattern search failed: {data}")
            response = JSONResponse(
                content={"code": 404, "status": "Error", "data": data},
                status_code=404
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Success response
        response = JSONResponse(
            content={"code": 200, "status": "OK", "data": data},
            status_code=200
        )
        cache_tag = f"morphology:pattern:{pattern}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in search_by_pattern: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


# ============================================
# 11. COMPARE WORDS
# ============================================

@morphology_router.get(
    "/compare",
    responses=compareWordsResponse,
    tags=["Morphology"],
    name="Compare Words Morphologically",
    description="Compare morphological features of multiple words.",
    openapi_extra={
        "x-agent-hints": "Compare the morphological structure of 2 or more words. Returns common tags, unique tags for each word, and similarity score.",
        "x-mcp-example": {
            "words": ["1:1:1", "1:2:1", "2:5:3"]
        }
    }
)
async def compare_words(
    words: str = Query(
        ...,
        description="Comma-separated list of word locations in format 'surah:ayah:position'",
        example="1:1:1,1:2:1,2:5:3",
    )
):
    """
    Compare morphological features of multiple words.
    
    Returns:
    - Word information for each location
    - Common tags (intersection)
    - Unique tags for each word
    - Jaccard similarity score (0-100)
    
    Example:
```json
    {
        "words": ["1:1:1", "1:2:1", "2:5:3"]
    }
```
    """
    try:
        word_locations=[w.strip() for w in words.split(',') if w.strip()]
        # Validate format
        for word_loc in word_locations:
            parts = word_loc.split(':')
            if len(parts) != 3:
                response = JSONResponse(
                    content={
                        "code": 400,
                        "status": "Error",
                        "data": f"Invalid location format: {word_loc}. Use 'surah:ayah:position'"
                    },
                    status_code=400
                )
                response.headers["Cache-Control"] = "no-store"
                return response
        
        logger.info(f"Compare words request: words={words}")
        
        # Compare words
        data = await morphology_repo.compare_words_morphology(
            word_locations=word_locations
        )
        
        # Handle error responses
        if isinstance(data, str):
            logger.error(f"Compare words failed: {data}")
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
        cache_tag = f"morphology:compare:{':'.join(words)}"
        add_cache_headers(response, cache_tag=sanitize_cache_tag(cache_tag))
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in compare_words: {str(e)}", exc_info=True)
        response = JSONResponse(
            content={"code": 500, "status": "Error", "data": "Something went wrong"},
            status_code=500
        )
        response.headers["Cache-Control"] = "no-store"
        return response


