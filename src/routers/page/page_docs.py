"""
Enhanced OpenAPI documentation for Page endpoints.

This module provides comprehensive API documentation for page-related endpoints,
including examples with real data from the Quran API database covering all 604 pages
of the Mushaf, hizb information, and various query options.

Page Numbers: 1-604 (total pages in the standard Mushaf)
Features: Metadata endpoints, edition-specific queries, words inclusion, pagination
"""

# GET /page/metadata - Get All Pages Metadata
getAllPagesMetadataResponse = {
    200: {
        "description": "Returns metadata for all 604 Quran pages, including the first ayah, first surah, and hizb numbers for each page. Useful for navigation, search, and LLM workflows.",
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
                            "hizbNumbers": [1]
                        },
                        {
                            "number": 2,
                            "firstAyahNumber": 8,
                            "firstSurahNumber": 2,
                            "hizbNumbers": [1]
                        },
                        {
                            "number": 50,
                            "firstAyahNumber": 1204,
                            "firstSurahNumber": 4,
                            "hizbNumbers": [10]
                        },
                        {
                            "number": 300,
                            "firstAyahNumber": 3706,
                            "firstSurahNumber": 18,
                            "hizbNumbers": [30]
                        },
                        {
                            "number": 604,
                            "firstAyahNumber": 6213,
                            "firstSurahNumber": 114,
                            "hizbNumbers": [60]
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching page metadata. The response contains an error message explaining the failure.",
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

# GET /page/metadata/{editionIdentifier} - Get All Pages Metadata by Edition
getAllPagesMetadataByEditionResponse = {
    200: {
    "description": "Returns metadata for all 604 Quran pages from a specific edition. The editionIdentifier (e.g., 'quran-uthmani') must be provided as a path parameter, not as a query parameter. Includes the first ayah, first surah, hizb numbers, and edition details. Useful for edition-specific navigation and LLM workflows.",
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
                            "hizbNumbers": [1],
                            "edition": {
                                "identifier": "quran-uthmani",
                                "language": "ar",
                                "name": "Uthmani",
                                "englishName": "Uthmani",
                                "format": "text",
                                "type": "quran",
                                "direction": "rtl"
                            }
                        },
                        {
                            "number": 604,
                            "firstAyahNumber": 6213,
                            "firstSurahNumber": 114,
                            "hizbNumbers": [60],
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

# GET /page/{pageNumber} - Get Page By Number
getPagebyNumberResponse = {
    200: {
        "description": "Returns a specific Quran page (1-604) from the default edition, including all ayahs and metadata. Optionally includes word breakdowns. Useful for page navigation, display, and LLM workflows.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 1,
                        "hizbNumbers": [1],
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
                                "number": 2,
                                "text": "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ",
                                "surah": {
                                    "number": 1,
                                    "name": "سورة الفاتحة",
                                    "englishName": "Al-Faatiha",
                                    "englishNameTranslation": "The Opening",
                                    "revelationType": "Meccan",
                                    "numberOfAyahs": 7
                                },
                                "numberInSurah": 2,
                                "juz": 1,
                                "manzil": 1,
                                "page": 1,
                                "ruku": 1,
                                "hizbQuarter": 1,
                                "sajda": False
                            },
                            {
                                "number": 3,
                                "text": "ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
                                "surah": {
                                    "number": 1,
                                    "name": "سورة الفاتحة",
                                    "englishName": "Al-Faatiha",
                                    "englishNameTranslation": "The Opening",
                                    "revelationType": "Meccan",
                                    "numberOfAyahs": 7
                                },
                                "numberInSurah": 3,
                                "juz": 1,
                                "manzil": 1,
                                "page": 1,
                                "ruku": 1,
                                "hizbQuarter": 1,
                                "sajda": False
                            },
                            {
                                "number": 4,
                                "text": "مَٰلِكِ يَوْمِ ٱلدِّينِ",
                                "surah": {
                                    "number": 1,
                                    "name": "سورة الفاتحة",
                                    "englishName": "Al-Faatiha",
                                    "englishNameTranslation": "The Opening",
                                    "revelationType": "Meccan",
                                    "numberOfAyahs": 7
                                },
                                "numberInSurah": 4,
                                "juz": 1,
                                "manzil": 1,
                                "page": 1,
                                "ruku": 1,
                                "hizbQuarter": 1,
                                "sajda": False
                            },
                            {
                                "number": 5,
                                "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
                                "surah": {
                                    "number": 1,
                                    "name": "سورة الفاتحة",
                                    "englishName": "Al-Faatiha",
                                    "englishNameTranslation": "The Opening",
                                    "revelationType": "Meccan",
                                    "numberOfAyahs": 7
                                },
                                "numberInSurah": 5,
                                "juz": 1,
                                "manzil": 1,
                                "page": 1,
                                "ruku": 1,
                                "hizbQuarter": 1,
                                "sajda": False
                            },
                            {
                                "number": 6,
                                "text": "ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ",
                                "surah": {
                                    "number": 1,
                                    "name": "سورة الفاتحة",
                                    "englishName": "Al-Faatiha",
                                    "englishNameTranslation": "The Opening",
                                    "revelationType": "Meccan",
                                    "numberOfAyahs": 7
                                },
                                "numberInSurah": 6,
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
        "description": "Bad Request - Invalid page number or other error",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Page number should be between 1 and 604"
                }
            }
        }
    }
}

# GET /page/{pageNumber}/{editionIdentifier} - Get Page By Number and Edition
getPagebyEditionResponse = {
    200: {
        "description": "Returns a specific Quran page (1-604) from a particular edition, including all ayahs and metadata. Optionally includes word breakdowns. Useful for edition-specific navigation, display, and LLM workflows.",
        "content": {
            "application/json": {
                "examples": {
                    "arabic_uthmani": {
                        "summary": "Arabic Uthmani Text",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 2,
                                "hizbNumbers": [1],
                                "ayahs": [
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
                                        "number": 9,
                                        "text": "يُخَٰدِعُونَ ٱللَّهَ وَٱلَّذِينَ ءَامَنُوا۟ وَمَا يَخْدَعُونَ إِلَّآ أَنفُسَهُمْ وَمَا يَشْعُرُونَ",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 9,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 2,
                                        "ruku": 2,
                                        "hizbQuarter": 1,
                                        "sajda": False
                                    }
                                ],
                                "surahs": [
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
                    "english_translation": {
                        "summary": "English Translation",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 1,
                                "hizbNumbers": [1],
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
                                        "number": 2,
                                        "text": "[All] praise is [due] to Allah, Lord of the worlds -",
                                        "surah": {
                                            "number": 1,
                                            "name": "سورة الفاتحة",
                                            "englishName": "Al-Faatiha",
                                            "englishNameTranslation": "The Opening",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 7
                                        },
                                        "numberInSurah": 2,
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
                    },
                    "with_words": {
                        "summary": "Page with Word-by-Word Analysis",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 1,
                                "hizbNumbers": [1],
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
                                        "sajda": False,
                                        "words": [
                                            {
                                                "text": "بِسْمِ",
                                                "translation": {
                                                    "en": "In (the) name",
                                                    "bn": "নামে",
                                                    "tr": "adıyla",
                                                    "ur": "کے نام سے"
                                                },
                                                "transliteration": {
                                                    "en": "bis'mi"
                                                }
                                            },
                                            {
                                                "text": "ٱللَّهِ",
                                                "translation": {
                                                    "en": "(of) Allah",
                                                    "bn": "আল্লাহর",
                                                    "tr": "Allah'ın",
                                                    "ur": "اللہ"
                                                },
                                                "transliteration": {
                                                    "en": "l-lahi"
                                                }
                                            },
                                            {
                                                "text": "ٱلرَّحْمَٰنِ",
                                                "translation": {
                                                    "en": "the Most Gracious",
                                                    "bn": "পরম করুণাময়",
                                                    "tr": "Rahman'ın",
                                                    "ur": "رحمان"
                                                },
                                                "transliteration": {
                                                    "en": "r-raḥmāni"
                                                }
                                            },
                                            {
                                                "text": "ٱلرَّحِيمِ",
                                                "translation": {
                                                    "en": "the Most Merciful",
                                                    "bn": "অসীম দয়ালু",
                                                    "tr": "Rahim'in",
                                                    "ur": "رحیم"
                                                },
                                                "transliteration": {
                                                    "en": "r-raḥīmi"
                                                }
                                            }
                                        ]
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
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid page number, edition identifier, or other error",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_page_number": {
                        "summary": "Invalid Page Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Page number should be between 1 and 604"
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

# Enhanced response for pages with pagination/limits
getPageWithPaginationResponse = {
    200: {
        "description": "Successful Response - Page with limit and offset applied",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 50,
                        "hizbNumbers": [10],
                        "ayahs": [
                            {
                                "number": 1204,
                                "text": "يَٰٓأَيُّهَا ٱلنَّاسُ ٱتَّقُوا۟ رَبَّكُمُ ٱلَّذِى خَلَقَكُم مِّن نَّفْسٍۢ وَٰحِدَةٍۢ",
                                "surah": {
                                    "number": 4,
                                    "name": "سورة النساء",
                                    "englishName": "An-Nisaa",
                                    "englishNameTranslation": "The Women",
                                    "revelationType": "Medinan",
                                    "numberOfAyahs": 176
                                },
                                "numberInSurah": 1,
                                "juz": 4,
                                "manzil": 2,
                                "page": 50,
                                "ruku": 57,
                                "hizbQuarter": 19,
                                "sajda": False
                            },
                            {
                                "number": 1205,
                                "text": "وَخَلَقَ مِنْهَا زَوْجَهَا وَبَثَّ مِنْهُمَا رِجَالًۭا كَثِيرًۭا وَنِسَآءًۭ",
                                "surah": {
                                    "number": 4,
                                    "name": "سورة النساء",
                                    "englishName": "An-Nisaa",
                                    "englishNameTranslation": "The Women",
                                    "revelationType": "Medinan",
                                    "numberOfAyahs": 176
                                },
                                "numberInSurah": 2,
                                "juz": 4,
                                "manzil": 2,
                                "page": 50,
                                "ruku": 57,
                                "hizbQuarter": 19,
                                "sajda": False
                            }
                        ],
                        "surahs": [
                            {
                                "number": 4,
                                "name": "سورة النساء",
                                "englishName": "An-Nisaa",
                                "englishNameTranslation": "The Women",
                                "revelationType": "Medinan",
                                "numberOfAyahs": 176
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
                            "total_ayahs_in_page": 15,
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
