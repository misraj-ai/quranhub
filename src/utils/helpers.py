from utils.config import BUNNY_URL
from typing import List, Tuple
from utils.logger import logger
from fastapi.responses import JSONResponse
from typing import Optional

def add_cache_headers(response: JSONResponse, cache_duration: int = 2592000, browser_cache: int = 3600, cache_tag: Optional[str] = None):
    """
    Add Cloudflare-optimized cache headers to response
    
    Args:
        response: The JSONResponse object
        cache_duration: Edge cache TTL in seconds (default: 30 days)
        browser_cache: Browser cache TTL in seconds (default: 7 days)
        cache_tag: Optional Cloudflare cache tag for targeted purging
    """
    # Main cache control header - tells Cloudflare to cache this
    response.headers["Cache-Control"] = f"public, max-age={cache_duration}, s-maxage={cache_duration}, stale-while-revalidate=86400"
    
    # CDN-Cache-Control for Cloudflare specifically (overrides Cache-Control for CF only)
    response.headers["CDN-Cache-Control"] = f"max-age={cache_duration}"
    
    # Cloudflare Browser Cache TTL
    response.headers["Cloudflare-CDN-Cache-Control"] = f"max-age={cache_duration}, browser-max-age={browser_cache}"
    
    # Add cache tag for targeted purging if provided
    if cache_tag:
        response.headers["Cache-Tag"] = cache_tag
    
    # Vary header for proper caching with different formats
    response.headers["Vary"] = "Accept-Encoding"
    
    return response

def get_ayah_audio_url(bitrate, edition_identifier, ayah_number):
    return f"{BUNNY_URL}/audio/versebyverse/{bitrate}/{edition_identifier}/{ayah_number}.mp3"
    
def get_ayah_audio_secondary_urls(bitrates, edition_identifier, ayah_number):
    return [f"{BUNNY_URL}/audio/versebyverse/{bitrate}/{edition_identifier}/{ayah_number}.mp3" for bitrate in bitrates]

def get_surah_audio_url(bitrate, edition_identifier, ayah_number):
    return f"{BUNNY_URL}/audio/surah/{bitrate}/{edition_identifier}/{ayah_number}.mp3"
    
def get_surah_audio_secondary_urls(bitrates, edition_identifier, ayah_number):
    return [f"{BUNNY_URL}/audio/surah/{bitrate}/{edition_identifier}/{ayah_number}.mp3" for bitrate in bitrates]


def find_indices(string, substring):
    try:
        words = string.split()
        sub_words = substring.split()
        indices = []

        # Find exact matches for the entire substring
        for i in range(len(words) - len(sub_words) + 1):
            if words[i:i + len(sub_words)] == sub_words:
                indices.extend(range(i, i + len(sub_words)))

        # If no exact match is found, try to find closest match
        if not indices:
            index_of_first_word = None
            index_of_second_word = None
            
            # Find the index of the first word of the substring
            try:
                index_of_first_word = words.index(sub_words[0])
            except ValueError:
                pass

            # Find the index of the second word of the substring
            try:
                index_of_second_word = words.index(sub_words[1])
            except ValueError:
                pass

            # Adjust indices if possible
            if index_of_first_word is not None and index_of_second_word is None:
                index_of_second_word = index_of_first_word + 1 if index_of_first_word + 1 < len(words) else len(words) - 1

            elif index_of_second_word is not None and index_of_first_word is None:
                index_of_first_word = index_of_second_word - 1 if index_of_second_word - 1 >= 0 else 0

            # Add adjusted indices
            if index_of_first_word is not None and index_of_second_word is not None:
                indices.extend([index_of_first_word, index_of_second_word])

        # Return the result as a list of words with their indices
        return [{'word': words[i], 'index': i} for i in indices]

    except Exception as e:
        logger.error("An exception occurred: %s", str(e), exc_info=True)
        return []


def custom_sort(item):
    if item['words']:
        location_parts = list(map(int, item['words'][0]['location'].split(':')))
        return tuple(location_parts)
    else:
        return (float('inf'), float('inf'), float('inf'))

def remove_extra_spaces(input_string):
    words = input_string.split()
    result_string = ' '.join(words)
    return result_string