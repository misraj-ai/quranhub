from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from db.session import AsyncSessionLocal
from db.models import Edition  # Assuming Edition is in a models module
from utils.logger import logger  # Assuming you have a logger module
from utils.config import TAFSIR_BOOKS_TRANSLATION, TAFSIR_BOOKS_LANGUAGES, TAFSIR_BOOKS_LEVELS, DEFAULT_EDITION_IDENTIFIER
from sqlalchemy.orm import selectinload

async def get_text_edition_for_narrator(narrator_identifier):
    """
    Get the text edition for a given narrator_identifier.
    If not found, fallback to DEFAULT_EDITION_IDENTIFIER.
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Edition).filter(
                    Edition.identifier == narrator_identifier,
                    Edition.format == "text"
                ).limit(1)
            )
            text_edition = result.scalar_one_or_none()
            
            if text_edition:
                return text_edition
            else:
                # Fallback to default edition if no text edition found for this narrator
                logger.warning(f"No text edition found for identifier: {narrator_identifier}. Using default edition.")
                return await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)
                
    except Exception as e:
        logger.error(f"Error fetching text edition for identifier {narrator_identifier}: {str(e)}")
        return await get_edition_by_identifier(DEFAULT_EDITION_IDENTIFIER)

async def get_editions_types():
    try:
        async with AsyncSessionLocal() as session:
            query = select(Edition.type).distinct()
            result = await session.execute(query)
            distinct_types = result.scalars().all()

        if not distinct_types:
            return "Types not found"

        return distinct_types

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching types."

async def get_editions_languages():
    try:
        async with AsyncSessionLocal() as session:
            query = select(Edition.language).distinct()
            result = await session.execute(query)
            distinct_languages = result.scalars().all()

        if not distinct_languages:
            return "Languages not found"

        return distinct_languages

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching languages."

async def get_editions_formats():
    try:
        async with AsyncSessionLocal() as session:
            query = select(Edition.format).distinct()
            result = await session.execute(query)
            distinct_formats = result.scalars().all()

        if not distinct_formats:
            return "Formats not found"

        return distinct_formats

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching formats."
    
async def get_editions_narrator_identifiers():
    try:
        async with AsyncSessionLocal() as session:
            query = select(Edition.narrator_identifier).filter(Edition.narrator_identifier.isnot(None)).distinct()
            result = await session.execute(query)
            distinct_narrations = result.scalars().all()

        if not distinct_narrations:
            return "Narrator Identifiers not found"

        return distinct_narrations

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching narrator identifiers."


def _format_audio_edition(item):
    """Format a single audio edition item."""
    reciter = item.reciter
    return {
        "identifier": item.identifier,
        "language": item.language,
        "name": item.name,
        "englishName": item.englishname,
        "imageUrl": reciter.image_url if reciter else None,
        "shortDescription": reciter.short_description if reciter else None,
        "format": item.format,
        "type": item.type,
        "direction": item.direction,
        "narratorIdentifier": item.narrator_identifier,
    }

def _format_default_edition(item):
    """Format a single default edition item."""
    return {
        "identifier": item.identifier,
        "language": item.language,
        "name": item.name,
        "englishName": item.englishname,
        "format": item.format,
        "type": item.type,
        "direction": item.direction,
        "narratorIdentifier": item.narrator_identifier
    }

def _format_tafsir_edition(item):
    """Format a single tafsir edition item, handling missing book in dictionary."""
    translated_name = []
    book_translations = TAFSIR_BOOKS_TRANSLATION.get(item.name, {})
    for lang in TAFSIR_BOOKS_LANGUAGES:
        translation = book_translations.get(lang)
        if translation:
            translated_name.append({lang: translation})
        else:
            translated_name.append({lang: None})

    level = None
    en_translation = book_translations.get("en")
    if en_translation:
        level = TAFSIR_BOOKS_LEVELS.get(en_translation)

    return {
        "identifier": item.identifier,
        "language": item.language,
        "name": item.name,
        "translatedName": translated_name,
        "format": item.format,
        "type": item.type,
        "direction": item.direction,
        "narratorIdentifier": item.narrator_identifier,
        "level": level,
        "imageUrl": item.tafsir.image_url if item.tafsir else None
    }


async def get_edition(language=None, type=None, format=None, narrator=None):
    try:
        async with AsyncSessionLocal() as session:
            query = select(Edition).options(
                selectinload(Edition.reciter),
                selectinload(Edition.tafsir)  # newly added
            )

            if language:
                query = query.filter(Edition.language == language)
            if type:
                query = query.filter(Edition.type == type)
            if format:
                query = query.filter(Edition.format == format)
            if narrator:
                query = query.filter(Edition.narrator_identifier == narrator)

            result = await session.execute(query)
            result = result.scalars().all()

        if not result:
            return "Edition not found"

        if type == "tafsir":
            return [_format_tafsir_edition(item) for item in result]

        if format == "audio":
            return [_format_audio_edition(item) for item in result]

        return [_format_default_edition(item) for item in result]

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching the edition."

async def get_edition_by_identifier(edition_identifier: str):
    """
    Retrieve an Edition by its identifier asynchronously.

    Args:
        edition_identifier (str): The identifier of the Edition to retrieve.

    Returns:
        Edition: The Edition object if exactly one is found.
        list: A list of Edition objects if multiple are found.
        None: If no Edition is found.

    Raises:
        SQLAlchemyError: If a database error occurs during the query.
        RuntimeError: If an unexpected error occurs.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Execute the query asynchronously
            result = await session.execute(
                select(Edition).filter(Edition.identifier == edition_identifier)
            )
            editions = result.scalars().all()

            # Handle the result
            if not editions:
                logger.info(f"No edition found for identifier: {edition_identifier}")
                return "Edition not found"
            elif len(editions) == 1:
                return editions[0]
            else:
                return editions

        except Exception as e:
            # Log any unexpected errors with details
            logger.error(f"Unexpected error while fetching edition with identifier '{edition_identifier}': {str(e)}")
            return "An unexpected error occurred, please try again later."
        

