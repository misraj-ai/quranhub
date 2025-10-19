# repositories/morphology_repo.py
"""
Morphology Repository - Database operations for Quranic morphological analysis
Handles 2.5M+ word-tag associations and 2,468 morphological tags
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from sqlalchemy import and_, or_, func, distinct, case, cast, Numeric
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload, aliased

from db.models import (
    Word, 
    Surat, 
    Ayat,
    MorphologicalTag, 
    WordMorphology, 
    WordMorphologyIndex
)
from db.session import AsyncSessionLocal
from utils.logger import logger


# ============================================
# GET ALL CATEGORIES
# ============================================

async def get_all_categories() -> Dict[str, Any]:
    """
    Get list of all morphological categories with their names in Arabic and English.
    
    Returns:
        Dictionary with categories and their metadata
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get all unique categories with their tag counts
            categories_query = select(
                MorphologicalTag.category,
                func.count(MorphologicalTag.tag_id).label('tag_count')
            ).group_by(
                MorphologicalTag.category
            ).order_by(
                MorphologicalTag.category
            )
            
            result = await session.execute(categories_query)
            rows = result.all()
            
            # Category names mapping (Arabic and English)
            category_names = {
                "Root": {
                    "ar": "الجذور",
                    "en": "Roots",
                    "description": "Arabic root letters"
                },
                "Sarf": {
                    "ar": "الصرف",
                    "en": "Morphology",
                    "description": "Morphological patterns and forms"
                },
                "Irab": {
                    "ar": "الإعراب",
                    "en": "Grammar",
                    "description": "Grammatical case markers"
                },
                "Afal": {
                    "ar": "الأفعال",
                    "en": "Verbs",
                    "description": "Verb forms and tenses"
                },
                "Lawahiq": {
                    "ar": "اللواحق",
                    "en": "Suffixes",
                    "description": "Attached suffixes"
                },
                "Horof": {
                    "ar": "الحروف",
                    "en": "Particles",
                    "description": "Particles and prepositions"
                },
                "Tajwid": {
                    "ar": "التجويد",
                    "en": "Tajweed",
                    "description": "Quranic recitation rules"
                },
                "Asma": {
                    "ar": "الأسماء",
                    "en": "Nouns",
                    "description": "Noun forms"
                },
                "Aam": {
                    "ar": "عام",
                    "en": "General",
                    "description": "General markers"
                },
                "Sawabiq": {
                    "ar": "السوابق",
                    "en": "Prefixes",
                    "description": "Attached prefixes"
                },
                "Monawaeat": {
                    "ar": "المنوعات",
                    "en": "Miscellaneous",
                    "description": "Various markers"
                }
            }
            
            # Build response
            categories = []
            for row in rows:
                category_code = row.category
                category_info = category_names.get(category_code, {
                    "ar": category_code,
                    "en": category_code,
                    "description": ""
                })
                
                categories.append({
                    "code": category_code,
                    "ar": category_info["ar"],
                    "en": category_info["en"],
                    "description": category_info["description"],
                    "tag_count": row.tag_count
                })
            
            return {
                "total_categories": len(categories),
                "categories": categories
            }
            
    except Exception as e:
        logger.error(f"Error getting all categories: {str(e)}", exc_info=True)
        return f"An error occurred while fetching categories: {str(e)}"
    
# ============================================
# WORD MORPHOLOGY LOOKUP
# ============================================

