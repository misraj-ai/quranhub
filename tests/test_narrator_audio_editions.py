"""
The narrator audio listing returns one entry per edition identifier: a reciter
with both a surah row and a verse-by-verse row appears once (verse-by-verse
fields first), surah-only reciters are included, word-by-word is excluded, and
`types` lists every layout with its bitrates.
"""

import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from repositories.edition_repo import _group_audio_editions_by_identifier


def row(identifier, type_, bitrates, en="Reciter"):
    reciter = SimpleNamespace(image_url=f"https://cdn/{identifier}.jpeg", short_description={"ar": "..", "en": ".."})
    return SimpleNamespace(
        identifier=identifier, language="ar", format="audio", type=type_, subtype="recitation",
        bitrates=bitrates, direction=None, narrator_identifier="quran-hafs",
        name={"ar": "قارئ", "en": en}, reciter=reciter,
    )


def test_surah_and_versebyverse_rows_collapse_into_one_entry():
    items = [row("ar.alafasy.hafs", "surah", [128]), row("ar.alafasy.hafs", "versebyverse", [64, 128])]
    out = _group_audio_editions_by_identifier(items)
    assert [e["identifier"] for e in out] == ["ar.alafasy.hafs"]
    assert out[0]["type"] == "versebyverse"          # base fields come from the verse-by-verse row
    assert out[0]["types"] == [
        {"type": "versebyverse", "bitrates": [128, 64]},
        {"type": "surah", "bitrates": [128]},
    ]


def test_surah_only_reciter_is_listed_with_surah_type_only():
    out = _group_audio_editions_by_identifier([row("ar.ghamdi.hafs", "surah", [256])])
    assert len(out) == 1
    assert out[0]["identifier"] == "ar.ghamdi.hafs"
    assert out[0]["type"] == "surah"
    assert out[0]["types"] == [{"type": "surah", "bitrates": [256]}]


def test_word_by_word_rows_are_excluded_and_order_is_preserved():
    items = [
        row("ar.husary.hafs", "versebyverse", [128, 64]),
        row("ar.wordbyword.hafs", "wordbyword", [128, 64]),
        row("ar.ghamdi.hafs", "surah", [256]),
        row("ar.husary.hafs", "surah", [128]),
    ]
    out = _group_audio_editions_by_identifier(items)
    assert [e["identifier"] for e in out] == ["ar.husary.hafs", "ar.ghamdi.hafs"]


def test_mujawwad_detection_still_works_on_the_grouped_entry():
    out = _group_audio_editions_by_identifier(
        [row("ar.husarymujawwad.hafs", "surah", [64], en="Mahmoud Khalil Al-Husary Mujawwad")]
    )
    assert out[0]["recitationType"] == "mujawwad"
