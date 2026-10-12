from utils.config import (
    BUNNY_URL,
    AUDIO_TYPE_VERSEBYVERSE,
    AUDIO_TYPE_WORDBYWORD,
    WORDBYWORD_MISSING_AUDIO,
    WORDBYWORD_POSITION_ALIASES,
)
from typing import List, Tuple
from utils.logger import logger
from utils.word_numbering import global_word_number
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


def get_word_audio_url(bitrate, edition_identifier, word_number):
    """Per-word audio URL keyed by the global word number (1..77432), like ayah audio by global ayah number."""
    return f"{BUNNY_URL}/audio/wordbyword/{bitrate}/{edition_identifier}/{word_number}.mp3"


def get_word_audio_secondary_urls(bitrates, edition_identifier, word_number):
    return [get_word_audio_url(bitrate, edition_identifier, word_number) for bitrate in bitrates]


def split_bitrates(bitrates):
    """Return (max_bitrate, remaining_bitrates) for an edition's bitrate list."""
    max_bitrate = max(bitrates)
    return max_bitrate, [bitrate for bitrate in bitrates if bitrate != max_bitrate]


def has_ayah_audio(edition) -> bool:
    """True only for audio editions whose files are split per ayah (verse-by-verse).

    Surah-only and word-by-word editions have no per-ayah files, so building
    verse-by-verse URLs for them would return links to files that don't exist.
    """
    return (
        edition is not None
        and edition.format == "audio"
        and edition.type == AUDIO_TYPE_VERSEBYVERSE
        and bool(edition.bitrates)
    )


def add_ayah_audio(ayah: dict, edition, ayah_number) -> None:
    """Attach `audio`/`audioSecondary` URLs to an ayah dict when the edition has per-ayah audio."""
    if not has_ayah_audio(edition):
        return
    max_bitrate, remaining_bitrates = split_bitrates(edition.bitrates)
    ayah["audio"] = get_ayah_audio_url(max_bitrate, edition.identifier, ayah_number)
    ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, edition.identifier, ayah_number)


def has_word_audio(edition) -> bool:
    return (
        edition is not None
        and edition.format == "audio"
        and edition.type == AUDIO_TYPE_WORDBYWORD
        and bool(edition.bitrates)
    )


def add_word_audio(word: dict, edition, surah_number, ayah_number, position) -> None:
    """Attach `number` (global word number) and `audio`/`audioSecondary` URLs for a word-by-word audio edition.

    Words with no source recording get `audio: None` so clients don't request a missing file.
    """
    if not has_word_audio(edition):
        return
    location = f"{surah_number}:{ayah_number}:{position}"
    alias = WORDBYWORD_POSITION_ALIASES.get(location)
    if alias:
        surah_number, ayah_number, position = (int(part) for part in alias.split(":"))
    number = global_word_number(surah_number, ayah_number, position)
    if number is None:
        logger.warning(f"No global word number for {location}; word audio omitted")
        return
    word["number"] = number
    if location in WORDBYWORD_MISSING_AUDIO:
        word["audio"] = None
        word["audioSecondary"] = []
        return
    max_bitrate, remaining_bitrates = split_bitrates(edition.bitrates)
    word["audio"] = get_word_audio_url(max_bitrate, edition.identifier, number)
    word["audioSecondary"] = get_word_audio_secondary_urls(remaining_bitrates, edition.identifier, number)


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