async def get_word_morphology_by_location(
    surah_id: int,
    ayah_number: int,
    position: int,
    category: Optional[str] = None,
    include_meaning: bool = True
) -> Dict[str, Any]:
    """
    Get complete morphological breakdown for a specific word by location.
    
    Args:
        surah_id: Surah number (1-114)
        ayah_number: Ayah number within surah
        position: Word position within ayah
        category: Optional filter by tag category
        include_meaning: Include tag meanings in response
        
    Returns:
        Dictionary with word info and morphological tags
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get word with its morphologies and related data
            query = select(Word).options(
                joinedload(Word.surat),
                selectinload(Word.morphologies).joinedload(WordMorphology.tag)
            ).filter(
                Word.surat_id == surah_id,
                Word.numberinsurat == ayah_number,
                Word.position == position
            )
            
            result = await session.execute(query)
            word = result.unique().scalar_one_or_none()
            
            if not word:
                return f"Word not found at location {surah_id}:{ayah_number}:{position}"
            
            # Get ayah text
            ayah_query = select(Ayat.text).filter(
                Ayat.surat_id == surah_id,
                Ayat.numberinsurat == ayah_number,
                Ayat.edition_id == 78  # quran-simple-clean
            )
            ayah_result = await session.execute(ayah_query)
            ayah_text = ayah_result.scalar_one_or_none()
            
            # Filter morphologies by category if specified
            morphologies = word.morphologies
            if category:
                morphologies = [m for m in morphologies if m.tag.category == category]
            
            # Group tags by category
            tags_by_category = {}
            all_tags = []
            
            for morph in sorted(morphologies, key=lambda m: m.tag_order or 0):
                tag_data = {
                    "code": morph.tag.code,
                    "category": morph.tag.category,
                    "order": morph.tag_order
                }
                
                if include_meaning:
                    tag_data["meaning"] = morph.tag.meaning
                    if morph.tag.user_meaning:
                        tag_data["user_meaning"] = morph.tag.user_meaning
                
                # Add to all_tags list
                all_tags.append(tag_data)
                
                # Group by category
                if morph.tag.category not in tags_by_category:
                    tags_by_category[morph.tag.category] = []
                tags_by_category[morph.tag.category].append(tag_data)
            
            return {
                "word": {
                    "id": word.id,
                    "location": f"{surah_id}:{ayah_number}:{position}",
                    "text": word.text,
                    "surah": {
                        "id": word.surat.id,
                        "name": word.surat.name,
                        "english_name": word.surat.englishname
                    },
                    "ayah_number": ayah_number,
                    "position": position,
                    "ayah_text": ayah_text
                },
                "morphology": {
                    "total_tags": len(all_tags),
                    "tags_by_category": tags_by_category,
                    "all_tags": all_tags
                }
            }
            
    except Exception as e:
        logger.error(f"Error getting word morphology for {surah_id}:{ayah_number}:{position}: {str(e)}", exc_info=True)
        return f"An error occurred while fetching word morphology: {str(e)}"


# ============================================
# SEARCH BY TAGS
# ============================================

async def search_words_by_tags(
    tags: List[str],
    match_all: bool = True,
    surah_number: Optional[int] = None,
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Search words by morphological tags.
    
    Args:
        tags: List of tag codes to search for
        match_all: If True, word must have ALL tags (AND). If False, ANY tag (OR)
        surah_number: Optional filter by surah
        category: Optional filter tags by category
        limit: Maximum results to return
        offset: Pagination offset
        
    Returns:
        Dictionary with matching words and metadata
    """
    try:
        async with AsyncSessionLocal() as session:
            # Base query joining all necessary tables
            base_query = select(
                Word.id.label('word_id'),
                Word.surat_id,
                Word.numberinsurat,
                Word.position,
                Word.text,
                Word.location,
                Surat.name.label('surah_name'),
                Surat.englishname.label('surah_english_name'),
                Ayat.text.label('ayah_text'),
                func.array_agg(
                    distinct(WordMorphology.tag_code)
                ).label('matched_tags')
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).join(
                Surat, Word.surat_id == Surat.id
            ).join(
                Ayat,
                and_(
                    Ayat.surat_id == Word.surat_id,
                    Ayat.numberinsurat == Word.numberinsurat,
                    Ayat.edition_id == 78
                )
            ).filter(
                WordMorphology.tag_code.in_(tags)
            )
            
            # Add surah filter if specified
            if surah_number:
                base_query = base_query.filter(Word.surat_id == surah_number)
            
            # Group by word
            base_query = base_query.group_by(
                Word.id,
                Word.surat_id,
                Word.numberinsurat,
                Word.position,
                Word.text,
                Word.location,
                Surat.name,
                Surat.englishname,
                Ayat.text
            )
            
            # Add HAVING clause for match_all (AND logic)
            if match_all:
                base_query = base_query.having(
                    func.count(distinct(WordMorphology.tag_code)) == len(tags)
                )
            
            # Order and paginate
            query = base_query.order_by(
                Word.surat_id,
                Word.numberinsurat,
                Word.position
            ).limit(limit).offset(offset)
            
            result = await session.execute(query)
            rows = result.all()
            
            # Get total count using subquery
            count_subquery = base_query.subquery()
            count_query = select(func.count()).select_from(count_subquery)
            count_result = await session.execute(count_query)
            total = count_result.scalar()
            
            # Format results
            results = []
            for row in rows:
                results.append({
                    "word_id": row.word_id,
                    "location": row.location,
                    "text": row.text,
                    "surah": {
                        "id": row.surat_id,
                        "name": row.surah_name,
                        "english_name": row.surah_english_name
                    },
                    "ayah_number": row.numberinsurat,
                    "position": row.position,
                    "ayah_text": row.ayah_text,
                    "matched_tags": row.matched_tags
                })
            
            return {
                "query": {
                    "tags": tags,
                    "match_all": match_all,
                    "surah_number": surah_number,
                    "category": category
                },
                "results": results,
                "pagination": {
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total
                }
            }
            
    except Exception as e:
        logger.error(f"Error searching by tags {tags}: {str(e)}", exc_info=True)
        return f"An error occurred while searching by tags: {str(e)}"


# ============================================
# SEARCH BY CATEGORY
# ============================================

