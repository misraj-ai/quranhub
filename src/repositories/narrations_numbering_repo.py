from typing import List, Tuple
from utils.logger import logger
from db.models import NarrationsNumbering
from db.session import AsyncSessionLocal
from sqlalchemy.future import select
from sqlalchemy.sql import func


async def get_narration_numbering_from_narration(
    surah_number: int, ayah_number: int, source_edition_id: str, target_edition_id: str
) -> List[int]:
    """
    Retrieve narration numbering from a source edition to a target edition.
    
    The database structure has multiple rows per surah, where each row represents
    a mapping between ayah numbers in different narrations.

    Args:
        surah_number (int): The Surah number.
        ayah_number (int): The Ayah number.
        source_edition_id (str): Source edition ID column name.
        target_edition_id (str): Target edition ID column name.

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
                return [ayah_number]  # Return same ayah if no narration data exists
            
            # Query the database for the specific surah
            query = select(NarrationsNumbering).filter(
                NarrationsNumbering.surah_number == int(surah_number)
            ).order_by(NarrationsNumbering.quran_hafs)  # Order by hafs for consistent processing
            result = await session.execute(query)
            rows = result.scalars().all()
            
            if not rows:
                logger.warning(f"No narration numbering rows found for Surah {surah_number}.")
                return [ayah_number]  # Return same ayah if no narration data exists

            # Convert identifiers to Python attribute names
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
                    logger.error(f"Cannot access attribute {source_attr} or {target_attr} in row {i+1}: {attr_error}")
                    
            if not target_edition_numbering:
                # If no conversion exists, it means this ayah is the same in both narrations
                return [ayah_number]
                
            return target_edition_numbering

    except Exception as e:
        logger.error(f"Error fetching narration numbering: {str(e)}", exc_info=True)
        return []


async def get_narration_numbering_from_hafs(
    surah_number: int, ayah_number: int, edition_id: str
) -> Tuple[List[int], List[int]]:
    """
    Retrieve narration numbering from Hafs edition and another specified edition.

    Args:
        surah_number (int): The Surah number.
        ayah_number (int): The Ayah number.
        edition_id (str): Target edition ID column name.

    Returns:
        Tuple[List[int], List[int]]: (hafs_edition_numbering, target_edition_numbering)

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

            # Find the row that contains the ayah_number in the edition_id column
            hafs_edition_numbering = []
            target_edition_numbering = []
            
            for row in rows:
                target_column_data = getattr(row, edition_id.replace('-', '_'), [])
                if ayah_number in target_column_data:
                    hafs_column_data = getattr(row, 'quran_hafs', [])
                    hafs_edition_numbering.extend(hafs_column_data)
                    target_edition_numbering.extend(target_column_data)
                    break
                    
            return hafs_edition_numbering, target_edition_numbering

    except Exception as e:
        logger.error(f"Error fetching narration numbering from Hafs: {str(e)}", exc_info=True)
        return [], []