async def get_audio_edition_by_max_bitrate(narration_identifier: str):
    """
    Retrieve the audio edition with the maximum bitrate for a given narration identifier.

    Args:
        narration_identifier (str): The narration identifier for which to retrieve the audio edition.

    Returns:
        tuple: The maximum bitrate and the audio edition if found.
        None: If no audio editions are found or an error occurs.

    Raises:
        SQLAlchemyError: If a database error occurs during the query.
        RuntimeError: If an unexpected error occurs.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Query the editions asynchronously for the given narration identifier
            result = await session.execute(
                select(Edition.bitrates, Edition.identifier, Edition.name, Edition.narrator_identifier)
                .filter(Edition.narrator_identifier == narration_identifier)
            )

            editions = result.fetchall()

            if not editions:
                logger.info(f"No editions found for narration identifier: {narration_identifier}")
                return None

            # Flatten the list of bitrates and find the maximum bitrate
            all_bitrates = [bitrate for item in editions for bitrate in item.bitrates]
            if all_bitrates:
                max_bitrate = max(all_bitrates)

                # Find editions that match the max bitrate
                editions_with_max_bitrate = [item for item in editions if max_bitrate in item.bitrates]

                # Return the first edition with the max bitrate
                audio_edition = editions_with_max_bitrate[0]
                return max_bitrate, audio_edition

            return None  # No valid bitrates found

    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError while fetching audio edition for narration '{narration_identifier}': {str(e)}", exc_info=True)
        return "A database error occurred while fetching the audio edition."
    except Exception as e:
        logger.error(f"Unexpected error while fetching audio edition for narration '{narration_identifier}': {str(e)}", exc_info=True)
        return "An unexpected error occurred, please try again later."
    
async def get_distinct_audio_editions_by_englishname():
    """
    Returns a list of distinct audio editions using englishname.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get all audio editions, eager load reciter, order by englishname
            result = await session.execute(
                select(Edition)
                .options(selectinload(Edition.reciter))
                .filter(Edition.format == "audio")
                .order_by(Edition.englishname)
            )
            editions = result.scalars().all()

        # Use a dict to ensure uniqueness by englishname (first occurrence after sorting)
        unique = {}
        for item in editions:
            if item.englishname not in unique:
                formatted = _format_audio_edition(item)
                # Remove identifier, type, narratorIdentifier
                formatted.pop("identifier", None)
                formatted.pop("type", None)
                formatted.pop("narratorIdentifier", None)
                unique[item.englishname] = formatted

        return list(unique.values())

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return "An error occurred while fetching distinct audio editions."

