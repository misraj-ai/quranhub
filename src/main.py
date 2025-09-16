from fastapi import FastAPI, HTTPException, Response
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
import typing as t
from routers.edition.edition_router import edition_router
from routers.ruku.ruku_router import ruku_router
from routers.page.page_router import page_router
from routers.narrations_differences.narrations_differences_router import narrations_differences_router
from routers.hizb.hizb_router import hizb_router
from routers.hizb_quarter.hizb_quarter_router import hizb_quarter_router
from routers.sajda.sajda_router import sajda_router
from routers.meta.meta_router import meta_router
from routers.manzil.manzil_router import manzil_router
from routers.search.search_router import search_router
from routers.ayah.ayah_router import ayah_router
from routers.surah.surah_router import surah_router
from routers.juz.juz_router import juz_router
from routers.quran.quran_router import quran_router
from routers.word.word_router import word_router
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
import logging
import cachetools
import json
from starlette.middleware.base import BaseHTTPMiddleware
import re
# Routers (all imports at top)
from routers.mutashabihat.mutashabihat_router import mutashabihat_router
from routers.similar_ayah.similar_ayah_router import similar_ayah_router
from routers.ayah_theme.ayah_theme_router import ayah_theme_router
from routers.font.font_router import font_router
from routers.mushaf_layout.mushaf_layout_router import mushaf_layout_router

# Global cache
cache = cachetools.TTLCache(maxsize=100, ttl=86400)

class CacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cache_key = str(request.url)

        # Define a regular expression pattern to match paths that contain any of the words
        skip_patterns = re.compile(r"(docs|openapi\.json|random|health|liveness|startup)", re.IGNORECASE)

        # If the path matches the regular expression, skip caching
        if skip_patterns.search(request.url.path):
            return await call_next(request)

        # Check cache
        cached_response = cache.get(cache_key)
        if cached_response:
            return JSONResponse(content=json.loads(cached_response), status_code=200)

        # Process request
        response = await call_next(request)

        try:
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            cache[cache_key] = response_body

            response_data = json.loads(response_body.decode('utf-8'))
            return JSONResponse(content=response_data, status_code=response.status_code)

        except Exception as e:
            # Log unexpected exceptions
            logger.debug(f"Exception in CacheMiddleware: {e}")
            # Return the original response if anything fails
            return response




#-----

tags_metadata = [
    {"name": "Edition", "description": "Available text and audio editions - All these endpoints give you a JSON object describing an edition. From this object, you need to use the identifier to get data from other endpoints in this API. For any of the endpoints that require an edition identifier, if you do not specify one, 'quran-simple' is used and returns the Arabic text of the Holy Quran."},
    {"name": "Ruku", "description": "Get a Ruku of the Quran - The Quran has 556 Rukus. You can get the text for each Ruku using the endpoints below."},
    {"name": "Page", "description": "Get a Page of the Quran - The Quran is traditionally printed / written on 604 pages. You can get the text for each page using the endpoints below."},
    {"name": "Narrations Differences", "description": "Get Narrations Differences from Ayahs in a Page."},
    {"name": "HizbQuarter", "description": "Get a Hizb Quarter of the Quran - The Quran comprises 240 Hizb Quarters. One Hizb is half a Juz."},
    {"name": "Hizb", "description": "Get a Hizb of the Quran - The Quran comprises 60 Hizbs. One Hizb is half a Juz."},
    {"name": "Sajda", "description": "Get all verses requiring Sajda / Prostration in the Quran - Depending on the madhab, there can be 14, 15 or 16 sajdas. This API has 15."},
    {"name": "Meta", "description": "Get meta data about Surahs, Pages, Hizbs and Juzs."},
    {"name": "Manzil", "description": "Get a Manzil of the Quran - The Quran has 7 Manzils (for those who want to read / recite it over one week). You can get the text for each Manzil using the endpoints below."},
    {"name": "Search", "description": "Search the text of the Quran - Please note that only text editions of the Quran are searchable."},
    {"name": "Ayah", "description": "Get an Ayah of the Quran - The Quran contains 6236 verses. With this endpoint, you can retrieve any of those verses."},
    {"name": "Surah", "description": "Get a Surah of the Quran - The Quran has 114 Surahs. You can get a list of all of them or all the ayahs for a particular surah using the endpoints below."},
    {"name": "Juz", "description": "Get a Juz of the Quran - The Quran has 30 Juz. You can get the text for each Juz using the endpoints below."},
    {"name": "Quran", "description": "Get a complete Quran edition - NOTE that audio and text edition responses differ. See examples for the response."},
    {"name": "Word", "description": "Get word-level resources such as tajweed rules, line numbers, and per-word images by location (surah:ayah:position)."},
    {"name": "Ayah Theme", "description": "Core themes and topics of each ayah in the Quran."},
    {"name": "Mutashabihat", "description": "Similarities in meaning, context, or wording among ayah phrases in the Quran."},
    {"name": "Similar Ayah", "description": "Ayahs from the Quran that share similarities in meaning, context, or wording. This data allows you to explore and access Ayahs that closely align with each other."},
    {"name": "Font", "description": "Font metadata, font files, and per-page font resources for Quranic scripts."},
    {"name": "Mushaf Layout", "description": "Mushaf layout metadata, page/line structure, and surah/word lookups for Quranic pages."},
]
async def lifespan(app: FastAPI):
    # Startup event: clear cache
    try:
        cache.clear()  # Clear in-memory cache
        logger.info("Cache cleared on application startup.")
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
    
    # Yield control back to FastAPI
    yield

