"""
Unit tests for audio URL helpers: per-ayah audio must only be attached to
verse-by-verse editions, and per-word audio only to word-by-word editions,
keyed by the global word number.
"""

import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest

from utils import word_numbering
from utils.config import BUNNY_URL, WORDBYWORD_MISSING_AUDIO
from utils.helpers import (
    add_ayah_audio,
    add_word_audio,
    get_word_audio_url,
    has_ayah_audio,
    has_word_audio,
    split_bitrates,
)


@pytest.fixture(autouse=True)
def word_counts():
    # Minimal word table: Al-Fatihah (29 words), 2:1 (1 word), then only the ayahs used below.
    counts = {(1, 1): 4, (1, 2): 4, (1, 3): 2, (1, 4): 3, (1, 5): 4, (1, 6): 3, (1, 7): 9, (2, 1): 1,
              (8, 66): 5, (37, 130): 3}
    word_numbering.set_word_counts(counts)
    yield
    word_numbering.set_word_counts({})


def edition(**overrides):
    base = dict(identifier="ar.test.hafs", format="audio", type="versebyverse", bitrates=[64, 128])
    base.update(overrides)
    return SimpleNamespace(**base)


def wbw(bitrates=(128, 64)):
    return edition(identifier="ar.wordbyword.hafs", type="wordbyword", bitrates=list(bitrates))


def test_split_bitrates_picks_max_and_keeps_the_rest():
    assert split_bitrates([64, 128, 32]) == (128, [64, 32])
    assert split_bitrates([128]) == (128, [])


def test_global_word_number_is_rank_in_surah_ayah_position_order():
    assert word_numbering.global_word_number(1, 1, 1) == 1
    assert word_numbering.global_word_number(1, 1, 4) == 4
    assert word_numbering.global_word_number(1, 2, 1) == 5
    assert word_numbering.global_word_number(1, 7, 9) == 29
    assert word_numbering.global_word_number(2, 1, 1) == 30
    assert word_numbering.global_word_number(99, 1, 1) is None


def test_versebyverse_edition_gets_ayah_audio():
    ayah = {"number": 7}
    add_ayah_audio(ayah, edition(), 7)
    assert ayah["audio"] == f"{BUNNY_URL}/audio/versebyverse/128/ar.test.hafs/7.mp3"
    assert ayah["audioSecondary"] == [f"{BUNNY_URL}/audio/versebyverse/64/ar.test.hafs/7.mp3"]


@pytest.mark.parametrize("kwargs", [
    dict(type="surah"),           # surah-only editions (e.g. ar.ghamdi.hafs) have no per-ayah files
    dict(type="wordbyword"),      # word-by-word editions carry audio on words, not ayahs
    dict(format="text", type="quran", bitrates=None),
    dict(bitrates=None),
    dict(bitrates=[]),
])
def test_non_versebyverse_editions_get_no_ayah_audio(kwargs):
    ayah = {"number": 7}
    assert not has_ayah_audio(edition(**kwargs))
    add_ayah_audio(ayah, edition(**kwargs), 7)
    assert "audio" not in ayah and "audioSecondary" not in ayah


def test_add_ayah_audio_tolerates_none_edition():
    ayah = {"number": 1}
    add_ayah_audio(ayah, None, 1)
    assert ayah == {"number": 1}


def test_word_audio_url_uses_global_word_number():
    assert get_word_audio_url(128, "ar.wordbyword.hafs", 6038) == f"{BUNNY_URL}/audio/wordbyword/128/ar.wordbyword.hafs/6038.mp3"


def test_wordbyword_edition_gets_word_audio_and_number():
    assert has_word_audio(wbw())
    word = {"text": "ٱللَّهِ"}
    add_word_audio(word, wbw(), 1, 1, 2)
    assert word["number"] == 2
    assert word["audio"] == f"{BUNNY_URL}/audio/wordbyword/128/ar.wordbyword.hafs/2.mp3"
    assert word["audioSecondary"] == [f"{BUNNY_URL}/audio/wordbyword/64/ar.wordbyword.hafs/2.mp3"]

    word = {"text": "الٓمٓ"}
    add_word_audio(word, wbw(), 2, 1, 1)
    assert word["number"] == 30 and word["audio"].endswith("/30.mp3")


def test_versebyverse_edition_gets_no_word_audio():
    word = {"text": "x"}
    assert not has_word_audio(edition())
    add_word_audio(word, edition(), 1, 1, 1)
    assert "audio" not in word and "number" not in word


def test_add_word_audio_tolerates_none_edition():
    word = {"text": "x"}
    add_word_audio(word, None, 1, 1, 1)
    assert word == {"text": "x"}


def test_words_without_source_audio_return_null_but_keep_number():
    assert "8:66:2" in WORDBYWORD_MISSING_AUDIO
    word = {}
    add_word_audio(word, wbw(), 8, 66, 2)
    assert word["audio"] is None and word["audioSecondary"] == []
    assert word["number"] == word_numbering.global_word_number(8, 66, 2)


def test_37_130_token_4_is_aliased_to_word_3():
    # quran-hafs text splits "إِلۡ يَاسِينَ" into two tokens; the word table and the audio have one word.
    n3 = word_numbering.global_word_number(37, 130, 3)
    word = {}
    add_word_audio(word, wbw([128]), 37, 130, 4)
    assert word["number"] == n3
    assert word["audio"].endswith(f"/{n3}.mp3")
    assert word["audioSecondary"] == []


def test_unknown_ayah_gives_no_audio_when_numbering_unavailable():
    word = {}
    add_word_audio(word, wbw(), 99, 1, 1)
    assert word == {}
