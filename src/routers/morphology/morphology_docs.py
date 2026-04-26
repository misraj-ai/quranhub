# routes/morphology_docs.py
"""
Morphology API Documentation - Response examples for OpenAPI
"""

# ============================================
# 1. GET WORD MORPHOLOGY
# ============================================

getWordMorphologyResponse = {
    200: {
        "description": "Returns complete morphological breakdown for a word",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "word": {
                            "id": 1,
                            "location": "1:1:1",
                            "text": "بِسْمِ",
                            "surah": {
                                "id": 1,
                                "name": "الفاتحة",
                                "english_name": "Al-Fatihah"
                            },
                            "ayah_number": 1,
                            "position": 1,
                            "ayah_text": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
                        },
                        "morphology": {
                            "total_tags": 36,
                            "tags_by_category": {
                                "Root": [
                                    {
                                        "code": "سمو",
                                        "meaning": "سمو",
                                        "order": 2
                                    }
                                ],
                                "Sarf": [
                                    {
                                        "code": "و1",
                                        "meaning": "وزن الكلمة: فَعَلَ",
                                        "user_meaning": "وزن الكلمة: فَعَلَ",
                                        "order": 36
                                    }
                                ],
                                "Irab": [
                                    {
                                        "code": "جر",
                                        "meaning": "في محل جر",
                                        "user_meaning": "في محل جر",
                                        "order": 7
                                    }
                                ]
                            },
                            "all_tags": [
                                {
                                    "code": "ب",
                                    "meaning": "حرف الباء",
                                    "category": "Lawahiq",
                                    "order": 1
                                }
                            ]
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Word not found at specified location",
        "content": {
            "application/json": {
                "example": {
                    "code": 404,
                    "status": "Error",
                    "data": "Word not found at location 1:1:999"
                }
            }
        }
    }
}

# ============================================
# NEW: GET AYAH MORPHOLOGY
# ============================================

getAyahMorphologyResponse = {
    200: {
        "description": "Returns morphological analysis for all words in a specific ayah",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "word": {
                                "id": 1,
                                "location": "1:1:1",
                                "text": "بِسْمِ",
                                "surah": {
                                    "id": 1,
                                    "name": "الفاتحة",
                                    "english_name": "Al-Fatihah"
                                },
                                "ayah_number": 1,
                                "position": 1,
                                "ayah_text": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
                            },
                            "morphology": {
                                "total_tags": 12,
                                "tags_by_category": {
                                    "Irab": [
                                        {
                                            "code": "جر",
                                            "meaning": "في محل جر",
                                            "user_meaning": "في محل جر",
                                            "order": 7
                                        }
                                    ]
                                },
                                "all_tags": [
                                    {
                                        "code": "ب",
                                        "meaning": "حرف الباء",
                                        "category": "Lawahiq",
                                        "order": 1
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Invalid reference format",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Invalid reference format."
                }
            }
        }
    },
    404: {
        "description": "Ayah not found",
        "content": {
            "application/json": {
                "example": {
                    "code": 404,
                    "status": "Error",
                    "data": "Ayah not found."
                }
            }
        }
    }
}

# ============================================
# 2. SEARCH BY TAGS
# ============================================

searchByTagsResponse = {
    200: {
        "description": "Returns words matching specified tags",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "query": {
                            "tags": ["فع", "ضي"],
                            "match_all": True,
                            "surah_number": None,
                            "category": None
                        },
                        "results": [
                            {
                                "word_id": 150,
                                "location": "2:10:5",
                                "text": "كَذَبُوا",
                                "surah": {
                                    "id": 2,
                                    "name": "البقرة",
                                    "english_name": "Al-Baqarah"
                                },
                                "ayah_number": 10,
                                "position": 5,
                                "ayah_text": "فِي قُلُوبِهِم مَّرَضٌ",
                                "matched_tags": ["فع", "ضي"]
                            }
                        ],
                        "pagination": {
                            "total": 1543,
                            "limit": 20,
                            "offset": 0,
                            "has_more": True
                        }
                    }
                }
            }
        }
    }
}

# ============================================
# 3. SEARCH BY CATEGORY
# ============================================

searchByCategoryResponse = {
    200: {
        "description": "Returns words with tags from specified category",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "category": "Afal",
                        "tag_code": None,
                        "results": [
                            {
                                "word_id": 45,
                                "location": "1:5:2",
                                "text": "نَعْبُدُ",
                                "surah": {
                                    "id": 1,
                                    "name": "الفاتحة",
                                    "english_name": "Al-Fatihah"
                                },
                                "ayah_number": 5,
                                "position": 2,
                                "matched_tags": [
                                    {"code": "فع", "meaning": "فعل"},
                                    {"code": "ضع", "meaning": "فعل مضارع"}
                                ]
                            }
                        ],
                        "pagination": {
                            "total": 12450,
                            "limit": 20,
                            "offset": 0,
                            "has_more": True
                        }
                    }
                }
            }
        }
    }
}

