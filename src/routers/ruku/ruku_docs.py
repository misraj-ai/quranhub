getRukubyNumberResponse={
        200: {
            "description": "Returns a specific Ruku (section) by its number (1-556) from the default edition, including all ayahs and metadata. Useful for navigation, study, and LLM workflows.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "status": "OK",
                        "data": {
                            "number": 1,
                            "ayahs": [
                                {
                                    "number": 1,
                                    "text": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
                                    "surah": {
                                        "number": 1,
                                        "name": "سورة الفاتحة",
                                        "englishName": "Al-Faatiha",
                                        "englishNameTranslation": "The Opening",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 7
                                    },
                                    "numberInSurah": 1,
                                    "juz": 1,
                                    "manzil": 1,
                                    "page": 1,
                                    "ruku": 1,
                                    "hizbQuarter": 1,
                                    "sajda": False
                                },
                                {
                                    "number": 7,
                                    "text": "صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ",
                                    "surah": {
                                        "number": 1,
                                        "name": "سورة الفاتحة",
                                        "englishName": "Al-Faatiha",
                                        "englishNameTranslation": "The Opening",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 7
                                    },
                                    "numberInSurah": 7,
                                    "juz": 1,
                                    "manzil": 1,
                                    "page": 1,
                                    "ruku": 1,
                                    "hizbQuarter": 1,
                                    "sajda": False
                                }
                            ],
                            "surahs": [
                                {
                                    "number": 1,
                                    "name": "سورة الفاتحة",
                                    "englishName": "Al-Faatiha",
                                    "englishNameTranslation": "The Opening",
                                    "revelationType": "Meccan",
                                    "numberOfAyahs": 7
                                }
                            ],
                            "edition": {
                                "identifier": "quran-simple",
                                "language": "ar",
                                "name": "Simple",
                                "englishName": "Simple",
                                "format": "text",
                                "type": "quran",
                                "direction": "rtl"
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad Request - Error occurred while fetching Ruku. The response contains an error message explaining the failure.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "Ruku number should be between 1 and 556"
                    }
                }
            }
        }
    }

getRukubyEditionResponse={
        200: {
            "description": "Returns a specific Ruku (section) by number from a particular edition, including all ayahs and metadata. Useful for edition-specific navigation, study, and LLM workflows.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "status": "OK",
                        "data": {
                            "number": 1,
                            "ayahs": [
                                {
                                    "number": 1,
                                    "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
                                    "surah": {
                                        "number": 1,
                                        "name": "سورة الفاتحة",
                                        "englishName": "Al-Faatiha",
                                        "englishNameTranslation": "The Opening",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 7
                                    },
                                    "numberInSurah": 1,
                                    "juz": 1,
                                    "manzil": 1,
                                    "page": 1,
                                    "ruku": 1,
                                    "hizbQuarter": 1,
                                    "sajda": False
                                }
                            ],
                            "surahs": [
                                {
                                    "number": 1,
                                    "name": "سورة الفاتحة",
                                    "englishName": "Al-Faatiha",
                                    "englishNameTranslation": "The Opening",
                                    "revelationType": "Meccan",
                                    "numberOfAyahs": 7
                                }
                            ],
                            "edition": {
                                "identifier": "en.sahih",
                                "language": "en",
                                "name": "Saheeh International",
                                "englishName": "Saheeh International",
                                "format": "text",
                                "type": "translation",
                                "direction": "ltr"
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad Request - Error occurred while fetching Ruku for the specified edition. The response contains an error message explaining the failure.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "Something went wrong: Edition not found"
                    }
                }
            }
        }
    }