async def get_edition_analysis():
    """
    Perform clean analysis of all editions in the database.
    Returns organized statistics with clear breakdowns by language, type, and format.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Load all editions with their relationships
            result = await session.execute(
                select(Edition).options(selectinload(Edition.reciter))
            )
            all_editions = result.scalars().all()

            if not all_editions:
                return {"error": "No editions found in database"}

            # Initialize analysis structure
            analysis = {
                "overview": {
                    "totalEditions": len(all_editions),
                    "textEditions": 0,
                    "audioEditions": 0,
                    "totalAudioFiles": 0
                },
                "formats": {},
                "types": {},
                "languages": {},
                "narrations": {},
                "reciters": {
                    "totalUniqueReciters": 0
                },
                "audioAnalysis": {
                    "byLanguage": {},
                    "byNarration": {},
                    "bitrates": {
                        "uniqueBitrates": 0,
                        "availableBitrates": [],
                        "statistics": {}
                    }
                }
            }

            # Track unique values
            all_bitrates = []
            reciter_counts = {}
            total_audio_files = 0  # New: sum of all audio files (per bitrate)

            # Process each edition
            for edition in all_editions:
                format_type = edition.format or "unknown"
                edition_type = edition.type or "unknown"
                language = edition.language or "unknown"
                narrator_id = edition.narrator_identifier

                # Overview counts
                if format_type == "text":
                    analysis["overview"]["textEditions"] += 1
                elif format_type == "audio":
                    analysis["overview"]["audioEditions"] += 1

                # Count formats
                if format_type not in analysis["formats"]:
                    analysis["formats"][format_type] = 0
                analysis["formats"][format_type] += 1

                # Count types
                if edition_type not in analysis["types"]:
                    analysis["types"][edition_type] = 0
                analysis["types"][edition_type] += 1

                # Enhanced language analysis with type breakdown
                if language not in analysis["languages"]:
                    analysis["languages"][language] = {
                        "total": 0,
                        "textEditions": 0,
                        "audioEditions": 0,
                        "textTypes": {},
                        "audioTypes": {}
                    }
                analysis["languages"][language]["total"] += 1

                if format_type == "text":
                    analysis["languages"][language]["textEditions"] += 1
                    if edition_type not in analysis["languages"][language]["textTypes"]:
                        analysis["languages"][language]["textTypes"][edition_type] = 0
                    analysis["languages"][language]["textTypes"][edition_type] += 1

                elif format_type == "audio":
                    analysis["languages"][language]["audioEditions"] += 1
                    if edition_type not in analysis["languages"][language]["audioTypes"]:
                        analysis["languages"][language]["audioTypes"][edition_type] = 0
                    analysis["languages"][language]["audioTypes"][edition_type] += 1

                # Narrations analysis - each narration has 1 text edition and multiple audio editions
                if narrator_id:
                    if narrator_id not in analysis["narrations"]:
                        analysis["narrations"][narrator_id] = {
                            "totalEditions": 0,
                            "textEditions": 1,  # Each narration has exactly 1 text edition
                            "audioEditions": 0
                        }
                    analysis["narrations"][narrator_id]["totalEditions"] += 1
                    # Only count audio editions - text edition is always 1 per narration
                    if format_type == "audio":
                        analysis["narrations"][narrator_id]["audioEditions"] += 1

                # Audio-specific analysis
                if format_type == "audio":
                    # Count audio files for this edition (per bitrate)
                    if edition_type in ("surah", "versebyverse"):
                        num_bitrates = len(edition.bitrates) if edition.bitrates else 0
                        if edition_type == "surah":
                            total_audio_files += num_bitrates * 114
                        elif edition_type == "versebyverse":
                            total_audio_files += num_bitrates * 6236

                    # Audio by language
                    if language not in analysis["audioAnalysis"]["byLanguage"]:
                        analysis["audioAnalysis"]["byLanguage"][language] = {
                            "editionCount": 0,
                            "types": {},
                            "uniqueNarrations": set()
                        }
                    analysis["audioAnalysis"]["byLanguage"][language]["editionCount"] += 1

                    if edition_type not in analysis["audioAnalysis"]["byLanguage"][language]["types"]:
                        analysis["audioAnalysis"]["byLanguage"][language]["types"][edition_type] = 0
                    analysis["audioAnalysis"]["byLanguage"][language]["types"][edition_type] += 1

                    if narrator_id:
                        analysis["audioAnalysis"]["byLanguage"][language]["uniqueNarrations"].add(narrator_id)

                    # Audio by narration
                    if narrator_id:
                        if narrator_id not in analysis["audioAnalysis"]["byNarration"]:
                            analysis["audioAnalysis"]["byNarration"][narrator_id] = {
                                "editionCount": 0,
                                "languages": set(),
                                "types": {}
                            }
                        analysis["audioAnalysis"]["byNarration"][narrator_id]["editionCount"] += 1
                        analysis["audioAnalysis"]["byNarration"][narrator_id]["languages"].add(language)

                        if edition_type not in analysis["audioAnalysis"]["byNarration"][narrator_id]["types"]:
                            analysis["audioAnalysis"]["byNarration"][narrator_id]["types"][edition_type] = 0
                        analysis["audioAnalysis"]["byNarration"][narrator_id]["types"][edition_type] += 1

                    # Collect bitrates
                    if edition.bitrates:
                        for bitrate in edition.bitrates:
                            all_bitrates.append(bitrate)

                # Track reciters
                if edition.reciter and edition.reciter.id:
                    reciter_id = edition.reciter.id
                    if reciter_id not in reciter_counts:
                        reciter_counts[reciter_id] = 0
                    reciter_counts[reciter_id] += 1


            # Finalize analysis
            # Convert sets to counts for JSON serialization
            for lang_data in analysis["audioAnalysis"]["byLanguage"].values():
                lang_data["uniqueNarrationsCount"] = len(lang_data["uniqueNarrations"])
                del lang_data["uniqueNarrations"]

            for narr_data in analysis["audioAnalysis"]["byNarration"].values():
                narr_data["languageCount"] = len(narr_data["languages"])
                del narr_data["languages"]

            # Reciter analysis - simplified
            analysis["reciters"]["totalUniqueReciters"] = len(reciter_counts)

            # Calculate total audio files: sum of (num_bitrates * 114) for surah, (num_bitrates * 6236) for versebyverse
            analysis["overview"]["totalAudioFiles"] = total_audio_files

            # Bitrate analysis
            unique_bitrates_list = sorted(list(set(all_bitrates))) if all_bitrates else []
            analysis["audioAnalysis"]["bitrates"]["uniqueBitrates"] = len(unique_bitrates_list)
            analysis["audioAnalysis"]["bitrates"]["availableBitrates"] = unique_bitrates_list

            if all_bitrates:
                analysis["audioAnalysis"]["bitrates"]["statistics"] = {
                    "average": round(sum(all_bitrates) / len(all_bitrates), 2),
                    "minimum": min(all_bitrates),
                    "maximum": max(all_bitrates)
                }

            return analysis

    except Exception as e:
        logger.error(f"Error in editions analysis: {str(e)}", exc_info=True)
        return {"error": "An error occurred while performing editions analysis."}

