"""
Enhanced OpenAPI documentation for Hizb endpoints.

This module provides comprehensive API documentation for hizb-related endpoints,
including examples with real data from all 60 Hizbs of the Quran.

Hizb Numbers: 1-60 (total Hizbs in the Quran, each being 1/60th of the Quran)
Features: Metadata endpoints, edition-specific queries, pagination options
Each Hizb contains multiple quarters (Rub al-Hizb) for easier reading sessions.
"""

# GET /hizb/metadata - Get All Hizbs Metadata
getAllHizbsMetadataResponse = {
    200: {
    "description": "Returns metadata for all 60 Hizbs of the Quran, including their first page, first ayah, and first surah. Use this to understand the structure and navigation of Hizbs.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "number": 1,
                            "firstAyahNumber": 1,
                            "firstSurahNumber": 1,
                            "firstPage": 1,
                            "lastAyahNumber": 37,
                            "lastSurahNumber": 2,
                            "lastPage": 5,
                            "ayahsCount": 37
                        },
                        {
                            "number": 30,
                            "firstAyahNumber": 1845,
                            "firstSurahNumber": 11,
                            "firstPage": 221,
                            "lastAyahNumber": 1944,
                            "lastSurahNumber": 12,
                            "lastPage": 235,
                            "ayahsCount": 100
                        },
                        {
                            "number": 60,
                            "firstAyahNumber": 6197,
                            "firstSurahNumber": 113,
                            "firstPage": 604,
                            "lastAyahNumber": 6236,
                            "lastSurahNumber": 114,
                            "lastPage": 604,
                            "ayahsCount": 40
                        }
                    ]
                }
            }
        }
    },
    400: {
    "description": "Bad request. The Hizb metadata could not be retrieved. Check the request or try again later.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something went wrong: Database connection failed"
                }
            }
        }
    }
}