# ============================================
# 4. SEARCH BY ROOT
# ============================================

searchByRootResponse = {
    200: {
        "description": "Returns all words derived from specified root",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "root": "حمد",
                        "root_info": {
                            "meaning": "حمد",
                            "total_occurrences": 63,
                            "surahs_count": 42
                        },
                        "derivatives": [
                            {
                                "word_id": 8,
                                "location": "1:2:1",
                                "text": "ٱلْحَمْدُ",
                                "surah": {
                                    "id": 1,
                                    "name": "الفاتحة",
                                    "english_name": "Al-Fatihah"
                                },
                                "ayah_number": 2,
                                "position": 1,
                                "ayah_text": "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ"
                            }
                        ],
                        "pagination": {
                            "total": 63,
                            "limit": 50,
                            "offset": 0,
                            "has_more": True
                        }
                    }
                }
            }
        }
    }
}

# ============================================
# 5. GET ALL ROOTS
# ============================================

getAllRootsResponse = {
    200: {
        "description": "Returns list of all Arabic roots with statistics",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "total_roots": 1805,
                        "roots": [
                            {
                                "root": "قول",
                                "meaning": "قول",
                                "statistics": {
                                    "word_count": 1722,
                                    "surah_count": 114
                                }
                            },
                            {
                                "root": "علم",
                                "meaning": "علم",
                                "statistics": {
                                    "word_count": 854,
                                    "surah_count": 103
                                }
                            }
                        ],
                        "pagination": {
                            "total": 1805,
                            "limit": 50,
                            "offset": 0,
                            "has_more": True
                        }
                    }
                }
            }
        }
    }
}

# ============================================
# 6. GET ALL TAGS
# ============================================

getAllTagsResponse = {
    200: {
        "description": "Returns list of all morphological tags",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "total_tags": 2468,
                        "tags": [
                            {
                                "tag_id": 1,
                                "code": "مت1",
                                "meaning": "كل الضمائر المتصلة في محل رفع",
                                "user_meaning": "اللاحق: ضمير متصل في محل رفع",
                                "category": "Irab",
                                "usage_count": 1245
                            }
                        ],
                        "categories": {
                            "Root": 1805,
                            "Sarf": 229,
                            "Irab": 195
                        },
                        "pagination": {
                            "total": 2468,
                            "limit": 100,
                            "offset": 0,
                            "has_more": True
                        }
                    }
                }
            }
        }
    }
}

# ============================================
# 7. GET TAG DETAILS
# ============================================

getTagDetailsResponse = {
    200: {
        "description": "Returns detailed information about a specific tag",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "tag": {
                            "code": "فع",
                            "meaning": "كل الأفعال",
                            "user_meaning": "فعل",
                            "category": "Afal"
                        },
                        "statistics": {
                            "total_words": 12450,
                            "surahs_count": 114,
                            "percentage_of_quran": 16.08
                        },
                        "related_tags": [
                            {
                                "code": "ضي",
                                "meaning": "فعل ماض",
                                "co_occurrence_count": 4521
                            }
                        ],
                        "examples": [
                            {
                                "word_id": 150,
                                "location": "2:10:5",
                                "text": "كَذَبُوا",
                                "ayah_text": "فِي قُلُوبِهِم مَّرَضٌ"
                            }
                        ]
                    }
                }
            }
        }
    }
}

# ============================================
# 8. GET MORPHOLOGY STATS
# ============================================

getMorphologyStatsResponse = {
    200: {
        "description": "Returns overall morphological statistics",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "scope": {
                            "surah_number": None,
                            "category": None
                        },
                        "overview": {
                            "total_words": 77433,
                            "words_with_morphology": 77432,
                            "coverage": 99.99,
                            "total_tags": 2468,
                            "total_associations": 2519202,
                            "avg_tags_per_word": 32.53
                        },
                        "by_category": {
                            "Root": {
                                "unique_tags": 1805,
                                "total_occurrences": 77432,
                                "avg_per_word": 1.0
                            }
                        },
                        "top_roots": [
                            {
                                "root": "قول",
                                "word_count": 1722,
                                "percentage": 2.22
                            }
                        ],
                        "top_tags": []
                    }
                }
            }
        }
    }
}

# ============================================
# 9. GET SURAH PROFILE
# ============================================