app = FastAPI(
    title="Quran Hub API",
    description="Quran Hub API Documentation",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)
# Add the CacheMiddleware to the app
app.add_middleware(CacheMiddleware)  
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Construct dynamic message based on msg and input
    error_details = []
    for error in errors:
        msg = error.get('msg', 'Validation error')
        input_value = error.get('loc', [])[-1]  # Get the last item in loc as the input field
        error_message = f"{msg} [{input_value}]"
        error_details.append(error_message)

    # Join the list of error messages into a single string, separated by commas
    error_message_str = ', '.join(error_details)

    return JSONResponse(
        status_code=422,
        content={
            "status": "Error",
            "data": "Something wrong happened: "+error_message_str,  # Joined string of error messages
            "code": 422
        }
    )


def custom_openapi():
    app.openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    for _, method_item in app.openapi_schema.get('paths').items():
        for _, param in method_item.items():
            responses = param.get('responses')
            # remove 422 response, also can remove other status code
            if '422' in responses:
                del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health/startup", include_in_schema=False)
async def startup_probe():
    logger.debug("Startup probe triggered")
    return {"status": "OK"}

@app.get("/health/liveness", include_in_schema=False)
async def liveness_probe():
    logger.debug("Liveness probe triggered")
    return {"status": "OK"}

@app.get("/health/readiness", include_in_schema=False)
async def readiness_probe():
    logger.debug("Readiness probe triggered")
    return {"status": "OK"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail,"status":False},
    )

@app.get('/')
async def get_response():
  try:
    return JSONResponse(content={"message":"Success"}, status_code=200)
  except Exception as e:
    logger.error("An exception occurred: %s", str(e))
    response= {
    "status": False,
    "message": "Something Went Wrong, Please try again later",
    "code":500
    }
    return JSONResponse(content=response, status_code=500)



# Register all routers (grouped for clarity, after all imports)
app.include_router(edition_router, prefix="/v1/edition")
app.include_router(ruku_router, prefix="/v1/ruku")
app.include_router(page_router, prefix="/v1/page")
app.include_router(narrations_differences_router, prefix="/v1/narrations-differences")
app.include_router(hizb_router, prefix="/v1/hizb")
app.include_router(hizb_quarter_router, prefix="/v1/hizbQuarter")
app.include_router(sajda_router, prefix="/v1/sajda")
app.include_router(meta_router, prefix="/v1/meta")
app.include_router(manzil_router, prefix="/v1/manzil")
app.include_router(search_router, prefix="/v1/search")
app.include_router(ayah_router, prefix="/v1/ayah")
app.include_router(surah_router, prefix="/v1/surah")
app.include_router(juz_router, prefix="/v1/juz")
app.include_router(word_router, prefix="/v1/word")
app.include_router(quran_router, prefix="/v1/quran")


app.include_router(mutashabihat_router, prefix="/v1/mutashabihat")
app.include_router(similar_ayah_router, prefix="/v1/similar-ayah")
app.include_router(ayah_theme_router, prefix="/v1/ayah-theme")
app.include_router(font_router, prefix="/v1/font")
app.include_router(mushaf_layout_router, prefix="/v1/mushaf-layouts")


excluded_keywords = ["health", "liveness", "startup"]

class EndpointFilter(logging.Filter):
    def __init__(self, excluded_keywords: list):
        super().__init__()
        self.excluded_keywords = excluded_keywords

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            message = record.getMessage()
            for keyword in self.excluded_keywords:
                if keyword in message:
                    return False  # Suppress log
            return True  # Allow other logs
        except Exception:
            return True  # Fail safe: log everything if error



uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(EndpointFilter(excluded_keywords))


@app.get("/health/startup", include_in_schema=False)
async def startup_probe():
    logger.debug("Startup probe triggered")
    return {"status": "OK"}

@app.get("/health/liveness", include_in_schema=False)
async def liveness_probe():
    logger.debug("Liveness probe triggered")
    return {"status": "OK"}

@app.get("/health/readiness", include_in_schema=False)
async def readiness_probe():
    logger.debug("Readiness probe triggered")
    return {"status": "OK"}


# Main entry point for running the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)

