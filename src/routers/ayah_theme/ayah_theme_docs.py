APPLICATION_JSON = "application/json"

__all__ = ["getAyahThemesResponse", "getThemesForAyahResponse"]

getAyahThemesResponse = {
    200: {
        "description": "Returns a paginated list of all ayah themes.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": [
                            {
                                "name": "Claim of Al-Quran to be the Book of Allah",
                                "keywords": ["Allah"],
                                "totalAyahs": 2
                            },
                            {
                                "name": "Reward for the believers",
                                "keywords": [],
                                "totalAyahs": 1
                            },
                            {
                                "name": "How can you deny Allah?",
                                "keywords": ["Allah"],
                                "totalAyahs": 2
                            },
                            {
                                "name": "The story of Adam's creation",
                                "keywords": ["Adam"],
                                "totalAyahs": 1
                            },
                            {
                                "name": "Victory of knowledge",
                                "keywords": [],
                                "totalAyahs": 3
                            },
                            {
                                "name": "Shaitan caused Adam to lose paradise",
                                "keywords": ["Adam", "Shaitan"],
                                "totalAyahs": 1
                            }
                        ]
                    },
                    "empty": {
                        "summary": "No themes found",
                        "value": []
                    }
                }
            }
        }
    },
    404: {
        "description": "No themes found.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "not_found": {
                        "summary": "No themes found",
                        "value": {"code": 404, "status": "Not Found", "data": "No themes found."}
                    }
                }
            }
        }
    }
}
getThemesForAyahResponse = {
    200: {
        "description": "Returns all themes for a given ayah (by surah and ayah number).",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "success": {
                        "summary": "Canonical success response",
                        "value": [
                            {
                                "name": "Claim of Al-Quran to be the Book of Allah",
                                "keywords": ["Allah"],
                                "totalAyahs": 2
                            },
                            {
                                "name": "How can you deny Allah?",
                                "keywords": ["Allah"],
                                "totalAyahs": 1
                            }
                        ]
                    },
                    "empty": {
                        "summary": "No themes found for this ayah",
                        "value": []
                    }
                }
            }
        }
    },
    404: {
        "description": "No themes found for this ayah.",
        "content": {
            APPLICATION_JSON: {
                "examples": {
                    "not_found": {
                        "summary": "No themes found for this ayah",
                        "value": {"code": 404, "status": "Not Found", "data": "No themes found for this ayah."}
                    }
                }
            }
        }
    }
}
