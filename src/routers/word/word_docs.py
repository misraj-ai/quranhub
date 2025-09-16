
"""
Word API Documentation (OpenAPI response examples)
"""

get_word_tajweed_response = {
    200: {
        "description": "Returns the tajweed rules for a specific word in the Quran, identified by its location (surah:ayah:position). Use this to analyze or display tajweed for a word in context.",
        "content": {
            "application/json": {
                "example": {
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
