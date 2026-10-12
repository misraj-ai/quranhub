
"""
Word API Documentation (OpenAPI response examples)
"""

get_word_tajweed_response = {
    200: {
        "description": "Returns the tajweed rules for a specific word (surah:ayah:position) or all words in an ayah (surah:ayah). Use this to analyze or display tajweed for a word or entire ayah.",
        "content": {
            "application/json": {
                "examples": {
                    "word_format": {
                        "summary": "Specific Word (surah:ayah:position)",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "location": "1:1:2",
                                "tajweed": {
                                    "text": "ٱللَّهِ",
                                    "rules": [
                                        {"cls": "ham_wasl", "len": 1, "span": "ٱ", "offset": 1}
                                    ]
                                }
                            }
                        }
                    },
                    "ayah_format": {
                        "summary": "Entire Ayah (surah:ayah)",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "location": "1:1",
                                "words": [
                                    {
                                        "position": 1,
                                        "tajweed": {"text": "بِسۡمِ", "rules": []}
                                    },
                                    {
                                        "position": 2,
                                        "tajweed": {"text": "ٱللَّهِ", "rules": [{"cls": "ham_wasl", "len": 1, "span": "ٱ", "offset": 1}]}
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "No word was found for the given location. Check that the surah, ayah, and position are valid.",
        "content": {
            "application/json": {
                "example": {
                    "code": 404,
                    "status": "Error",
                    "data": "Word not found for location 1:1:2"
                }
            }
        }
    }
}

get_word_line_number_response = {
    200: {
        "description": "Returns the line number on the page for a specific word in the Quran, identified by its location (surah:ayah:position). Use this to map a word to its printed line in a Mushaf or digital display.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "location": "1:1:2",
                        "line_number": 9
                    }
                }
            }
        }
    },
    404: {
        "description": "No word was found for the given location. Check that the surah, ayah, and position are valid.",
        "content": {
            "application/json": {
                "example": {
                    "code": 404,
                    "status": "Error",
                    "data": "Word not found for location 1:1:2"
                }
            }
        }
    }
}

get_word_audio_response = {
    200: {
        "description": "Returns per-word audio URLs from a word-by-word audio edition, for a single word (surah:ayah:position) or every word in an ayah (surah:ayah). `audio` is null for the few words that have no recording.",
        "content": {
            "application/json": {
                "examples": {
                    "word_format": {
                        "summary": "Specific Word (surah:ayah:position)",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "location": "1:1:2",
                                "text": "ٱللَّهِ",
                                "number": 2,
                                "audio": "https://quranhub.b-cdn.net/quran/audio/wordbyword/128/ar.wordbyword.hafs/2.mp3",
                                "audioSecondary": [
                                    "https://quranhub.b-cdn.net/quran/audio/wordbyword/64/ar.wordbyword.hafs/2.mp3"
                                ],
                                "edition": {
                                    "identifier": "ar.wordbyword.hafs",
                                    "name": "تلاوة كلمة بكلمة",
                                    "englishName": "Word by Word Recitation",
                                    "format": "audio",
                                    "type": "wordbyword",
                                    "narratorIdentifier": "quran-hafs"
                                }
                            }
                        }
                    },
                    "ayah_format": {
                        "summary": "Entire Ayah (surah:ayah)",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "location": "1:1",
                                "edition": {
                                    "identifier": "ar.wordbyword.hafs",
                                    "name": "تلاوة كلمة بكلمة",
                                    "englishName": "Word by Word Recitation",
                                    "format": "audio",
                                    "type": "wordbyword",
                                    "narratorIdentifier": "quran-hafs"
                                },
                                "words": [
                                    {
                                        "position": 1,
                                        "location": "1:1:1",
                                        "text": "بِسۡمِ",
                                        "number": 1,
                                        "audio": "https://quranhub.b-cdn.net/quran/audio/wordbyword/128/ar.wordbyword.hafs/1.mp3",
                                        "audioSecondary": [
                                            "https://quranhub.b-cdn.net/quran/audio/wordbyword/64/ar.wordbyword.hafs/1.mp3"
                                        ]
                                    },
                                    {
                                        "position": 2,
                                        "location": "1:1:2",
                                        "text": "ٱللَّهِ",
                                        "number": 2,
                                        "audio": "https://quranhub.b-cdn.net/quran/audio/wordbyword/128/ar.wordbyword.hafs/2.mp3",
                                        "audioSecondary": [
                                            "https://quranhub.b-cdn.net/quran/audio/wordbyword/64/ar.wordbyword.hafs/2.mp3"
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "No word was found for the given location, or no word-by-word audio edition is available.",
        "content": {
            "application/json": {
                "example": {
                    "code": 404,
                    "status": "Error",
                    "data": "Word not found for location 1:1:2"
                }
            }
        }
    }
}

get_word_image_response = {
    200: {
        "description": "Returns the image URL for a specific word in the Quran, identified by its location (surah:ayah:position) and image type (v4, rq, qa). Use this to display a rendered image of the word in different tajweed styles or color schemes.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "location": "1:1:2",
                        "type": "v4",
                        "img_url": "https://quranhub.b-cdn.net/quran/images/word/v4/1:1:2.png"
                    }
                }
            }
        }
    },
    404: {
        "description": "No word was found for the given location. Check that the surah, ayah, and position are valid.",
        "content": {
            "application/json": {
                "example": {
                    "code": 404,
                    "status": "Error",
                    "data": "Word not found for location 1:1:2"
                }
            }
        }
    }
}