async def search_words_by_category(
    category: str,
    tag_code: Optional[str] = None,
    surah_number: Optional[int] = None,
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Search words by morphological tag category.
    
    Args:
        category: Tag category (Root, Sarf, Irab, etc.)
        tag_code: Optional specific tag within category
        surah_number: Optional filter by surah
        limit: Maximum results
        offset: Pagination offset
        
    Returns:
        Dictionary with matching words
    """
    try:
        async with AsyncSessionLocal() as session:
            # Build query
            query = select(
                Word.id.label('word_id'),
                Word.surat_id,
                Word.numberinsurat,
                Word.position,
                Word.text,
                Word.location,
                Surat.name.label('surah_name'),
                Surat.englishname.label('surah_english_name'),
                Ayat.text.label('ayah_text'),
                func.array_agg(
                    func.json_build_object(
                        'code', MorphologicalTag.code,
                        'meaning', MorphologicalTag.meaning
                    )
                ).label('matched_tags')
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).join(
                MorphologicalTag, WordMorphology.tag_code == MorphologicalTag.code
            ).join(
                Surat, Word.surat_id == Surat.id
            ).join(
                Ayat,
                and_(
                    Ayat.surat_id == Word.surat_id,
                    Ayat.numberinsurat == Word.numberinsurat,
                    Ayat.edition_id == 78
                )
            ).filter(
                MorphologicalTag.category == category
            )
            
            # Add optional filters
            if tag_code:
                query = query.filter(MorphologicalTag.code == tag_code)
            if surah_number:
                query = query.filter(Word.surat_id == surah_number)
            
            # Group, order, and paginate
            query = query.group_by(
                Word.id,
                Word.surat_id,
                Word.numberinsurat,
                Word.position,
                Word.text,
                Word.location,
                Surat.name,
                Surat.englishname,
                Ayat.text
            ).order_by(
                Word.surat_id,
                Word.numberinsurat,
                Word.position
            ).limit(limit).offset(offset)
            
            result = await session.execute(query)
            rows = result.all()
            
            # Get total count
            count_query = select(
                func.count(distinct(Word.id))
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).join(
                MorphologicalTag, WordMorphology.tag_code == MorphologicalTag.code
            ).filter(
                MorphologicalTag.category == category
            )
            
            if tag_code:
                count_query = count_query.filter(MorphologicalTag.code == tag_code)
            if surah_number:
                count_query = count_query.filter(Word.surat_id == surah_number)
            
            count_result = await session.execute(count_query)
            total = count_result.scalar()
            
            # Format results
            results = []
            for row in rows:
                results.append({
                    "word_id": row.word_id,
                    "location": row.location,
                    "text": row.text,
                    "surah": {
                        "id": row.surat_id,
                        "name": row.surah_name,
                        "english_name": row.surah_english_name
                    },
                    "ayah_number": row.numberinsurat,
                    "position": row.position,
                    "ayah_text": row.ayah_text,
                    "matched_tags": row.matched_tags
                })
            
            return {
                "category": category,
                "tag_code": tag_code,
                "results": results,
                "pagination": {
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total
                }
            }
            
    except Exception as e:
        logger.error(f"Error searching by category {category}: {str(e)}", exc_info=True)
        return f"An error occurred while searching by category: {str(e)}"


# ============================================
# ROOT-BASED SEARCH
# ============================================

async def search_words_by_root(
    root: str,
    surah_number: Optional[int] = None,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Find all words derived from a specific Arabic root.
    
    Args:
        root: Arabic root
        surah_number: Optional filter by surah
        limit: Maximum results
        offset: Pagination offset
        
    Returns:
        Dictionary with root info and derived words
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get root statistics from materialized view
            root_stats_query = select(WordMorphologyIndex).filter(
                WordMorphologyIndex.tag_code == root,
                WordMorphologyIndex.category == 'Root'
            )
            
            root_stats_result = await session.execute(root_stats_query)
            root_stats = root_stats_result.scalar_one_or_none()
            
            if not root_stats:
                return f"Root '{root}' not found"
            
            # Build query for words with this root
            query = select(
                Word.id.label('word_id'),
                Word.surat_id,
                Word.numberinsurat,
                Word.position,
                Word.text,
                Word.location,
                Surat.name.label('surah_name'),
                Surat.englishname.label('surah_english_name'),
                Ayat.text.label('ayah_text')
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).join(
                Surat, Word.surat_id == Surat.id
            ).join(
                Ayat,
                and_(
                    Ayat.surat_id == Word.surat_id,
                    Ayat.numberinsurat == Word.numberinsurat,
                    Ayat.edition_id == 78
                )
            ).filter(
                WordMorphology.tag_code == root
            )
            
            # Add surah filter if specified
            if surah_number:
                query = query.filter(Word.surat_id == surah_number)
            
            # Order and paginate
            query = query.order_by(
                Word.surat_id,
                Word.numberinsurat,
                Word.position
            ).limit(limit).offset(offset)
            
            result = await session.execute(query)
            rows = result.all()
            
            # Get total count
            count_query = select(
                func.count(distinct(Word.id))
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).filter(
                WordMorphology.tag_code == root
            )
            
            if surah_number:
                count_query = count_query.filter(Word.surat_id == surah_number)
            
            count_result = await session.execute(count_query)
            total = count_result.scalar()
            
            # Format results
            derivatives = []
            for row in rows:
                derivatives.append({
                    "word_id": row.word_id,
                    "location": row.location,
                    "text": row.text,
                    "surah": {
                        "id": row.surat_id,
                        "name": row.surah_name,
                        "english_name": row.surah_english_name
                    },
                    "ayah_number": row.numberinsurat,
                    "position": row.position,
                    "ayah_text": row.ayah_text
                })
            
            return {
                "root": root,
                "root_info": {
                    "meaning": root_stats.meaning,
                    "total_occurrences": root_stats.word_count,
                    "surahs_count": root_stats.surah_count
                },
                "derivatives": derivatives,
                "pagination": {
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total
                }
            }
            
    except Exception as e:
        logger.error(f"Error searching by root {root}: {str(e)}", exc_info=True)
        return f"An error occurred while searching by root: {str(e)}"


# ============================================
# LIST ALL ROOTS
# ============================================

async def get_all_roots(
    sort_by: str = "frequency",
    min_occurrences: int = 1,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Get list of all Arabic roots in the Quran.
    
    Args:
        sort_by: 'frequency' or 'alphabetical'
        min_occurrences: Minimum word count filter
        limit: Maximum results
        offset: Pagination offset
        
    Returns:
        Dictionary with roots and statistics
    """
    try:
        async with AsyncSessionLocal() as session:
            # Build query
            query = select(WordMorphologyIndex).filter(
                WordMorphologyIndex.category == 'Root',
                WordMorphologyIndex.word_count >= min_occurrences
            )
            
            # Apply sorting
            if sort_by == "frequency":
                query = query.order_by(WordMorphologyIndex.word_count.desc())
            else:  # alphabetical
                query = query.order_by(WordMorphologyIndex.tag_code)
            
            # Get total count
            count_query = select(func.count()).select_from(WordMorphologyIndex).filter(
                WordMorphologyIndex.category == 'Root',
                WordMorphologyIndex.word_count >= min_occurrences
            )
            count_result = await session.execute(count_query)
            total = count_result.scalar()
            
            # Apply pagination
            query = query.limit(limit).offset(offset)
            
            result = await session.execute(query)
            roots_data = result.scalars().all()
            
            # Format results
            roots = []
            for root in roots_data:
                roots.append({
                    "root": root.tag_code,
                    "meaning": root.meaning,
                    "statistics": {
                        "word_count": root.word_count,
                        "surah_count": root.surah_count
                    }
                })
            
            return {
                "total_roots": total,
                "roots": roots,
                "pagination": {
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total
                }
            }
            
    except Exception as e:
        logger.error(f"Error getting all roots: {str(e)}", exc_info=True)
        return f"An error occurred while fetching roots: {str(e)}"


# ============================================
# GET ALL TAGS
# ============================================

async def get_all_tags(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Get list of all morphological tags.
    
    Args:
        category: Optional filter by category
        search: Optional search in code or meaning
        limit: Maximum results
        offset: Pagination offset
        
    Returns:
        Dictionary with tags and category counts
    """
    try:
        async with AsyncSessionLocal() as session:
            # Build base query with usage count from word_morphology_index
            query = select(
                MorphologicalTag,
                func.coalesce(WordMorphologyIndex.word_count, 0).label('usage_count')
            ).outerjoin(
                WordMorphologyIndex,
                MorphologicalTag.code == WordMorphologyIndex.tag_code
            )
            
            # Apply filters
            filters = []
            if category:
                filters.append(MorphologicalTag.category == category)
            if search:
                search_pattern = f"%{search}%"
                filters.append(or_(
                    MorphologicalTag.code.ilike(search_pattern),
                    MorphologicalTag.meaning.ilike(search_pattern),
                    MorphologicalTag.user_meaning.ilike(search_pattern)
                ))
            
            if filters:
                query = query.filter(and_(*filters))
            
            # Get total count
            count_query = select(func.count()).select_from(MorphologicalTag)
            if filters:
                count_query = count_query.filter(and_(*filters))
            count_result = await session.execute(count_query)
            total = count_result.scalar()
            
            # Apply sorting and pagination
            query = query.order_by(MorphologicalTag.category, MorphologicalTag.code)
            query = query.limit(limit).offset(offset)
            
            result = await session.execute(query)
            rows = result.all()
            
            # Get category counts
            category_query = select(
                MorphologicalTag.category,
                func.count(MorphologicalTag.tag_id).label('count')
            ).group_by(MorphologicalTag.category)
            
            category_result = await session.execute(category_query)
            category_counts = {row.category: row.count for row in category_result.all()}
            
            # Format results
            tags = []
            for row in rows:
                tag = row[0]  # MorphologicalTag object
                usage_count = row[1]  # usage_count from join
                
                tags.append({
                    "tag_id": tag.tag_id,
                    "code": tag.code,
                    "meaning": tag.meaning,
                    "user_meaning": tag.user_meaning,
                    "category": tag.category,
                    "usage_count": usage_count
                })
            
            return {
                "total_tags": total,
                "tags": tags,
                "categories": category_counts,
                "pagination": {
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total
                }
            }
            
    except Exception as e:
        logger.error(f"Error getting all tags: {str(e)}", exc_info=True)
        return f"An error occurred while fetching tags: {str(e)}"


# ============================================
# GET TAG DETAILS
# ============================================

async def get_tag_details(tag_code: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific tag including statistics and examples.
    
    Args:
        tag_code: Tag code to lookup
        
    Returns:
        Dictionary with tag details, statistics, and examples
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get tag info
            tag_query = select(MorphologicalTag).filter(
                MorphologicalTag.code == tag_code
            )
            tag_result = await session.execute(tag_query)
            tag = tag_result.scalar_one_or_none()
            
            if not tag:
                return f"Tag '{tag_code}' not found"
            
            # Get statistics from materialized view
            stats_query = select(WordMorphologyIndex).filter(
                WordMorphologyIndex.tag_code == tag_code
            )
            stats_result = await session.execute(stats_query)
            stats = stats_result.scalar_one_or_none()
            
            # Get related tags (tags that frequently appear with this tag)
            # Create aliases for self-join
            wm1 = aliased(WordMorphology)
            wm2 = aliased(WordMorphology)
            
            related_query = select(
                MorphologicalTag.code,
                MorphologicalTag.meaning,
                func.count().label('co_occurrence_count')
            ).select_from(wm1).join(
                wm2, wm1.word_id == wm2.word_id
            ).join(
                MorphologicalTag, wm2.tag_code == MorphologicalTag.code
            ).filter(
                wm1.tag_code == tag_code,
                wm2.tag_code != tag_code
            ).group_by(
                MorphologicalTag.code,
                MorphologicalTag.meaning
            ).order_by(
                func.count().desc()
            ).limit(10)
            
            related_result = await session.execute(related_query)
            related_tags = [
                {
                    "code": row.code,
                    "meaning": row.meaning,
                    "co_occurrence_count": row.co_occurrence_count
                }
                for row in related_result.all()
            ]
            
            # Get example words
            examples_query = select(
                Word.id.label('word_id'),
                Word.location,
                Word.text,
                Ayat.text.label('ayah_text')
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).join(
                Ayat,
                and_(
                    Ayat.surat_id == Word.surat_id,
                    Ayat.numberinsurat == Word.numberinsurat,
                    Ayat.edition_id == 78
                )
            ).filter(
                WordMorphology.tag_code == tag_code
            ).order_by(
                Word.surat_id,
                Word.numberinsurat,
                Word.position
            ).limit(5)
            
            examples_result = await session.execute(examples_query)
            examples = [
                {
                    "word_id": row.word_id,
                    "location": row.location,
                    "text": row.text,
                    "ayah_text": row.ayah_text
                }
                for row in examples_result.all()
            ]
            
            # Calculate percentage if stats available
            total_words = 77433
            percentage = (stats.word_count / total_words * 100) if stats else 0
            
            return {
                "tag": {
                    "code": tag.code,
                    "meaning": tag.meaning,
                    "user_meaning": tag.user_meaning,
                    "category": tag.category
                },
                "statistics": {
                    "total_words": stats.word_count if stats else 0,
                    "surahs_count": stats.surah_count if stats else 0,
                    "percentage_of_quran": round(percentage, 2)
                },
                "related_tags": related_tags,
                "examples": examples
            }
            
    except Exception as e:
        logger.error(f"Error getting tag details for {tag_code}: {str(e)}", exc_info=True)
        return f"An error occurred while fetching tag details: {str(e)}"


# ============================================
# MORPHOLOGICAL STATISTICS
# ============================================

async def get_morphology_statistics(
    surah_number: Optional[int] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get overall morphological statistics for the Quran or specific surah.
    
    Args:
        surah_number: Optional filter by specific surah
        category: Optional filter by tag category
        
    Returns:
        Dictionary with comprehensive morphological statistics
    """
    try:
        async with AsyncSessionLocal() as session:
            # Base statistics
            total_words = 77433
            
            # Build base filter for surah if specified
            word_filter = Word.surat_id == surah_number if surah_number else True
            
            # Get words with morphology count
            words_query = select(
                func.count(distinct(WordMorphology.word_id))
            ).select_from(WordMorphology).join(
                Word, WordMorphology.word_id == Word.id
            ).filter(word_filter)
            
            words_result = await session.execute(words_query)
            words_with_morphology = words_result.scalar() or 0
            
            # Get total associations
            assoc_query = select(
                func.count(WordMorphology.id)
            ).select_from(WordMorphology).join(
                Word, WordMorphology.word_id == Word.id
            ).filter(word_filter)
            
            assoc_result = await session.execute(assoc_query)
            total_associations = assoc_result.scalar() or 0
            
            # Get category statistics
            category_filter = [word_filter]
            if category:
                category_filter.append(MorphologicalTag.category == category)
            
            category_query = select(
                MorphologicalTag.category,
                func.count(distinct(MorphologicalTag.code)).label('unique_tags'),
                func.count(WordMorphology.id).label('total_occurrences'),
                case(
                    (words_with_morphology > 0, 
                     func.round(
                         cast(func.count(WordMorphology.id), Numeric) / words_with_morphology, 
                         2
                     )),
                    else_=0
                ).label('avg_per_word')
            ).select_from(WordMorphology).join(
                MorphologicalTag, WordMorphology.tag_code == MorphologicalTag.code
            ).join(
                Word, WordMorphology.word_id == Word.id
            ).filter(
                and_(*category_filter)
            ).group_by(
                MorphologicalTag.category
            ).order_by(
                func.count(WordMorphology.id).desc()
            )
            
            category_result = await session.execute(category_query)
            categories = {
                row.category: {
                    "unique_tags": row.unique_tags,
                    "total_occurrences": row.total_occurrences,
                    "avg_per_word": float(row.avg_per_word) if row.avg_per_word else 0
                }
                for row in category_result.all()
            }
            
            # Get top roots
            if surah_number:
                top_roots_query = select(
                    WordMorphologyIndex.tag_code.label('root'),
                    func.count(distinct(Word.id)).label('word_count'),
                    func.round(
                        cast(func.count(distinct(Word.id)), Numeric) / total_words * 100,
                        2
                    ).label('percentage')
                ).select_from(WordMorphologyIndex).join(
                    WordMorphology, WordMorphologyIndex.tag_code == WordMorphology.tag_code
                ).join(
                    Word, WordMorphology.word_id == Word.id
                ).filter(
                    WordMorphologyIndex.category == 'Root',
                    Word.surat_id == surah_number
                ).group_by(
                    WordMorphologyIndex.tag_code
                ).order_by(
                    func.count(distinct(Word.id)).desc()
                ).limit(10)
            else:
                top_roots_query = select(
                    WordMorphologyIndex.tag_code.label('root'),
                    WordMorphologyIndex.word_count,
                    func.round(
                        cast(WordMorphologyIndex.word_count, Numeric) / total_words * 100,
                        2
                    ).label('percentage')
                ).filter(
                    WordMorphologyIndex.category == 'Root'
                ).order_by(
                    WordMorphologyIndex.word_count.desc()
                ).limit(10)
            
            top_roots_result = await session.execute(top_roots_query)
            top_roots = [
                {
                    "root": row.root,
                    "word_count": row.word_count,
                    "percentage": float(row.percentage)
                }
                for row in top_roots_result.all()
            ]
            
            # Get top tags overall
            top_tags_query = select(
                MorphologicalTag.code,
                MorphologicalTag.category,
                func.count(WordMorphology.id).label('usage_count'),
                case(
                    (words_with_morphology > 0,
                     func.round(
                         cast(func.count(WordMorphology.id), Numeric) / words_with_morphology * 100,
                         2
                     )),
                    else_=0
                ).label('percentage')
            ).select_from(WordMorphology).join(
                MorphologicalTag, WordMorphology.tag_code == MorphologicalTag.code
            ).join(
                Word, WordMorphology.word_id == Word.id
            ).filter(
                word_filter
            ).group_by(
                MorphologicalTag.code,
                MorphologicalTag.category
            ).order_by(
                func.count(WordMorphology.id).desc()
            ).limit(20)
            
            top_tags_result = await session.execute(top_tags_query)
            top_tags = [
                {
                    "code": row.code,
                    "category": row.category,
                    "usage_count": row.usage_count,
                    "percentage": float(row.percentage)
                }
                for row in top_tags_result.all()
            ]
            
            # Calculate coverage and average tags per word
            coverage = (words_with_morphology / total_words * 100) if total_words > 0 else 0
            avg_tags_per_word = (total_associations / words_with_morphology) if words_with_morphology > 0 else 0
            
            return {
                "scope": {
                    "surah_number": surah_number,
                    "category": category
                },
                "overview": {
                    "total_words": total_words if not surah_number else words_with_morphology,
                    "words_with_morphology": words_with_morphology,
                    "coverage": round(coverage, 2),
                    "total_tags": len(categories),
                    "total_associations": total_associations,
                    "avg_tags_per_word": round(avg_tags_per_word, 2)
                },
                "by_category": categories,
                "top_roots": top_roots,
                "top_tags": top_tags
            }
            
    except Exception as e:
        logger.error(f"Error getting morphology statistics: {str(e)}", exc_info=True)
        return f"An error occurred while fetching statistics: {str(e)}"


# ============================================
# SURAH MORPHOLOGICAL PROFILE
# ============================================

async def get_surah_morphology_profile(surah_number: int) -> Dict[str, Any]:
    """
    Get detailed morphological analysis for a specific surah.
    
    Args:
        surah_number: Surah number (1-114)
        
    Returns:
        Dictionary with surah morphological profile
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get surah info
            surah_query = select(Surat).filter(Surat.id == surah_number)
            surah_result = await session.execute(surah_query)
            surah = surah_result.scalar_one_or_none()
            
            if not surah:
                return f"Surah {surah_number} not found"
            
            # Get word count for surah
            word_count_query = select(
                func.count(Word.id)
            ).filter(
                Word.surat_id == surah_number
            )
            word_count_result = await session.execute(word_count_query)
            total_words = word_count_result.scalar()
            
            # Get unique roots in surah
            unique_roots_query = select(
                func.count(distinct(WordMorphology.tag_code))
            ).select_from(WordMorphology).join(
                MorphologicalTag, WordMorphology.tag_code == MorphologicalTag.code
            ).join(
                Word, WordMorphology.word_id == Word.id
            ).filter(
                Word.surat_id == surah_number,
                MorphologicalTag.category == 'Root'
            )
            unique_roots_result = await session.execute(unique_roots_query)
            unique_roots = unique_roots_result.scalar()
            
            # Get most common root
            most_common_root_query = select(
                WordMorphology.tag_code.label('root'),
                func.count().label('occurrences')
            ).select_from(WordMorphology).join(
                MorphologicalTag, WordMorphology.tag_code == MorphologicalTag.code
            ).join(
                Word, WordMorphology.word_id == Word.id
            ).filter(
                Word.surat_id == surah_number,
                MorphologicalTag.category == 'Root'
            ).group_by(
                WordMorphology.tag_code
            ).order_by(
                func.count().desc()
            ).limit(1)
            
            most_common_root_result = await session.execute(most_common_root_query)
            most_common_root_row = most_common_root_result.first()
            most_common_root = {
                "root": most_common_root_row.root,
                "occurrences": most_common_root_row.occurrences
            } if most_common_root_row else None
            
            # Get verb tense distribution
            verb_tenses_query = select(
                MorphologicalTag.user_meaning,
                func.count(distinct(Word.id)).label('count')
            ).select_from(WordMorphology).join(
                MorphologicalTag, WordMorphology.tag_code == MorphologicalTag.code
            ).join(
                Word, WordMorphology.word_id == Word.id
            ).filter(
                Word.surat_id == surah_number,
                MorphologicalTag.code.in_(['ضي', 'ضع', 'مر'])
            ).group_by(
                MorphologicalTag.user_meaning
            )
            
            verb_tenses_result = await session.execute(verb_tenses_query)
            verb_tenses = {
                row.user_meaning: row.count
                for row in verb_tenses_result.all()
            }
            
            # Calculate complexity score (simple heuristic)
            complexity_score = min(100, (unique_roots / total_words * 100 * 2)) if total_words > 0 else 0
            
            return {
                "surah": {
                    "id": surah.id,
                    "name": surah.name,
                    "english_name": surah.englishname,
                    "total_words": total_words,
                    "total_ayahs": surah.numberofayats
                },
                "morphology": {
                    "unique_roots": unique_roots,
                    "most_common_root": most_common_root,
                    "verb_tenses": verb_tenses
                },
                "complexity_score": round(complexity_score, 1)
            }
            
    except Exception as e:
        logger.error(f"Error getting surah profile for {surah_number}: {str(e)}", exc_info=True)
        return f"An error occurred while fetching surah profile: {str(e)}"


# ============================================
# SEARCH BY PATTERN (وزن)
# ============================================

async def search_words_by_pattern(
    pattern: str,
    surah_number: Optional[int] = None,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Find words matching a specific morphological pattern (وزن).
    """
    try:
        async with AsyncSessionLocal() as session:
            # First, try exact match in meaning
            pattern_tag_query = select(MorphologicalTag).filter(
                MorphologicalTag.category == 'Sarf',
                or_(
                    MorphologicalTag.meaning == f"وزن الكلمة: {pattern}",
                    MorphologicalTag.user_meaning == f"وزن الكلمة: {pattern}",
                    MorphologicalTag.meaning == pattern,
                    MorphologicalTag.user_meaning == pattern
                )
            )
            
            pattern_tag_result = await session.execute(pattern_tag_query)
            pattern_tag = pattern_tag_result.first()
            
            # If no exact match, try contains
            if not pattern_tag:
                pattern_tag_query = select(MorphologicalTag).filter(
                    MorphologicalTag.category == 'Sarf',
                    or_(
                        MorphologicalTag.meaning.contains(pattern),
                        MorphologicalTag.user_meaning.contains(pattern)
                    )
                ).limit(1)
                
                pattern_tag_result = await session.execute(pattern_tag_query)
                pattern_tag_row = pattern_tag_result.first()
                pattern_tag = pattern_tag_row[0] if pattern_tag_row else None
            else:
                pattern_tag = pattern_tag[0]
            
            if not pattern_tag:
                return f"Pattern '{pattern}' not found"
            
            # Get pattern statistics
            stats_query = select(WordMorphologyIndex).filter(
                WordMorphologyIndex.tag_code == pattern_tag.code
            )
            stats_result = await session.execute(stats_query)
            stats = stats_result.scalar_one_or_none()
            
            # Get words with this pattern
            # Create alias for root lookup
            wm_root = aliased(WordMorphology)
            root_tag = aliased(MorphologicalTag)
            
            words_query = select(
                Word.id.label('word_id'),
                Word.location,
                Word.text,
                Word.surat_id,
                Word.numberinsurat,
                Surat.name.label('surah_name'),
                Ayat.text.label('ayah_text'),
                wm_root.tag_code.label('root')
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).join(
                Surat, Word.surat_id == Surat.id
            ).join(
                Ayat,
                and_(
                    Ayat.surat_id == Word.surat_id,
                    Ayat.numberinsurat == Word.numberinsurat,
                    Ayat.edition_id == 78
                )
            ).outerjoin(
                wm_root,
                Word.id == wm_root.word_id
            ).outerjoin(
                root_tag,
                and_(
                    wm_root.tag_code == root_tag.code,
                    root_tag.category == 'Root'
                )
            ).filter(
                WordMorphology.tag_code == pattern_tag.code
            )
            
            # Add surah filter if specified
            if surah_number:
                words_query = words_query.filter(Word.surat_id == surah_number)
            
            # Group to handle multiple roots per word (though unlikely)
            words_query = words_query.group_by(
                Word.id,
                Word.location,
                Word.text,
                Word.surat_id,
                Word.numberinsurat,
                Surat.name,
                Ayat.text,
                wm_root.tag_code
            ).order_by(
                Word.surat_id,
                Word.numberinsurat,
                Word.position
            ).limit(limit).offset(offset)
            
            words_result = await session.execute(words_query)
            rows = words_result.all()
            
            # Get total count
            count_query = select(
                func.count(distinct(Word.id))
            ).select_from(Word).join(
                WordMorphology, Word.id == WordMorphology.word_id
            ).filter(
                WordMorphology.tag_code == pattern_tag.code
            )
            
            if surah_number:
                count_query = count_query.filter(Word.surat_id == surah_number)
            
            count_result = await session.execute(count_query)
            total = count_result.scalar()
            
            # Format results
            words = []
            for row in rows:
                words.append({
                    "word_id": row.word_id,
                    "location": row.location,
                    "text": row.text,
                    "root": row.root,
                    "surah": {
                        "id": row.surat_id,
                        "name": row.surah_name
                    },
                    "ayah_number": row.numberinsurat,
                    "ayah_text": row.ayah_text
                })
            
            return {
                "pattern": pattern,
                "pattern_info": {
                    "tag_code": pattern_tag.code,
                    "category": pattern_tag.category,
                    "total_occurrences": stats.word_count if stats else 0
                },
                "words": words,
                "pagination": {
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total
                }
            }
            
    except Exception as e:
        logger.error(f"Error searching by pattern {pattern}: {str(e)}", exc_info=True)
        return f"An error occurred while searching by pattern: {str(e)}"


# ============================================
# COMPARE WORDS MORPHOLOGICALLY
# ============================================

async def compare_words_morphology(word_locations: List[str]) -> Dict[str, Any]:
    """
    Compare morphological features of multiple words.
    
    Args:
        word_locations: List of word locations in format "surah:ayah:position"
        
    Returns:
        Dictionary with comparison data
    """
    try:
        async with AsyncSessionLocal() as session:
            words_data = []
            all_tags_sets = []
            
            for location in word_locations:
                parts = location.split(':')
                if len(parts) != 3:
                    continue
                
                try:
                    surah_id, ayah_num, position = map(int, parts)
                except ValueError:
                    continue
                
                # Get word morphology
                word_query = select(Word).options(
                    selectinload(Word.morphologies).joinedload(WordMorphology.tag)
                ).filter(
                    Word.surat_id == surah_id,
                    Word.numberinsurat == ayah_num,
                    Word.position == position
                )
                
                result = await session.execute(word_query)
                word = result.unique().scalar_one_or_none()
                
                if not word:
                    continue
                
                # Collect tag codes
                tag_codes = {m.tag.code for m in word.morphologies}
                all_tags_sets.append(tag_codes)
                
                # Get categories
                categories = list({m.tag.category for m in word.morphologies})
                
                words_data.append({
                    "location": location,
                    "text": word.text,
                    "tags_count": len(word.morphologies),
                    "categories": categories,
                    "tag_codes": list(tag_codes)
                })
            
            if len(words_data) < 2:
                return "Need at least 2 valid word locations to compare"
            
            # Find common tags
            common_tags_codes = set.intersection(*all_tags_sets) if all_tags_sets else set()
            
            # Get tag details for common tags
            if common_tags_codes:
                common_tags_query = select(MorphologicalTag).filter(
                    MorphologicalTag.code.in_(list(common_tags_codes))
                )
                common_tags_result = await session.execute(common_tags_query)
                common_tags = [
                    {
                        "code": tag.code,
                        "meaning": tag.meaning,
                        "category": tag.category
                    }
                    for tag in common_tags_result.scalars().all()
                ]
            else:
                common_tags = []
            
            # Find unique tags for each word
            unique_to_each = {}
            for i, word_data in enumerate(words_data):
                word_tags = set(word_data["tag_codes"])
                other_tags = set()
                for j, other_word in enumerate(words_data):
                    if i != j:
                        other_tags.update(other_word["tag_codes"])
                
                unique_tags = word_tags - other_tags
                unique_to_each[word_data["location"]] = list(unique_tags)
            
            # Calculate similarity score (Jaccard similarity)
            if len(all_tags_sets) >= 2:
                intersection_size = len(common_tags_codes)
                union_size = len(set.union(*all_tags_sets))
                similarity_score = (intersection_size / union_size * 100) if union_size > 0 else 0
            else:
                similarity_score = 0
            
            return {
                "words": words_data,
                "comparison": {
                    "common_tags": common_tags,
                    "unique_to_each": unique_to_each,
                    "similarity_score": round(similarity_score, 2)
                }
            }
            
    except Exception as e:
        logger.error(f"Error comparing words: {str(e)}", exc_info=True)
        return f"An error occurred while comparing words: {str(e)}"