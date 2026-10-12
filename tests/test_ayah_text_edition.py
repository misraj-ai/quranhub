"""
Regression test: /v1/ayah/... must resolve an audio edition's text through the
narrator's text edition (e.g. quran-warsh), not the audio identifier itself.
Passing the audio identifier never matched a text edition, so every audio
edition silently fell back to quran-simple (Hafs text and Hafs numbering).
"""

import asyncio
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import repositories.ayah_repo as ayah_repo
from utils.config import DEFAULT_EDITION_IDENTIFIER


def test_audio_edition_text_comes_from_narrator(monkeypatch):
    calls = []

    async def fake_narrator_lookup(identifier):
        calls.append(("narrator", identifier))
        return SimpleNamespace(id=999, identifier=identifier)

    async def fake_by_identifier(identifier):
        calls.append(("identifier", identifier))
        return SimpleNamespace(id=1, identifier=identifier)

    monkeypatch.setattr(ayah_repo, "get_text_edition_for_narrator", fake_narrator_lookup)
    monkeypatch.setattr(ayah_repo, "get_edition_by_identifier", fake_by_identifier)

    audio = SimpleNamespace(identifier="ar.abdulsamad.warsh", format="audio", narrator_identifier="quran-warsh")
    text = asyncio.run(ayah_repo._text_edition_for_audio(audio))

    assert text.identifier == "quran-warsh"
    assert calls == [("narrator", "quran-warsh")]


def test_audio_edition_without_narrator_uses_default(monkeypatch):
    calls = []

    async def fake_narrator_lookup(identifier):
        calls.append(("narrator", identifier))
        return None

    async def fake_by_identifier(identifier):
        calls.append(("identifier", identifier))
        return SimpleNamespace(id=1, identifier=identifier)

    monkeypatch.setattr(ayah_repo, "get_text_edition_for_narrator", fake_narrator_lookup)
    monkeypatch.setattr(ayah_repo, "get_edition_by_identifier", fake_by_identifier)

    audio = SimpleNamespace(identifier="xx.noname", format="audio", narrator_identifier=None)
    text = asyncio.run(ayah_repo._text_edition_for_audio(audio))

    assert text.identifier == DEFAULT_EDITION_IDENTIFIER
    assert calls == [("identifier", DEFAULT_EDITION_IDENTIFIER)]