# GET /hizb/metadata/{editionIdentifier} - Get All Hizbs Metadata by Edition
getAllHizbsMetadataByEditionResponse = {
    200: {
    "description": "Returns metadata for all Hizbs from a specific edition. The editionIdentifier (e.g., 'quran-uthmani') must be provided as a path parameter, not as a query parameter. Use this to understand the structure and navigation of Hizbs in a particular edition.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "number": 1,
                            "firstAyahNumber": 1,
                            "firstSurahNumber": 1,
                            "firstPage": 1,
                            "lastAyahNumber": 37,
                            "lastSurahNumber": 2,
                            "lastPage": 5,
                            "ayahsCount": 37,
                            "edition": {
                                "identifier": "en.sahih",
                                "language": "en",
                                "name": "Saheeh International",
                                "englishName": "Saheeh International",
                                "format": "text",
                                "type": "translation",
                                "direction": "ltr"
                            }
                        },
                        {
                            "number": 60,
                            "firstAyahNumber": 6197,
                            "firstSurahNumber": 113,
                            "firstPage": 604,
                            "lastAyahNumber": 6236,
                            "lastSurahNumber": 114,
                            "lastPage": 604,
                            "ayahsCount": 40,
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
                    ]
                }
            }
        }
    },
    400: {
    "description": "Bad request. The Hizb metadata for the specified edition could not be retrieved. Check the edition identifier or try again later.",
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

# GET /hizb/{hizbNumber} - Get Hizb by Number
getHizbbyNumberResponse = {
    200: {
    "description": "Returns the requested Hizb with all its ayahs from the default edition. Use this to fetch the content of a specific Hizb for display or analysis.",
        "content": {
            "application/json": {
                "examples": {
                    "hizb_1": {
                        "summary": "Hizb 1 - Beginning of the Quran",
                        "value": {
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
                                        "number": 8,
                                        "text": "وَمِنَ ٱلنَّاسِ مَن يَقُولُ ءَامَنَّا بِٱللَّهِ وَبِٱلْيَوْمِ ٱلْءَاخِرِ وَمَا هُم بِمُؤْمِنِينَ",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 8,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 2,
                                        "ruku": 2,
                                        "hizbQuarter": 1,
                                        "sajda": False
                                    },
                                    {
                                        "number": 37,
                                        "text": "وَمِنْهُم مَّن يَقُولُ رَبَّنَآ ءَاتِنَا فِى ٱلدُّنْيَا حَسَنَةًۭ وَفِى ٱلْءَاخِرَةِ حَسَنَةًۭ وَقِنَا عَذَابَ ٱلنَّارِ",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 37,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 5,
                                        "ruku": 4,
                                        "hizbQuarter": 2,
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
                                    },
                                    {
                                        "number": 2,
                                        "name": "سورة البقرة",
                                        "englishName": "Al-Baqarah",
                                        "englishNameTranslation": "The Cow",
                                        "revelationType": "Medinan",
                                        "numberOfAyahs": 286
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
                    },
                    "hizb_30": {
                        "summary": "Hizb 30 - Middle section",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 30,
                                "ayahs": [
                                    {
                                        "number": 1845,
                                        "text": "الٓرۚ تِلْكَ ءَايَٰتُ ٱلْكِتَٰبِ ٱلْمُبِينِ",
                                        "surah": {
                                            "number": 12,
                                            "name": "سورة يوسف",
                                            "englishName": "Yusuf",
                                            "englishNameTranslation": "Joseph",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 111
                                        },
                                        "numberInSurah": 1,
                                        "juz": 12,
                                        "manzil": 3,
                                        "page": 235,
                                        "ruku": 257,
                                        "hizbQuarter": 117,
                                        "sajda": False
                                    },
                                    {
                                        "number": 1944,
                                        "text": "لَقَدْ كَانَ فِى قَصَصِهِمْ عِبْرَةٌۭ لِّأُو۟لِى ٱلْأَلْبَٰبِ ۗ مَا كَانَ حَدِيثًۭا يُفْتَرَىٰ",
                                        "surah": {
                                            "number": 12,
                                            "name": "سورة يوسف",
                                            "englishName": "Yusuf",
                                            "englishNameTranslation": "Joseph",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 111
                                        },
                                        "numberInSurah": 111,
                                        "juz": 13,
                                        "manzil": 3,
                                        "page": 248,
                                        "ruku": 268,
                                        "hizbQuarter": 120,
                                        "sajda": False
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 12,
                                        "name": "سورة يوسف",
                                        "englishName": "Yusuf",
                                        "englishNameTranslation": "Joseph",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 111
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
                    },
                    "hizb_60": {
                        "summary": "Hizb 60 - Final hizb of the Quran",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 60,
                                "ayahs": [
                                    {
                                        "number": 6197,
                                        "text": "قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ",
                                        "surah": {
                                            "number": 113,
                                            "name": "سورة الفلق",
                                            "englishName": "Al-Falaq",
                                            "englishNameTranslation": "The Dawn",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 5
                                        },
                                        "numberInSurah": 1,
                                        "juz": 30,
                                        "manzil": 7,
                                        "page": 604,
                                        "ruku": 555,
                                        "hizbQuarter": 240,
                                        "sajda": False
                                    },
                                    {
                                        "number": 6236,
                                        "text": "مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ",
                                        "surah": {
                                            "number": 114,
                                            "name": "سورة الناس",
                                            "englishName": "An-Naas",
                                            "englishNameTranslation": "Mankind",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 6
                                        },
                                        "numberInSurah": 6,
                                        "juz": 30,
                                        "manzil": 7,
                                        "page": 604,
                                        "ruku": 556,
                                        "hizbQuarter": 240,
                                        "sajda": False
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 113,
                                        "name": "سورة الفلق",
                                        "englishName": "Al-Falaq",
                                        "englishNameTranslation": "The Dawn",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 5
                                    },
                                    {
                                        "number": 114,
                                        "name": "سورة الناس",
                                        "englishName": "An-Naas",
                                        "englishNameTranslation": "Mankind",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 6
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
            }
        }
    },
    400: {
    "description": "Bad request. The Hizb could not be retrieved. Check the hizb number or try again later.",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_hizb_number": {
                        "summary": "Invalid Hizb Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Hizb number should be between 1 and 60"
                        }
                    },
                    "general_error": {
                        "summary": "General Error",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Something went wrong"
                        }
                    }
                }
            }
        }
    }
}

# GET /hizb/{hizbNumber}/{editionIdentifier} - Get Hizb by Number and Edition
getHizbbyEditionResponse = {
    200: {
    "description": "Returns the requested Hizb from a specific edition. Use this to fetch the content of a specific Hizb in a specific edition for display or analysis.",
        "content": {
            "application/json": {
                "examples": {
                    "english_translation": {
                        "summary": "English Translation of Hizb 1",
                        "value": {
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
                                    },
                                    {
                                        "number": 8,
                                        "text": "And of the people are some who say, \"We believe in Allah and the Last Day,\" but they are not believers.",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 8,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 2,
                                        "ruku": 2,
                                        "hizbQuarter": 1,
                                        "sajda": False
                                    },
                                    {
                                        "number": 37,
                                        "text": "But among them are some who say, \"Our Lord, give us in this world [that which is] good and in the Hereafter [that which is] good and protect us from the punishment of the Fire.\"",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 37,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 5,
                                        "ruku": 4,
                                        "hizbQuarter": 2,
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
                                    },
                                    {
                                        "number": 2,
                                        "name": "سورة البقرة",
                                        "englishName": "Al-Baqarah",
                                        "englishNameTranslation": "The Cow",
                                        "revelationType": "Medinan",
                                        "numberOfAyahs": 286
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
                    },
                    "arabic_uthmani": {
                        "summary": "Arabic Uthmani Text of Hizb 30",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 30,
                                "ayahs": [
                                    {
                                        "number": 1845,
                                        "text": "الٓرۚ تِلْكَ ءَايَٰتُ ٱلْكِتَٰبِ ٱلْمُبِينِ",
                                        "surah": {
                                            "number": 12,
                                            "name": "سورة يوسف",
                                            "englishName": "Yusuf",
                                            "englishNameTranslation": "Joseph",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 111
                                        },
                                        "numberInSurah": 1,
                                        "juz": 12,
                                        "manzil": 3,
                                        "page": 235,
                                        "ruku": 257,
                                        "hizbQuarter": 117,
                                        "sajda": False
                                    },
                                    {
                                        "number": 1944,
                                        "text": "لَقَدْ كَانَ فِى قَصَصِهِمْ عِبْرَةٌۭ لِّأُو۟لِى ٱلْأَلْبَٰبِ ۗ مَا كَانَ حَدِيثًۭا يُفْتَرَىٰ",
                                        "surah": {
                                            "number": 12,
                                            "name": "سورة يوسف",
                                            "englishName": "Yusuf",
                                            "englishNameTranslation": "Joseph",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 111
                                        },
                                        "numberInSurah": 111,
                                        "juz": 13,
                                        "manzil": 3,
                                        "page": 248,
                                        "ruku": 268,
                                        "hizbQuarter": 120,
                                        "sajda": False
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 12,
                                        "name": "سورة يوسف",
                                        "englishName": "Yusuf",
                                        "englishNameTranslation": "Joseph",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 111
                                    }
                                ],
                                "edition": {
                                    "identifier": "quran-uthmani",
                                    "language": "ar",
                                    "name": "Uthmani",
                                    "englishName": "Uthmani",
                                    "format": "text",
                                    "type": "quran",
                                    "direction": "rtl"
                                }
                            }
                        }
                    },
                    "with_pagination": {
                        "summary": "Hizb with Limit and Offset",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 15,
                                "ayahs": [
                                    {
                                        "number": 936,
                                        "text": "الم",
                                        "surah": {
                                            "number": 7,
                                            "name": "سورة الأعراف",
                                            "englishName": "Al-A'raaf",
                                            "englishNameTranslation": "The Heights",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 206
                                        },
                                        "numberInSurah": 1,
                                        "juz": 8,
                                        "manzil": 3,
                                        "page": 151,
                                        "ruku": 154,
                                        "hizbQuarter": 57,
                                        "sajda": False
                                    },
                                    {
                                        "number": 937,
                                        "text": "كِتَٰبٌ أُنزِلَ إِلَيْكَ فَلَا يَكُن فِى صَدْرِكَ حَرَجٌۭ مِّنْهُ",
                                        "surah": {
                                            "number": 7,
                                            "name": "سورة الأعراف",
                                            "englishName": "Al-A'raaf",
                                            "englishNameTranslation": "The Heights",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 206
                                        },
                                        "numberInSurah": 2,
                                        "juz": 8,
                                        "manzil": 3,
                                        "page": 151,
                                        "ruku": 154,
                                        "hizbQuarter": 57,
                                        "sajda": False
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 7,
                                        "name": "سورة الأعراف",
                                        "englishName": "Al-A'raaf",
                                        "englishNameTranslation": "The Heights",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 206
                                    }
                                ],
                                "edition": {
                                    "identifier": "quran-uthmani",
                                    "language": "ar",
                                    "name": "Uthmani",
                                    "englishName": "Uthmani",
                                    "format": "text",
                                    "type": "quran",
                                    "direction": "rtl"
                                },
                                "pagination": {
                                    "total_ayahs_in_hizb": 104,
                                    "returned_ayahs": 2,
                                    "limit": 2,
                                    "offset": 0
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    400: {
    "description": "Bad request. The Hizb for the specified edition could not be retrieved. Check the hizb number, edition identifier, or try again later.",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_hizb_number": {
                        "summary": "Invalid Hizb Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Hizb number should be between 1 and 60"
                        }
                    },
                    "invalid_edition": {
                        "summary": "Edition Not Found",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Something went wrong: Edition not found"
                        }
                    },
                    "general_error": {
                        "summary": "General Error",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Something went wrong"
                        }
                    }
                }
            }
        }
    }
}
