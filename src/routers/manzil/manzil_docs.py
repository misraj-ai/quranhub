"""
Enhanced OpenAPI documentation for Manzil endpoints.

This module provides comprehensive API documentation for manzil-related endpoints,
including examples with real data from all 7 Manzils of the Quran. 

Manzil Numbers: 1-7 (traditional seven-section division of the Quran for weekly reading)
Features: Edition-specific queries, pagination options, multiple surahs per manzil

Manzil divisions:
- Manzil 1: Al-Fatiha to An-Nisa (4:23)  
- Manzil 2: An-Nisa (4:24) to Al-An'am
- Manzil 3: Al-A'raf to At-Tawbah
- Manzil 4: Yunus to An-Nahl
- Manzil 5: Al-Isra to Al-Furqan
- Manzil 6: Ash-Shu'ara to Ya-Sin
- Manzil 7: As-Saffat to An-Nas
"""

# GET /manzil/{manzilNumber} - Get Manzil by Number
getManzilbyNumberResponse = {
    200: {
        "description": "Returns a specific Manzil (one of 7 weekly sections) by its number (1-7) from the default edition, including all ayahs and metadata. Useful for weekly reading plans, navigation, and LLM workflows.",
        "content": {
            "application/json": {
                "examples": {
                    "manzil_1": {
                        "summary": "Manzil 1 - Al-Fatiha to part of An-Nisa",
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
                                        "number": 1227,
                                        "text": "وَلَا تَنكِحُوا۟ مَا نَكَحَ ءَابَآؤُكُم مِّنَ ٱلنِّسَآءِ إِلَّا مَا قَدْ سَلَفَ ۚ إِنَّهُۥ كَانَ فَٰحِشَةًۭ وَمَقْتًۭا وَسَآءَ سَبِيلًا",
                                        "surah": {
                                            "number": 4,
                                            "name": "سورة النساء",
                                            "englishName": "An-Nisaa",
                                            "englishNameTranslation": "The Women",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 176
                                        },
                                        "numberInSurah": 23,
                                        "juz": 4,
                                        "manzil": 1,
                                        "page": 81,
                                        "ruku": 57,
                                        "hizbQuarter": 30,
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
                                    },
                                    {
                                        "number": 3,
                                        "name": "سورة آل عمران",
                                        "englishName": "Aal-i-Imraan",
                                        "englishNameTranslation": "Family of Imran",
                                        "revelationType": "Medinan",
                                        "numberOfAyahs": 200
                                    },
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
                    "manzil_7": {
                        "summary": "Manzil 7 - As-Saffat to An-Nas (final section)",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 7,
                                "ayahs": [
                                    {
                                        "number": 4620,
                                        "text": "وَٱلصَّٰٓفَّٰتِ صَفًّۭا",
                                        "surah": {
                                            "number": 37,
                                            "name": "سورة الصافات",
                                            "englishName": "As-Saaffaat",
                                            "englishNameTranslation": "Those who set the Ranks",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 182
                                        },
                                        "numberInSurah": 1,
                                        "juz": 23,
                                        "manzil": 7,
                                        "page": 446,
                                        "ruku": 400,
                                        "hizbQuarter": 177,
                                        "sajda": False
                                    },
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
                                        "number": 37,
                                        "name": "سورة الصافات",
                                        "englishName": "As-Saaffaat",
                                        "englishNameTranslation": "Those who set the Ranks",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 182
                                    },
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
        "description": "Bad Request - Invalid manzil number or other error",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_manzil_number": {
                        "summary": "Invalid Manzil Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Manzil number should be between 1 and 7"
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

# GET /manzil/{manzilNumber}/{editionIdentifier} - Get Manzil by Number and Edition
getManzilbyEditionResponse = {
    200: {
        "description": "Returns a specific Manzil (one of 7 weekly sections) by number from a particular edition, including all ayahs and metadata. Useful for edition-specific weekly reading, navigation, and LLM workflows.",
        "content": {
            "application/json": {
                "examples": {
                    "english_translation": {
                        "summary": "English Translation of Manzil 1",
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
                                        "number": 1227,
                                        "text": "And do not marry those [women] whom your fathers married, except what has already occurred. Indeed, it was an immorality and hateful [to Allah] and was evil as a way.",
                                        "surah": {
                                            "number": 4,
                                            "name": "سورة النساء",
                                            "englishName": "An-Nisaa",
                                            "englishNameTranslation": "The Women",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 176
                                        },
                                        "numberInSurah": 23,
                                        "juz": 4,
                                        "manzil": 1,
                                        "page": 81,
                                        "ruku": 57,
                                        "hizbQuarter": 30,
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
                                    },
                                    {
                                        "number": 3,
                                        "name": "سورة آل عمران",
                                        "englishName": "Aal-i-Imraan",
                                        "englishNameTranslation": "Family of Imran",
                                        "revelationType": "Medinan",
                                        "numberOfAyahs": 200
                                    },
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
                        "summary": "Arabic Uthmani Text of Manzil 4",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 4,
                                "ayahs": [
                                    {
                                        "number": 2842,
                                        "text": "يُونُسَ وَمُوسَىٰ وَهَٰرُونَ ۚ وَكَذَٰلِكَ نَجْزِى ٱلْمُحْسِنِينَ",
                                        "surah": {
                                            "number": 10,
                                            "name": "سورة يونس",
                                            "englishName": "Yunus",
                                            "englishNameTranslation": "Jonah",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 109
                                        },
                                        "numberInSurah": 1,
                                        "juz": 11,
                                        "manzil": 4,
                                        "page": 208,
                                        "ruku": 211,
                                        "hizbQuarter": 81,
                                        "sajda": False
                                    },
                                    {
                                        "number": 3756,
                                        "text": "وَأَوْحَيْنَآ إِلَىٰ أُمِّ مُوسَىٰٓ أَنْ أَرْضِعِيهِ ۖ فَإِذَا خِفْتِ عَلَيْهِ فَأَلْقِيهِ فِى ٱلْيَمِّ",
                                        "surah": {
                                            "number": 16,
                                            "name": "سورة النحل",
                                            "englishName": "An-Nahl",
                                            "englishNameTranslation": "The Bee",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 128
                                        },
                                        "numberInSurah": 128,
                                        "juz": 14,
                                        "manzil": 4,
                                        "page": 281,
                                        "ruku": 318,
                                        "hizbQuarter": 112,
                                        "sajda": False
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 10,
                                        "name": "سورة يونس",
                                        "englishName": "Yunus",
                                        "englishNameTranslation": "Jonah",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 109
                                    },
                                    {
                                        "number": 16,
                                        "name": "سورة النحل",
                                        "englishName": "An-Nahl",
                                        "englishNameTranslation": "The Bee",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 128
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
                        "summary": "Manzil with Limit and Offset",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 2,
                                "ayahs": [
                                    {
                                        "number": 1228,
                                        "text": "حُرِّمَتْ عَلَيْكُمْ أُمَّهَٰتُكُمْ وَبَنَاتُكُمْ وَأَخَوَٰتُكُمْ",
                                        "surah": {
                                            "number": 4,
                                            "name": "سورة النساء",
                                            "englishName": "An-Nisaa",
                                            "englishNameTranslation": "The Women",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 176
                                        },
                                        "numberInSurah": 24,
                                        "juz": 4,
                                        "manzil": 2,
                                        "page": 81,
                                        "ruku": 57,
                                        "hizbQuarter": 30,
                                        "sajda": False
                                    },
                                    {
                                        "number": 1229,
                                        "text": "وَعَمَّٰتُكُمْ وَخَٰلَٰتُكُمْ وَبَنَاتُ ٱلْأَخِ وَبَنَاتُ ٱلْأُخْتِ",
                                        "surah": {
                                            "number": 4,
                                            "name": "سورة النساء",
                                            "englishName": "An-Nisaa",
                                            "englishNameTranslation": "The Women",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 176
                                        },
                                        "numberInSurah": 25,
                                        "juz": 5,
                                        "manzil": 2,
                                        "page": 81,
                                        "ruku": 57,
                                        "hizbQuarter": 30,
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
                                    "total_ayahs_in_manzil": 1171,
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
        "description": "Bad Request - Invalid manzil number, edition identifier, or other error",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_manzil_number": {
                        "summary": "Invalid Manzil Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Manzil number should be between 1 and 7"
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