getSurahProfileResponse = {
    200: {
        "description": "Returns morphological profile for a surah",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "surah": {
                            "id": 1,
                            "name": "الفاتحة",
                            "english_name": "Al-Fatihah",
                            "total_words": 29,
                            "total_ayahs": 7
                        },
                        "morphology": {
                            "unique_roots": 22,
                            "most_common_root": {
                                "root": "حمد",
                                "occurrences": 1
                            },
                            "verb_tenses": {
                                "ماضي": 2,
                                "مضارع": 4
                            }
                        },
                        "complexity_score": 65.5
                    }
                }
            }
        }
    }
}

# ============================================
# 10. SEARCH BY PATTERN
# ============================================

searchByPatternResponse = {
    200: {
        "description": "Returns words matching morphological pattern",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "pattern": "فَعَلَ",
                        "pattern_info": {
                            "tag_code": "و1",
                            "category": "Sarf",
                            "total_occurrences": 2345
                        },
                        "words": [
                            {
                                "word_id": 120,
                                "location": "2:8:4",
                                "text": "كَذَبَ",
                                "root": "كذب",
                                "surah": {
                                    "id": 2,
                                    "name": "البقرة"
                                },
                                "ayah_number": 8
                            }
                        ],
                        "pagination": {
                            "total": 2345,
                            "limit": 50,
                            "offset": 0,
                            "has_more": True
                        }
                    }
                }
            }
        }
    }
}

# ============================================
# 11. COMPARE WORDS
# ============================================

compareWordsResponse = {
    200: {
        "description": "Returns morphological comparison of multiple words",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "words": [
                            {
                                "location": "1:1:1",
                                "text": "بِسْمِ",
                                "tags_count": 36,
                                "categories": ["Root", "Sarf", "Irab"]
                            }
                        ],
                        "comparison": {
                            "common_tags": [
                                {
                                    "code": "أص",
                                    "meaning": "أصلية",
                                    "category": "Root"
                                }
                            ],
                            "unique_to_each": {
                                "1:1:1": ["ب", "سمو"],
                                "1:2:1": ["حمد", "ال1"]
                            },
                            "similarity_score": 45.2
                        }
                    }
                }
            }
        }
    }
}

# ============================================
# GET ALL CATEGORIES
# ============================================

getAllCategoriesResponse = {
    200: {
        "description": "Returns list of all morphological categories with Arabic and English names",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "total_categories": 11,
                        "categories": [
                            {
                                "code": "Root",
                                "arabic_name": "الجذور",
                                "english_name": "Roots",
                                "description": "Arabic root letters",
                                "tag_count": 1805
                            },
                            {
                                "code": "Sarf",
                                "arabic_name": "الصرف",
                                "english_name": "Morphology",
                                "description": "Morphological patterns and forms",
                                "tag_count": 229
                            },
                            {
                                "code": "Irab",
                                "arabic_name": "الإعراب",
                                "english_name": "Grammar",
                                "description": "Grammatical case markers",
                                "tag_count": 195
                            },
                            {
                                "code": "Afal",
                                "arabic_name": "الأفعال",
                                "english_name": "Verbs",
                                "description": "Verb forms and tenses",
                                "tag_count": 15
                            },
                            {
                                "code": "Lawahiq",
                                "arabic_name": "اللواحق",
                                "english_name": "Suffixes",
                                "description": "Attached suffixes",
                                "tag_count": 47
                            },
                            {
                                "code": "Horof",
                                "arabic_name": "الحروف",
                                "english_name": "Particles",
                                "description": "Particles and prepositions",
                                "tag_count": 43
                            },
                            {
                                "code": "Tajwid",
                                "arabic_name": "التجويد",
                                "english_name": "Tajweed",
                                "description": "Quranic recitation rules",
                                "tag_count": 39
                            },
                            {
                                "code": "Asma",
                                "arabic_name": "الأسماء",
                                "english_name": "Nouns",
                                "description": "Noun forms",
                                "tag_count": 37
                            },
                            {
                                "code": "Aam",
                                "arabic_name": "عام",
                                "english_name": "General",
                                "description": "General markers",
                                "tag_count": 24
                            },
                            {
                                "code": "Sawabiq",
                                "arabic_name": "السوابق",
                                "english_name": "Prefixes",
                                "description": "Attached prefixes",
                                "tag_count": 22
                            },
                            {
                                "code": "Monawaeat",
                                "arabic_name": "المنوعات",
                                "english_name": "Miscellaneous",
                                "description": "Various markers",
                                "tag_count": 12
                            }
                        ]
                    }
                }
            }
        }
    }
}