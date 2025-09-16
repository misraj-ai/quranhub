APPLICATION_JSON = "application/json"

getSimilarAyahsResponse = {
    200: {
        "description": "Returns a list of similar ayah objects, each with canonical ayah and surah metadata, plus score, coverage, matchedWordsCount, and spans (with startPos, endPos, matchedText).",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": [
                            {
                                "number": 41,
                                "text": "Tanzeelun mina alrrahmani alrraheemi",
                                "numberInSurah": 2,
                                "juz": 24,
                                "manzil": 6,
                                "page": 482,
                                "ruku": 3,
                                "hizbQuarter": 189,
                                "hizb": 95,
                                "sajda": False,
                                "surah": {
                                    "id": 41,
                                    "name": "Fussilat",
                                    "englishName": "Fussilat",
                                    "englishTranslation": "Explained in Detail",
                                    "revelationCity": "Meccan",
                                    "numberOfAyahs": 54,
                                    "revelationOrder": 61
                                },
                                "score": 50,
                                "coverage": 50,
                                "matchedWordsCount": 2,
                                "spans": [
                                    {"startPos": 3, "endPos": 4, "matchedText": "alrrahmani alrraheemi"}
                                ],
                                "audio": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdulsamad.warsh/41.mp3",
                                "audioSecondary": [
                                    "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.husary.hafs/41.mp3"
                                ]
                            },
                            {
                                "number": 4482,
                                "text": "Waalhamdu lillahi rabbi alAAalameena",
                                "numberInSurah": 182,
                                "juz": 23,
                                "manzil": 6,
                                "page": 482,
                                "ruku": 3,
                                "hizbQuarter": 189,
                                "hizb": 95,
                                "sajda": False,
                                "surah": {
                                    "id": 37,
                                    "name": "As-Saffat",
                                    "englishName": "Those who set the Ranks",
                                    "englishTranslation": "As-Saffat",
                                    "revelationCity": "Meccan",
                                    "numberOfAyahs": 182,
                                    "revelationOrder": 56
                                },
                                "score": 99,
                                "coverage": 100,
                                "matchedWordsCount": 4,
                                "spans": [
                                    {"startPos": 1, "endPos": 4, "matchedText": "Waalhamdu lillahi rabbi alAAalameena"}
                                ],
                                "audio": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdulsamad.warsh/4482.mp3",
                                "audioSecondary": [
                                    "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.husary.hafs/4482.mp3"
                                ]
                            }
                        ]
                    },
                    "empty": {
                        "summary": "No similar ayahs found",
                        "value": []
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid surah or ayah number",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "invalid_surah": {
                        "summary": "Invalid Surah Number",
                        "value": {"code": 400, "status": "Error", "data": "Surah number must be between 1 and 114"}
                    },
                    "invalid_ayah": {
                        "summary": "Invalid Ayah Number",
                        "value": {"code": 400, "status": "Error", "data": "Invalid ayah number for this surah"}
                    }
                }
            }
        }
    },
    404: {
        "description": "No similar ayahs found for the given parameters or ayah does not exist in this narration.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "not_found": {
                        "summary": "No similar ayahs found",
                        "value": {"code": 404, "status": "Not Found", "data": "No similar ayahs found for the given parameters or ayah does not exist in this narration."}
                    }
                }
            }
        }
    }
}
