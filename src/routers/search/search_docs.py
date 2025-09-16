# Enhanced Quran Search API Documentation
# Real response examples from the enhanced keyword repository with pg_trgm fuzzy search

getKeywordbySurahAndLanguageOrEditionResponse = {
    200: {
        "description": "Returns ayahs (verses) matching a keyword in the Quran, with support for language detection, edition selection, exact/fuzzy matching, and Surah filtering. Each ayah result includes similarity metrics: 'similarity' (character-level), 'wordSimilarity' (word-level/phrase), and 'relevanceScore' (composite, 100-50 scale). Results are sorted by: relevanceScore DESC, wordSimilarity DESC, similarity DESC, ayah number ASC. Useful for LLMs, search UIs, and advanced workflows.",
        "content": {
            "application/json": {
                "examples": {
                    "arabic_exact_search": {
                        "summary": "Arabic Exact Search with Diacritics",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "keyword": "ٱلْحَمْدُ لِلَّهِ",
                                "normalizedKeyword": "الحمد لله",
                                "isArabic": True,
                                "exactSearch": True,
                                "searchType": "exact",
                                "count": 5,
                                "ayahs": [
                                    {
                                        "number": 2,
                                        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
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
                                        "count": 1
                                    }
                                ],
                                "edition": {
                                    "identifier": "quran-simple-clean",
                                    "language": "ar",
                                    "name": "Simple Clean",
                                    "englishName": "Simple Clean",
                                    "format": "text",
                                    "type": "quran",
                                    "direction": "rtl"
                                }
                            }
                        }
                    },
                    "arabic_fuzzy_search_with_typos": {
                        "summary": "Arabic Fuzzy Search Handling Typos",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "keyword": "الحمدو لله",
                                "normalizedKeyword": "الحمدو لله",
                                "isArabic": True,
                                "exactSearch": False,
                                "searchType": "fuzzy",
                                "count": 10,
                                "ayahs": [
                                    {
                                        "number": 2,
                                        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
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
                                        "sajda": False,
                                        "similarity": {
                                            "similarity": 0.40909090638160706,
                                            "wordSimilarity": 0.75,
                                            "relevanceScore": 90
                                        }
                                    },
                                    {
                                        "number": 2141,
                                        "text": "الْحَمْدُ لِلَّهِ الَّذِي أَنْزَلَ عَلَىٰ عَبْدِهِ الْكِتَابَ وَلَمْ يَجْعَلْ لَهُ عِوَجًا ۜ",
                                        "surah": {
                                            "number": 18,
                                            "name": "سورة الكهف",
                                            "englishName": "Al-Kahf",
                                            "englishNameTranslation": "The Cave",
                                            "revelationType": "Meccan",
                                            "numberOfAyahs": 110
                                        },
                                        "numberInSurah": 1,
                                        "juz": 15,
                                        "manzil": 4,
                                        "page": 293,
                                        "ruku": 252,
                                        "hizbQuarter": 117,
                                        "sajda": False,
                                        "similarity": {
                                            "similarity": 0.18367347121238708,
                                            "wordSimilarity": 0.75,
                                            "relevanceScore": 90
                                        }
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 1,
                                        "name": "سورة الفاتحة",
                                        "englishName": "Al-Faatiha",
                                        "englishNameTranslation": "The Opening",
                                        "count": 1
                                    },
                                    {
                                        "number": 18,
                                        "name": "سورة الكهف",
                                        "englishName": "Al-Kahf",
                                        "englishNameTranslation": "The Cave",
                                        "count": 1
                                    }
                                ],
                                "edition": {
                                    "identifier": "quran-simple-clean",
                                    "language": "ar",
                                    "name": "Simple Clean",
                                    "englishName": "Simple Clean",
                                    "format": "text",
                                    "type": "quran",
                                    "direction": "rtl"
                                }
                            }
                        }
                    },
                    "english_fuzzy_search": {
                        "summary": "English Fuzzy Search with Similarity Scores",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "keyword": "Abraham",
                                "normalizedKeyword": "abraham",
                                "isArabic": False,
                                "exactSearch": False,
                                "searchType": "fuzzy",
                                "count": 3,
                                "ayahs": [
                                    {
                                        "number": 5154,
                                        "text": "There has already been for you an excellent pattern in Abraham and those with him, when they said to their people, \"Indeed, we are disassociated from you and from whatever you worship other than Allah. We have denied you, and there has appeared between us and you animosity and hatred forever until you believe in Allah alone\" except for the saying of Abraham to his father, \"I will surely ask forgiveness for you, but I have not [power to do] for you anything against Allah. Our Lord, upon You we have relied, and to You we have returned, and to You is the destination.",
                                        "surah": {
                                            "number": 60,
                                            "name": "سورة الممتحنة",
                                            "englishName": "Al-Mumtahana",
                                            "englishNameTranslation": "She that is to be examined",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 13
                                        },
                                        "numberInSurah": 4,
                                        "juz": 28,
                                        "manzil": 7,
                                        "page": 549,
                                        "ruku": 491,
                                        "hizbQuarter": 219,
                                        "sajda": False,
                                        "similarity": {
                                            "similarity": 0.85,
                                            "wordSimilarity": 0.92,
                                            "relevanceScore": 100
                                        }
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 60,
                                        "name": "سورة الممتحنة",
                                        "englishName": "Al-Mumtahana",
                                        "englishNameTranslation": "She that is to be examined",
                                        "count": 1
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
                    "english_typo_tolerance": {
                        "summary": "English Search with Typo Handling (Ibraham → Abraham)",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "keyword": "Ibraham",
                                "normalizedKeyword": "ibraham",
                                "isArabic": False,
                                "exactSearch": False,
                                "searchType": "fuzzy",
                                "count": 1,
                                "ayahs": [
                                    {
                                        "number": 2665,
                                        "text": "And [mention, O Muhammad], when Abraham was tried by his Lord with commands and he fulfilled them. [Allah] said, \"Indeed, I will make you a leader for the people.\"",
                                        "surah": {
                                            "number": 2,
                                            "name": "سورة البقرة",
                                            "englishName": "Al-Baqarah",
                                            "englishNameTranslation": "The Cow",
                                            "revelationType": "Medinan",
                                            "numberOfAyahs": 286
                                        },
                                        "numberInSurah": 124,
                                        "juz": 2,
                                        "manzil": 1,
                                        "page": 20,
                                        "ruku": 15,
                                        "hizbQuarter": 7,
                                        "sajda": False,
                                        "similarity": {
                                            "similarity": 0.72,
                                            "wordSimilarity": 0.85,
                                            "relevanceScore": 80
                                        }
                                    }
                                ],
                                "surahs": [
                                    {
                                        "number": 2,
                                        "name": "سورة البقرة",
                                        "englishName": "Al-Baqarah",
                                        "englishNameTranslation": "The Cow",
                                        "count": 1
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
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid search parameters or no results found",
        "content": {
            "application/json": {
                "examples": {
                    "no_results": {
                        "summary": "No Search Results Found",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Nothing matching your search was found"
                        }
                    },
                    "invalid_edition": {
                        "summary": "Invalid Edition Identifier",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Something wrong happened: Edition not found"
                        }
                    },
                    "invalid_surah": {
                        "summary": "Invalid Surah Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Surah number must be between 1 and 114"
                        }
                    }
                }
            }
        }
    }
}
