"""
Reciter metadata carries `nationality` ({code, en, ar} or null): the audio edition formatter exposes it.
"""

import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from repositories.edition_repo import _format_audio_edition


def edition(nationality):
    reciter = SimpleNamespace(image_url=None, short_description={"ar": "..", "en": ".."}, nationality=nationality)
    return SimpleNamespace(identifier="ar.x.hafs", language="ar", format="audio", type="surah", subtype="recitation",
                           bitrates=[128], direction=None, narrator_identifier="quran-hafs",
                           name={"ar": "قارئ", "en": "Reciter"}, reciter=reciter)


def test_formatter_exposes_nationality():
    nat = {"code": "SA", "en": "Saudi Arabia", "ar": "السعودية"}
    assert _format_audio_edition(edition(nat))["nationality"] == nat


def test_formatter_returns_null_when_unknown():
    assert _format_audio_edition(edition(None))["nationality"] is None
