# repositories/keyword_repo.py — Enhanced Quran Search with pg_trgm
from __future__ import annotations

import re
import unicodedata
from typing import List, Optional

import pyarabic.araby as araby
from sqlalchemy import and_, or_, text
from sqlalchemy.future import select
from sqlalchemy.sql import func

from db.models import Surat, Ayat, Edition
from db.session import AsyncSessionLocal
from repositories.edition_repo import get_edition_by_identifier, get_text_edition_for_narrator
from repositories.narrations_numbering_repo import get_narration_numbering_from_narration
from utils.config import DEFAULT_EDITION_IDENTIFIER
from utils.helpers import get_ayah_audio_url, get_ayah_audio_secondary_urls
from utils.logger import logger


# Constants
CLEAN_ARABIC_EDITION_ID = 78  # quran-simple-clean edition for Arabic search


def is_arabic_text(keyword: str) -> bool:
    """Check if text contains Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', keyword or ''))


def normalize_arabic_text(text: str) -> str:
    """Normalize Arabic text for search by removing diacritics and extra spaces."""
    if not text:
        return text
    
    # Remove diacritics and tashkeel
    text = araby.strip_diacritics(text)
    text = araby.strip_tatweel(text)
    text = araby.normalize_ligature(text)
    text = araby.normalize_hamza(text)
    
    # Normalize Unicode
    text = unicodedata.normalize('NFKC', text)
    
    # Normalize common letter variations
    text = (text
            .replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ٱ', 'ا')
            .replace('ى', 'ي').replace('ئ', 'ي')
            .replace('ؤ', 'و')
            .replace('ة', 'ه'))  # Normalize taa marbuta to haa
    
    # Clean up spaces and punctuation
    text = re.sub(r'[،؛؟!\.\,\;\?]', '', text)
    text = re.sub(r'\s+', ' ', text.strip())
    
    return text


def normalize_non_arabic_text(text: str) -> str:
    """Normalize non-Arabic text for search."""
    return re.sub(r'\s+', ' ', text.strip().lower())


async def search_ayahs_by_keyword(
    keyword: str,
    edition_identifier: str = DEFAULT_EDITION_IDENTIFIER,
    exact_search: bool = False,
    limit: int = 20,
    offset: int = 0
):
    """
    Enhanced search function supporting both Arabic and non-Arabic text with fuzzy matching.
    
    Args:
        keyword: Search term (Arabic or non-Arabic)
        edition_identifier: Target edition for results
        exact_search: True for exact matching, False for fuzzy/typo-tolerant search
        limit: Maximum number of results
        offset: Offset for pagination
        
    Returns:
        Dictionary with search results
    """
    try:
        # Determine language and normalize search text
        is_arabic = is_arabic_text(keyword)
        
        # Get target edition for results first (needed for non-Arabic search edition)
        target_edition = await get_edition_by_identifier(edition_identifier)
        if isinstance(target_edition, str):
            return target_edition
        elif isinstance(target_edition, list):
            target_edition = target_edition[0] if target_edition[0].type == "versebyverse" else target_edition[1]
        
        target_edition_id = target_edition.id
        
        # Handle audio editions - use narrator-specific text edition
        if target_edition.format == "audio":
            text_edition = await get_text_edition_for_narrator(target_edition.identifier)
            if isinstance(text_edition, str):
                return text_edition
            target_edition_id = text_edition.id
        
        if is_arabic:
            normalized_keyword = normalize_arabic_text(keyword)
            search_edition_id = CLEAN_ARABIC_EDITION_ID
        else:
            normalized_keyword = normalize_non_arabic_text(keyword)
            # For non-Arabic text, use the requested edition for search
            # This supports multiple languages (English, French, Spanish, etc.)
            search_edition_id = target_edition_id
        
        async with AsyncSessionLocal() as session:
            # Search on the appropriate edition (clean Arabic or English)
            if exact_search:
                # Exact search using simple text matching
                search_query = text("""
                    SELECT DISTINCT a.surat_id, a.numberinsurat, a.number
                    FROM quranhub_schema.ayat a
                    WHERE a.edition_id = :search_edition_id
                    AND LOWER(a.text) LIKE LOWER(:search_pattern)
                    ORDER BY a.number
                    LIMIT :limit OFFSET :offset
                """)
                
                search_pattern = f"%{normalized_keyword}%"
                
            else:
                # Fuzzy search using pg_trgm for typo tolerance
                if is_arabic:
                    # Balanced Arabic fuzzy search with explicit similarity calculation
                    search_query = text("""
                        WITH scored_results AS (
                            SELECT 
                                a.surat_id, 
                                a.numberinsurat, 
                                a.number,
                                a.text,
                                similarity(a.text, :normalized_keyword) as sim_score,
                                GREATEST(
                                    word_similarity(:normalized_keyword, a.text),
                                    word_similarity(a.text, :normalized_keyword)
                                ) as word_sim_score,
                                -- Enhanced relevance scoring
                                CASE 
                                    WHEN a.text ILIKE :search_pattern THEN 100
                                    WHEN word_similarity(:normalized_keyword, a.text) > 0.6 THEN 90
                                    WHEN similarity(a.text, :normalized_keyword) > 0.4 THEN 80
                                    WHEN word_similarity(:normalized_keyword, a.text) > 0.4 THEN 70
                                    WHEN similarity(a.text, :normalized_keyword) > 0.3 THEN 60
                                    ELSE 50
                                END as relevance_score
                            FROM quranhub_schema.ayat a
                            WHERE a.edition_id = :search_edition_id
                            AND (
                                -- Exact matches (highest priority) - no similarity threshold needed
                                a.text ILIKE :search_pattern
                                OR
                                -- Fuzzy matching for non-exact matches
                                (
                                    a.text NOT ILIKE :search_pattern
                                    AND (
                                        -- Higher thresholds for better precision
                                        similarity(a.text, :normalized_keyword) > 0.25
                                        OR
                                        word_similarity(:normalized_keyword, a.text) > 0.35
                                        OR
                                        -- More selective partial word matches
                                        (
                                            a.text % :normalized_keyword 
                                            AND word_similarity(:normalized_keyword, a.text) > 0.25
                                        )
                                    )
                                )
                            )
                            -- More lenient length filtering
                            AND LENGTH(:normalized_keyword) > 2
                        )
                        SELECT 
                            surat_id, numberinsurat, number, sim_score, word_sim_score, relevance_score
                        FROM scored_results
                        ORDER BY 
                            relevance_score DESC,
                            word_sim_score DESC,
                            sim_score DESC,
                            number ASC
                        LIMIT :limit OFFSET :offset
                    """)
                else:
                    # Optimized multi-language search using available indexes
                    search_query = text("""
                        SELECT 
                            a.surat_id, 
                            a.numberinsurat, 
                            a.number,
                            similarity(LOWER(a.text), LOWER(:normalized_keyword)) as sim_score,
                            GREATEST(
                                word_similarity(LOWER(:normalized_keyword), LOWER(a.text)),
                                word_similarity(LOWER(a.text), LOWER(:normalized_keyword))
                            ) as word_sim_score,
                            CASE 
                                WHEN LOWER(a.text) = LOWER(:normalized_keyword) THEN 100
                                WHEN a.text ILIKE :search_pattern THEN 90
                                WHEN word_similarity(LOWER(:normalized_keyword), LOWER(a.text)) > 0.6 THEN 80
                                WHEN similarity(LOWER(a.text), LOWER(:normalized_keyword)) > 0.4 THEN 70
                                ELSE GREATEST(
                                    similarity(LOWER(a.text), LOWER(:normalized_keyword)) * 60,
                                    word_similarity(LOWER(:normalized_keyword), LOWER(a.text)) * 65
                                )
                            END as relevance_score
                        FROM quranhub_schema.ayat a
                        WHERE a.edition_id = :search_edition_id
                        AND (
                            -- Exact substring matches (fastest)
                            a.text ILIKE :search_pattern
                            OR
                            -- Full-text search using GIN index (fast for English-like languages)
                            to_tsvector('simple', a.text) @@ plainto_tsquery('simple', :normalized_keyword)
                            OR
                            -- Fallback trigram similarity for other languages (slower but works)
                            (
                                LENGTH(:normalized_keyword) > 3 
                                AND similarity(LOWER(a.text), LOWER(:normalized_keyword)) > 0.35
                            )
                        )
                        ORDER BY 
                            relevance_score DESC,
                            word_sim_score DESC,
                            sim_score DESC,
                            a.number ASC
                        LIMIT :limit OFFSET :offset
                    """)
                
                search_pattern = f"%{normalized_keyword}%"
            
            # Execute search query
            search_result = await session.execute(search_query, {
                "search_edition_id": search_edition_id,
                "normalized_keyword": normalized_keyword,
                "search_pattern": search_pattern,
                "limit": limit,
                "offset": offset
            })
            
            search_rows = search_result.fetchall()
            
            # Set search type for response
            search_type = "exact" if exact_search else "fuzzy"
            
            # Store similarity scores for API response
            similarity_scores = {}
            if not exact_search and search_rows:
                for row in search_rows:
                    similarity_scores[row.number] = {
                        "similarity": getattr(row, 'sim_score', 0) if hasattr(row, 'sim_score') else 0,
                        "wordSimilarity": getattr(row, 'word_sim_score', 0) if hasattr(row, 'word_sim_score') else 0,
                        "relevanceScore": getattr(row, 'relevance_score', 0) if hasattr(row, 'relevance_score') else 0
                    }
            
            if not search_rows:
                return {
                    "keyword": keyword,
                    "normalizedKeyword": normalized_keyword,
                    "isArabic": is_arabic,
                    "exactSearch": exact_search,
                    "searchType": search_type,
                    "count": 0,
                    "ayahs": [],
                    "surahs": [],
                    "edition": {
                        "identifier": target_edition.identifier,
                        "language": target_edition.language,
                        "name": target_edition.name,
                        "englishName": target_edition.englishname,
                        "format": target_edition.format,
                        "type": target_edition.type,
                        "direction": target_edition.direction
                    }
                }
            
            # Handle narration numbering conversion if needed
            target_verse_positions = []
            search_order = {}
            
            # Determine the narrator identifier based on edition format
            narrator_id = None
            if target_edition.format == "audio":
                # For audio editions, use narrator_identifier
                narrator_id = target_edition.narrator_identifier
            else:
                # For non-audio editions, use the edition identifier itself
                narrator_id = target_edition.identifier
            
            if narrator_id and narrator_id != "quran-hafs":
                # Convert from Hafs numbering to target narrator numbering
                logger.info(f"Converting from Hafs to {narrator_id} numbering for {len(search_rows)} results")
                
                for idx, row in enumerate(search_rows):
                    # Convert each ayah number from Hafs to target narrator
                    target_numbers = await get_narration_numbering_from_narration(
                        surah_number=row.surat_id,
                        ayah_number=row.numberinsurat,
                        source_edition_id="quran-hafs",
                        target_edition_id=narrator_id
                    )
                    
                    if target_numbers:
                        # Add all target numbers for this source ayah
                        for target_num in target_numbers:
                            target_verse_positions.append((row.surat_id, target_num))
                            # Preserve search order for each converted ayah
                            search_order[(row.surat_id, target_num)] = idx
                        logger.debug(f"Converted Surah {row.surat_id}:{row.numberinsurat} -> {target_numbers}")
                    else:
                        # This should not happen now since we return [ayah_number] when no difference exists
                        logger.warning(f"Unexpected: No conversion returned for Surah {row.surat_id}:{row.numberinsurat}, using original")
                        target_verse_positions.append((row.surat_id, row.numberinsurat))
                        search_order[(row.surat_id, row.numberinsurat)] = idx
                        
                logger.info(f"Narration conversion complete: {len(target_verse_positions)} target verses")
            else:
                # No conversion needed - use original Hafs numbering
                for idx, row in enumerate(search_rows):
                    target_verse_positions.append((row.surat_id, row.numberinsurat))
                    search_order[(row.surat_id, row.numberinsurat)] = idx
            
            # Create verse conditions for database query
            if not target_verse_positions:
                logger.warning("No target verse positions found after narration conversion")
                return {
                    "keyword": keyword,
                    "normalizedKeyword": normalized_keyword,
                    "isArabic": is_arabic,
                    "exactSearch": exact_search,
                    "searchType": search_type,
                    "count": 0,
                    "ayahs": [],
                    "surahs": [],
                    "edition": {
                        "identifier": target_edition.identifier,
                        "language": target_edition.language,
                        "name": target_edition.name,
                        "englishName": target_edition.englishname,
                        "format": target_edition.format,
                        "type": target_edition.type,
                        "direction": target_edition.direction
                    }
                }
                
            verse_conditions = []
            for surat_id, ayah_number in target_verse_positions:
                verse_conditions.append(
                    and_(Ayat.surat_id == surat_id, Ayat.numberinsurat == ayah_number)
                )
            
            # Fetch target edition verses without ordering (we'll sort them later)
            target_query = select(
                Ayat.number,
                Ayat.text,
                Ayat.numberinsurat,
                Ayat.juz_id,
                Ayat.manzil_id,
                Ayat.page_id,
                Ayat.ruku_id,
                Ayat.hizbquarter_id,
                Ayat.sajda_id,
                Surat.id,
                Surat.name,
                Surat.englishname,
                Surat.englishtranslation,
                Surat.revelationcity,
                Surat.numberofayats
            ).join(Surat, Ayat.surat_id == Surat.id).filter(
                Ayat.edition_id == target_edition_id,
                or_(*verse_conditions)
            )
            
            target_result = await session.execute(target_query)
            target_verses_raw = target_result.fetchall()
            
            # Sort target verses by search result order
            target_verses = sorted(
                target_verses_raw,
                key=lambda v: search_order.get((v.id, v.numberinsurat), 999)
            )
            
            # Process results
            ayahs = []
            surahs = []
            surah_ids = set()
            
            for verse in target_verses:
                ayah_data = {
                    "number": verse.number,
                    "text": verse.text,
                    "surah": {
                        "number": verse.id,
                        "name": verse.name,
                        "englishName": verse.englishname,
                        "englishNameTranslation": verse.englishtranslation,
                        "revelationType": verse.revelationcity,
                        "numberOfAyahs": verse.numberofayats
                    },
                    "numberInSurah": verse.numberinsurat,
                    "juz": verse.juz_id,
                    "manzil": verse.manzil_id,
                    "page": verse.page_id,
                    "ruku": verse.ruku_id,
                    "hizbQuarter": verse.hizbquarter_id,
                    "sajda": verse.sajda_id if verse.sajda_id else False
                }
                
                # Add similarity scores for fuzzy search
                if not exact_search and verse.number in similarity_scores:
                    ayah_data["similarity"] = similarity_scores[verse.number]
                
                ayahs.append(ayah_data)
                
                # Add unique surahs
                if verse.id not in surah_ids:
                    surahs.append({
                        "number": verse.id,
                        "name": verse.name,
                        "englishName": verse.englishname,
                        "englishNameTranslation": verse.englishtranslation,
                        "revelationType": verse.revelationcity,
                        "numberOfAyahs": verse.numberofayats
                    })
                    surah_ids.add(verse.id)
            
            # Add audio URLs if target edition is audio
            if target_edition.format == "audio":
                bitrates = target_edition.bitrates
                max_bitrate = max(bitrates)
                remaining_bitrates = [bitrate for bitrate in bitrates if bitrate != max_bitrate]
                for ayah in ayahs:
                    ayah["audio"] = get_ayah_audio_url(max_bitrate, target_edition.identifier, ayah["number"])
                    ayah["audioSecondary"] = get_ayah_audio_secondary_urls(remaining_bitrates, target_edition.identifier, ayah["number"])
            
            return {
                "keyword": keyword,
                "normalizedKeyword": normalized_keyword,
                "isArabic": is_arabic,
                "exactSearch": exact_search,
                "searchType": search_type,
                "count": len(ayahs),
                "ayahs": ayahs,
                "surahs": surahs,
                "edition": {
                    "identifier": target_edition.identifier,
                    "language": target_edition.language,
                    "name": target_edition.name,
                    "englishName": target_edition.englishname,
                    "format": target_edition.format,
                    "type": target_edition.type,
                    "direction": target_edition.direction
                }
            }
    
    except Exception as e:
        logger.error(f"Error searching for keyword '{keyword}': {str(e)}", exc_info=True)
        return f"An error occurred while searching for the keyword: {str(e)}"


# Legacy function for backward compatibility
async def get_keyword(
    keyword: str,
    surah: Optional[int] = None,
    language: Optional[str] = None,
    edition_identifier: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    exact_search: bool = True,
):
    """Legacy compatibility function - maps to new enhanced search."""
    edition_id = edition_identifier or DEFAULT_EDITION_IDENTIFIER
    result = await search_ayahs_by_keyword(
        keyword=keyword,
        edition_identifier=edition_id,
        exact_search=exact_search,
        limit=limit,
        offset=offset
    )
    
    # Transform result to match legacy format if needed
    if isinstance(result, dict) and "ayahs" in result:
        return {
            "count": result["count"],
            "searchType": "exact" if exact_search else "fuzzy",
            "keyword": keyword,
            "cleanedKeyword": result.get("normalizedKeyword", keyword),
            "matches": [
                {
                    "number": ayah["number"],
                    "text": ayah["text"],
                    "numberInSurah": ayah["numberInSurah"],
                    "pageNumber": ayah["page"],
                    "edition": {
                        "identifier": result["edition"]["identifier"],
                        "language": result["edition"]["language"],
                        "name": result["edition"]["name"],
                        "englishName": result["edition"]["englishName"],
                        "type": result["edition"]["type"],
                    },
                    "surah": ayah["surah"],
                    **({"similarity": ayah["similarity"]} if "similarity" in ayah else {})
                }
                for ayah in result["ayahs"]
            ]
        }
    
    return result
