"""
Enhanced OpenAPI documentation for Juz endpoints.

This module provides comprehensive API documentation for juz-related endpoints,
including examples with real data from all 30 Juzs (Para/Sipara) of the Quran,
metadata endpoints, edition-specific queries, and pagination options.

Juz Numbers: 1-30 (total Juzs in the Quran)
Features: Metadata endpoints, edition-specific queries, pagination, multiple surahs per juz
"""

# GET /juz/metadata - Get All Juzs Metadata
getAllJuzsMetadataResponse = {
    200: {
        "description": "Returns metadata for all 30 Juzs (sections) of the Quran, including first/last ayah, surah, page, and ayah count. Useful for navigation, study, and LLM workflows.",
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
                            "lastAyahNumber": 148,
                            "lastSurahNumber": 2,
                            "lastPage": 21,
                            "ayahsCount": 148
                        },
                        {
                            "number": 2,
                            "firstAyahNumber": 149,
                            "firstSurahNumber": 2,
                            "firstPage": 22,
                            "lastAyahNumber": 309,
                            "lastSurahNumber": 2,
                            "lastPage": 41,
                            "ayahsCount": 161
                        },
                        {
                            "number": 15,
                            "firstAyahNumber": 2801,
                            "firstSurahNumber": 17,
                            "firstPage": 282,
                            "lastAyahNumber": 3159,
                            "lastSurahNumber": 18,
                            "lastPage": 301,
                            "ayahsCount": 359
                        },
                        {
                            "number": 30,
                            "firstAyahNumber": 5673,
                            "firstSurahNumber": 78,
                            "firstPage": 582,
                            "lastAyahNumber": 6236,
                            "lastSurahNumber": 114,
                            "lastPage": 604,
                            "ayahsCount": 564
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching Juz metadata. The response contains an error message explaining the failure.",
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

# GET /juz/metadata/{editionIdentifier} - Get All Juzs Metadata by Edition
getAllJuzsMetadataByEditionResponse = {
    200: {
    "description": "Returns metadata for all 30 Juzs from a specific edition. The editionIdentifier (e.g., 'quran-uthmani') must be provided as a path parameter, not as a query parameter. Includes first/last ayah, surah, page, ayah count, and edition details. Useful for edition-specific navigation and LLM workflows.",
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
                            "lastAyahNumber": 148,
                            "lastSurahNumber": 2,
                            "lastPage": 21,
                            "ayahsCount": 148,
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
                            "number": 30,
                            "firstAyahNumber": 5673,
                            "firstSurahNumber": 78,
                            "firstPage": 582,
                            "lastAyahNumber": 6236,
                            "lastSurahNumber": 114,
                            "lastPage": 604,
                            "ayahsCount": 564,
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
        "description": "Bad Request - Invalid edition identifier or other error. The response contains an error message explaining the failure.",
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

# GET /juz/{juzNumber} - Get Juz by Number
getTheJuzResponse = {
    200: {
        "description": "Returns a specific Juz (section) by its number (1-30) from the default edition, including all ayahs and metadata. Useful for navigation, study, and LLM workflows.",
        "content": {
            "application/json": {
                "examples": {
                    "juz_1": {
                        "summary": "Juz 1 - Al-Fatiha and part of Al-Baqarah",
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
                                        "number": 148,
                                        "text": "وَلِكُلٍّۢ وِجْهَةٌ هُوَ مُوَلِّيهَا ۖ فَٱسْتَبِقُوا۟ ٱلْخَيْرَٰتِ ۚ أَيْنَ مَا تَكُونُوا۟ يَأْتِ بِكُمُ ٱللَّهُ جَمِيعًا ۚ إِنَّ ٱللَّهَ عَلَىٰ كُلِّ شَىْءٍۢ قَدِيرٌۭ",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 148,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 21,
                                        "ruku": 18,
                                        "hizbQuarter": 8,
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
                    "juz_30": {
                        "summary": "Juz 30 - Amma (short surahs)",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 30,
                                "ayahs": [
                                    {
                                        "number": 5673,
                                        "text": "عَمَّ يَتَسَآءَلُونَ",
                                        "surah": {
                                            "number": 78,
                                            "name": "سورة النبأ",
                                            "englishName": "An-Naba",
                                            "englishNameTranslation": "The Announcement",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 40
                                        },
                                        "numberInSurah": 1,
                                        "juz": 30,
                                        "manzil": 7,
                                        "page": 582,
                                        "ruku": 518,
                                        "hizbQuarter": 233,
                                        "sajda": False
                                    },
                                    {
                                        "number": 5674,
                                        "text": "عَنِ ٱلنَّبَإِ ٱلْعَظِيمِ",
                                        "surah": {
                                            "number": 78,
                                            "name": "سورة النبأ",
                                            "englishName": "An-Naba",
                                            "englishNameTranslation": "The Announcement",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 40
                                        },
                                        "numberInSurah": 2,
                                        "juz": 30,
                                        "manzil": 7,
                                        "page": 582,
                                        "ruku": 518,
                                        "hizbQuarter": 233,
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
                                        "number": 78,
                                        "name": "سورة النبأ",
                                        "englishName": "An-Naba",
                                        "englishNameTranslation": "The Announcement",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 40
                                    },
                                    {
                                        "number": 79,
                                        "name": "سورة النازعات",
                                        "englishName": "An-Naazi'aat",
                                        "englishNameTranslation": "Those who drag forth",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 46
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
        "description": "Bad Request - Invalid juz number or other error",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_juz_number": {
                        "summary": "Invalid Juz Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Juz number must be between 1 and 30."
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

# GET /juz/{juzNumber}/{editionIdentifier} - Get Juz by Number and Edition
getTheJuzbyEditionResponse = {
    200: {
        "description": "Returns a specific Juz (section) by number from a particular edition, including all ayahs and metadata. Useful for edition-specific navigation, study, and LLM workflows.",
        "content": {
            "application/json": {
                "examples": {
                    "english_translation": {
                        "summary": "English Translation of Juz 30",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 30,
                                "ayahs": [
                                    {
                                        "number": 5673,
                                        "text": "About what are they asking one another?",
                                        "surah": {
                                            "number": 78,
                                            "name": "سورة النبأ",
                                            "englishName": "An-Naba",
                                            "englishNameTranslation": "The Announcement",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 40
                                        },
                                        "numberInSurah": 1,
                                        "juz": 30,
                                        "manzil": 7,
                                        "page": 582,
                                        "ruku": 518,
                                        "hizbQuarter": 233,
                                        "sajda": False
                                    },
                                    {
                                        "number": 5674,
                                        "text": "About the great news -",
                                        "surah": {
                                            "number": 78,
                                            "name": "سورة النبأ",
                                            "englishName": "An-Naba",
                                            "englishNameTranslation": "The Announcement",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 40
                                        },
                                        "numberInSurah": 2,
                                        "juz": 30,
                                        "manzil": 7,
                                        "page": 582,
                                        "ruku": 518,
                                        "hizbQuarter": 233,
                                        "sajda": False
                                    },
                                    {
                                        "number": 6236,
                                        "text": "From among the jinn and mankind.\"",
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
                                        "number": 78,
                                        "name": "سورة النبأ",
                                        "englishName": "An-Naba",
                                        "englishNameTranslation": "The Announcement",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 40
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
                        "summary": "Arabic Uthmani Text of Juz 1",
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
                                        "number": 148,
                                        "text": "وَلِكُلٍّۢ وِجْهَةٌ هُوَ مُوَلِّيهَا ۖ فَٱسْتَبِقُوا۟ ٱلْخَيْرَٰتِ ۚ أَيْنَ مَا تَكُونُوا۟ يَأْتِ بِكُمُ ٱللَّهُ جَمِيعًا ۚ إِنَّ ٱللَّهَ عَلَىٰ كُلِّ شَىْءٍۢ قَدِيرٌۭ",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 148,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 21,
                                        "ruku": 18,
                                        "hizbQuarter": 8,
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
                        "summary": "Juz with Limit and Offset",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 15,
                                "ayahs": [
                                    {
                                        "number": 2801,
                                        "text": "سُبْحَانَ ٱلَّذِىٓ أَسْرَىٰ بِعَبْدِهِۦ لَيْلًۭا مِّنَ ٱلْمَسْجِدِ ٱلْحَرَامِ",
                                        "surah": {
                                            "number": 17,
                                            "name": "سورة الإسراء",
                                            "englishName": "Al-Israa",
                                            "englishNameTranslation": "The Night Journey",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 111
                                        },
                                        "numberInSurah": 1,
                                        "juz": 15,
                                        "manzil": 4,
                                        "page": 282,
                                        "ruku": 320,
                                        "hizbQuarter": 113,
                                        "sajda": False
                                    },
                                    {
                                        "number": 2802,
                                        "text": "إِلَى ٱلْمَسْجِدِ ٱلْأَقْصَا ٱلَّذِى بَٰرَكْنَا حَوْلَهُۥ",
                                        "surah": {
                                            "number": 17,
                                            "name": "سورة الإسراء",
                                            "englishName": "Al-Israa",
                                            "englishNameTranslation": "The Night Journey",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 111
                                        },
                                        "numberInSurah": 2,
                                        "juz": 15,
                                        "manzil": 4,
                                        "page": 282,
                                        "ruku": 320,
                                        "hizbQuarter": 113,
                                        "sajda": False
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 17,
                                        "name": "سورة الإسراء",
                                        "englishName": "Al-Israa",
                                        "englishNameTranslation": "The Night Journey",
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
                                },
                                "pagination": {
                                    "total_ayahs_in_juz": 359,
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
        "description": "Bad Request - Invalid juz number, edition identifier, or other error",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_juz_number": {
                        "summary": "Invalid Juz Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Juz number must be between 1 and 30."
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
