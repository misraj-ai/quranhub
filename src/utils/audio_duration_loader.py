"""
Audio Duration Loader

This module provides a singleton cache for pre-calculated audio durations.
Durations are loaded from a JSON file at application startup and cached in memory
for fast O(1) lookups during request processing.
"""

import json
import os
from typing import Dict, Optional
from utils.logger import logger


class AudioDurationCache:
    """Singleton cache for pre-calculated audio durations."""

    _instance = None
    _durations: Dict[str, int] = {}
    _metadata: Dict = {}
    _loaded: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioDurationCache, cls).__new__(cls)
        return cls._instance

    def load(self, file_path: str = None) -> bool:
        """
        Load durations from JSON file.

        Args:
            file_path: Path to audio_durations.json. If None, uses default path.

        Returns:
            True if loaded successfully, False otherwise
        """
        if self._loaded:
            logger.info("Audio durations already loaded")
            return True

        if file_path is None:
            # Default path: data/audio_durations.json relative to project root
            base_path = os.environ.get('AUDIO_DURATIONS_PATH',
                                      os.path.join(os.path.dirname(__file__), '../../data'))
            file_path = os.path.join(base_path, 'audio_durations.json')

        try:
            if not os.path.exists(file_path):
                logger.warning(f"Audio durations file not found: {file_path}")
                return False

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._durations = data.get('durations', {})
            self._metadata = data.get('metadata', {})
            self._loaded = True

            logger.info(f"Loaded {len(self._durations)} audio durations from {file_path}")
            if self._metadata:
                logger.info(f"Metadata: version={self._metadata.get('version')}, "
                          f"editions={len(self._metadata.get('editions', []))}, "
                          f"method={self._metadata.get('method')}")
            return True

        except Exception as e:
            logger.error(f"Failed to load audio durations: {e}", exc_info=True)
            return False

    def get_duration(self, edition: str, surah: int, verse: int) -> Optional[int]:
        """
        Get duration in milliseconds for a specific verse.

        Args:
            edition: Edition identifier (e.g., "ar.muhammadayyoub.hafs")
            surah: Surah number (1-114)
            verse: Global verse number (1-6236)

        Returns:
            Duration in milliseconds, or None if not found
        """
        key = f"{edition}:{surah}:{verse}"
        return self._durations.get(key)

    def has_edition(self, edition: str) -> bool:
        """Check if any durations exist for this edition."""
        prefix = f"{edition}:"
        return any(key.startswith(prefix) for key in self._durations.keys())

    def get_stats(self) -> Dict:
        """Get statistics about loaded durations."""
        return {
            "loaded": self._loaded,
            "totalDurations": len(self._durations),
            "metadata": self._metadata
        }


# Global singleton instance
_audio_duration_cache = AudioDurationCache()


def load_audio_durations(file_path: str = None) -> bool:
    """
    Load audio durations from JSON file.

    Args:
        file_path: Optional path to JSON file. If None, uses default location.

    Returns:
        True if loaded successfully, False otherwise
    """
    return _audio_duration_cache.load(file_path)


def get_audio_duration(edition: str, surah: int, verse: int) -> Optional[int]:
    """
    Get pre-calculated duration in milliseconds for a specific verse.

    Args:
        edition: Edition identifier (e.g., "ar.muhammadayyoub.hafs")
        surah: Surah number (1-114)
        verse: Global verse number (1-6236)

    Returns:
        Duration in milliseconds, or None if not found
    """
    return _audio_duration_cache.get_duration(edition, surah, verse)


def get_audio_duration_stats() -> Dict:
    """
    Get statistics about loaded durations.

    Returns:
        Dictionary containing loading status, total durations, and metadata
    """
    return _audio_duration_cache.get_stats()
