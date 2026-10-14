"""
Reciters-by-nationality endpoints: input validation (400), unknown nationality (404), and the success envelope.
The repository is stubbed, so no database is needed.
"""

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from repositories import edition_repo
from routers.edition import edition_router as router


def call(coro):
    response = asyncio.run(coro)
    return response.status_code, json.loads(response.body)


def by_nationality(code, **kw):
    return asyncio.run(router.get_audio_editions_by_reciter_nationality(countryCode=code, narrator=kw.get("narrator"), language=None, sortBy="ar"))


def test_invalid_country_code_is_400(monkeypatch):
    async def boom(*a, **k):
        raise AssertionError("repository must not be called for an invalid code")
    monkeypatch.setattr(edition_repo, "get_audio_editions_by_nationality", boom)
    for bad in ("SAU", "S", "1A", "S-"):
        response = by_nationality(bad)
        assert response.status_code == 400, bad


def test_unknown_nationality_is_404(monkeypatch):
    async def none(*a, **k):
        return "not_found"
    monkeypatch.setattr(edition_repo, "get_audio_editions_by_nationality", none)
    response = by_nationality("xx")
    assert response.status_code == 404
    assert json.loads(response.body)["data"] == "No audio editions found for nationality 'XX'"


def test_success_passes_filters_through(monkeypatch):
    seen = {}

    async def ok(code, narrator_identifier=None, language=None, sort_by=None):
        seen.update(code=code, narrator=narrator_identifier, sort=sort_by)
        return [{"identifier": "ar.alafasy.hafs", "nationality": {"code": "KW", "en": "Kuwait", "ar": "الكويت"}}]
    monkeypatch.setattr(edition_repo, "get_audio_editions_by_nationality", ok)
    response = by_nationality("kw", narrator="quran-hafs")
    body = json.loads(response.body)
    assert response.status_code == 200 and body["data"][0]["identifier"] == "ar.alafasy.hafs"
    assert seen == {"code": "KW", "narrator": "quran-hafs", "sort": "ar"}   # lower case input is normalised to upper case


def test_code_case_and_spaces_are_normalised(monkeypatch):
    seen = []

    async def ok(code, **kw):
        seen.append(code)
        return [{"identifier": "ar.x.hafs"}]
    monkeypatch.setattr(edition_repo, "get_audio_editions_by_nationality", ok)
    for raw in ("kw", "KW", "Kw", " kW "):
        assert by_nationality(raw).status_code == 200
    assert seen == ["KW"] * 4


def test_nationality_list_envelope(monkeypatch):
    async def lst():
        return [{"code": "SA", "en": "Saudi Arabia", "ar": "السعودية", "reciters": 65, "editions": 65}]
    monkeypatch.setattr(edition_repo, "get_audio_nationalities", lst)
    response = asyncio.run(router.get_reciter_nationalities())
    assert response.status_code == 200 and json.loads(response.body)["data"][0]["code"] == "SA"
