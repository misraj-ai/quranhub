from typing import List, Tuple
from utils.logger import logger
from db.models import NarrationsNumbering
from db.session import AsyncSessionLocal
from sqlalchemy.future import select
from sqlalchemy.sql import func
import math

async def get_narration_numbering_from_narration(
    surah_number: int, ayah_number: int, source_edition_id: str, target_edition_id: str
) -> List[int]:
    """
    Retrieve narration numbering from a source edition to a target edition.
    
    Args:
        surah_number (int): The Surah number.
        ayah_number (int): The Ayah number.
        source_edition_id (str): Source edition ID (e.g., 'quran-warsh').
        target_edition_id (str): Target edition ID (e.g., 'quran-qaloon').

    Returns:
        List[int]: List of target edition numbering.
    """
    try:
        async with AsyncSessionLocal() as session:
            # First check if this surah exists in the narrations table
            check_query = select(func.count()).select_from(NarrationsNumbering).filter(
                NarrationsNumbering.surah_number == int(surah_number)
            )
            count_result = await session.execute(check_query)
            row_count = count_result.scalar()
            
            if row_count == 0:
                logger.warning(f"Surah {surah_number} does not exist in narrations_numbering table!")
                return [ayah_number]
            
            # Query the database for the specific surah
            query = select(NarrationsNumbering).filter(
                NarrationsNumbering.surah_number == int(surah_number)
            )
            result = await session.execute(query)
            rows = result.scalars().all()
            
            if not rows:
                logger.warning(f"No narration numbering rows found for Surah {surah_number}.")
                return [ayah_number]

            # Convert identifiers to Python attribute names (with underscores)
            # e.g., 'quran-warsh' → 'quran_warsh'
            source_attr = source_edition_id.replace('-', '_')
            target_attr = target_edition_id.replace('-', '_')
            
            # Find all rows that contain the ayah_number in the source_edition_id column
            target_edition_numbering = []
            
            for i, row in enumerate(rows):
                try:
                    source_column_data = getattr(row, source_attr, [])
                    
                    if ayah_number in source_column_data:
                        target_column_data = getattr(row, target_attr, [])
                        target_edition_numbering.extend(target_column_data)
                        break  # Found the match, no need to continue
                        
                except Exception as attr_error:
                    logger.error(
                        f"Cannot access attribute {source_attr} or {target_attr} in row {i+1}: {attr_error}"
                    )
                    
            if not target_edition_numbering:
                return [ayah_number]
                
            return target_edition_numbering

    except Exception as e:
        logger.error(f"Error fetching narration numbering: {str(e)}", exc_info=True)
        return []

# narrations_numbering_repo.py - Replace get_hafs_verse_for_narration_verse

async def get_hafs_verse_for_narration_verse(
    surah_number: int, 
    ayah_number: int, 
    edition_id: str
) -> List[int]:
    """
    Get the SPECIFIC Hafs verse(s) for this narration verse.
    
    Uses proper distribution, not proportional rounding.
    """
    try:
        async with AsyncSessionLocal() as session:
            query = select(NarrationsNumbering).filter(
                NarrationsNumbering.surah_number == int(surah_number)
            )
            result = await session.execute(query)
            rows = result.scalars().all()

            if not rows:
                return [ayah_number]

            target_attr = edition_id.replace('-', '_')
            hafs_attr = 'quran_hafs'
            
            for row in rows:
                target_data = getattr(row, target_attr, [])
                
                if ayah_number in target_data:
                    hafs_data = getattr(row, hafs_attr, [])
                    target_index = target_data.index(ayah_number)
                    
                    # CRITICAL FIX: Use ceiling division for proper distribution
                    if len(hafs_data) == len(target_data):
                        # 1-to-1
                        return [hafs_data[target_index]]
                    
                    elif len(hafs_data) > len(target_data):
                        # MERGE: Multiple Hafs → Fewer narration verses
                        # Distribute Hafs verses evenly across narration verses
                        verses_per_narration = len(hafs_data) / len(target_data)
                        start_idx = int(target_index * verses_per_narration)
                        end_idx = int((target_index + 1) * verses_per_narration)
                        
                        if target_index == len(target_data) - 1:
                            end_idx = len(hafs_data)
                        
                        if end_idx <= start_idx:
                            end_idx = start_idx + 1
                        
                        result_verses = hafs_data[start_idx:end_idx]
                        return result_verses if result_verses else [hafs_data[start_idx]]
                    
                    else:
                        # SPLIT: Fewer Hafs → More narration verses
                        # Use ceiling to properly distribute
                        narrations_per_hafs = len(target_data) / len(hafs_data)
                        hafs_index = min(
                            int(math.ceil((target_index + 1) / narrations_per_hafs)) - 1,
                            len(hafs_data) - 1
                        )
                        
                        logger.info(
                            f"SPLIT: {edition_id} {surah_number}:{ayah_number} "
                            f"(idx {target_index}/{len(target_data)}) → Hafs [{hafs_data[hafs_index]}]"
                        )
                        
                        return [hafs_data[hafs_index]]
                                
            return [ayah_number]
            
    except Exception as e:
        logger.error(f"Error in get_hafs_verse_for_narration_verse: {e}", exc_info=True)
        return [ayah_number]
    
async def get_narration_numbering_from_hafs(
    surah_number: int, ayah_number: int, edition_id: str
) -> Tuple[List[int], List[int]]:
    """
    Retrieve narration numbering from Hafs edition and another specified edition.
    
    IMPORTANT: After the database migration, this function now correctly handles
    merge scenarios where multiple Hafs verses map to a single narration verse.

    Args:
        surah_number (int): The Surah number.
        ayah_number (int): The Ayah number in the target narration.
        edition_id (str): Target edition ID (e.g., 'quran-warsh').

    Returns:
        Tuple[List[int], List[int]]: (hafs_edition_numbering, target_edition_numbering)
        
    Example:
        For Warsh verse 73:1, returns ([1, 2], [1]) because Warsh verse 1 = Hafs verses 1+2
    """
    try:
        async with AsyncSessionLocal() as session:
            # Query the database for the specific surah
            query = select(NarrationsNumbering).filter(
                NarrationsNumbering.surah_number == int(surah_number)
            )
            result = await session.execute(query)
            rows = result.scalars().all()

            if not rows:
                logger.info(f"No narration numbering found for Surah {surah_number}.")
                return [], []

            # Convert identifiers to Python attribute names (with underscores)
            # e.g., 'quran-warsh' → 'quran_warsh'
            target_attr = edition_id.replace('-', '_')
            hafs_attr = 'quran_hafs'  # Python attribute name
            
            # Find the row that contains the ayah_number in the edition_id column
            hafs_edition_numbering = []
            target_edition_numbering = []
            
            for row in rows:
                target_column_data = getattr(row, target_attr, [])
                if ayah_number in target_column_data:
                    hafs_column_data = getattr(row, hafs_attr, [])
                    hafs_edition_numbering.extend(hafs_column_data)
                    target_edition_numbering.extend(target_column_data)
                    break  # Found the match
            
            # Log for debugging
            if hafs_edition_numbering:
                logger.debug(
                    f"Narration mapping: {edition_id} {surah_number}:{ayah_number} → "
                    f"Hafs verses {hafs_edition_numbering}, Target verses {target_edition_numbering}"
                )
            else:
                logger.warning(
                    f"No narration mapping found for {edition_id} {surah_number}:{ayah_number}"
                )
                    
            return hafs_edition_numbering, target_edition_numbering

    except Exception as e:
        logger.error(f"Error fetching narration numbering from Hafs: {str(e)}", exc_info=True)
        return [], []