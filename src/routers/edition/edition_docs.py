# Enhanced Edition API Documentation
# Updated response examples based on current API structure and database samples

getTheEditionResponse = {
    200: {
        "description": "Successful Response - Comprehensive list of all available Quranic editions including text editions (Quran, translations, tafsir, narrations), audio recitations, and specialized formats",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "identifier": "quran-simple",
                            "language": "ar",
                            "name": "Simple",
                            "englishName": "Simple", 
                            "format": "text",
                            "type": "quran",
                            "direction": "rtl",
                            "narratorIdentifier": None
                        },
                        {
                            "identifier": "ar.abdullahbasfar.hafs",
                            "language": "ar",
                            "name": "عبد الله بصفر",
                            "englishName": "Abdullah Basfar",
                            "format": "audio",
                            "type": "versebyverse",
                            "direction": "rtl",
                            "narratorIdentifier": "quran-hafs",
                            "description": {
                                "ar": "عبد الله بصفر: قارئ سعودي بارز وأستاذ مشارك في جامعة الملك عبد العزيز بجدة. الأمين العام السابق للهيئة العالمية للكتاب والسنة، معروف بصوته العذب وإسهاماته العلمية.",
                                "en": "Abdullah Basfar: Prominent Saudi reciter and associate professor at King Abdulaziz University in Jeddah. Former Secretary-General of the World Book and Sunnah Organization, known for his melodious voice and scholarly contributions."
                            },
                            "imageUrl": "https://quranhub.b-cdn.net/quran/images/reciters/abdullah-basfar.jpeg"
                        },
                        {
                            "identifier": "en.sahih",
                            "language": "en",
                            "name": "Saheeh International",
                            "englishName": "Saheeh International",
                            "format": "text",
                            "type": "translation",
                            "direction": "ltr",
                            "narratorIdentifier": None
                        },
                        {
                            "identifier": "ar.mukhtasar",
                            "language": "ar",
                            "name": "المختصر في التفسير",
                            "englishName": "Al-Mukhtasar",
                            "format": "text",
                            "type": "tafsir",
                            "direction": "rtl",
                            "narratorIdentifier": None,
                            "description": {
                                "ar": "المختصر في التفسير: تفسير مختصر وشامل للقرآن الكريم، يقدم فهماً واضحاً وميسراً لمعاني الآيات بأسلوب معاصر.",
                                "en": "Al-Mukhtasar: A comprehensive and concise interpretation of the Holy Quran, providing clear and accessible understanding of verse meanings in contemporary style."
                            },
                            "imageUrl": "https://quranhub.b-cdn.net/quran/images/tafsirs/al-mukhtasar.jpg"
                        },
                        {
                            "identifier": "quran-hafs",
                            "language": "ar",
                            "name": "حفص عن عاصم",
                            "englishName": "Hafs from 'Aasem",
                            "format": "text",
                            "type": "narration",
                            "direction": "rtl",
                            "narratorIdentifier": None
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching editions",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Edition not found"
                }
            }
        }
    }
}

getTheEditionLanguagesResponse = {
    200: {
        "description": "Successful Response - List of all available languages for Quranic editions using ISO 639-1 language codes",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        "ar", "en", "fr", "es", "de", "it", "ru", "tr", "id", "ms", 
                        "ur", "hi", "bn", "fa", "zh", "ja", "ko", "th", "vi", "tl",
                        "sw", "ha", "pt", "nl", "sv", "no", "da", "fi", "pl", "cs",
                        "sk", "hu", "ro", "bg", "hr", "sr", "bs", "sq", "mk", "sl",
                        "et", "lv", "lt", "mt", "ga", "cy", "eu", "ca", "gl", "ast",
                        "oc", "co", "rm", "lad", "an", "mwl", "ext", "lij", "vec",
                        "pms", "lmo", "eml", "rgn", "nap", "scn", "srd", "fur"
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching available languages",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Languages not found"
                }
            }
        }
    }
}

getTheEditionByLanguageResponse = {
    200: {
        "description": "Successful Response - All editions available in the specified language, including original Arabic texts, translations, audio recitations, and tafsir commentaries",
        "content": {
            "application/json": {
                "examples": {
                    "arabic_editions": {
                        "summary": "Arabic Language Editions",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {
                                    "identifier": "quran-simple",
                                    "language": "ar",
                                    "name": "Simple",
                                    "englishName": "Simple",
                                    "format": "text",
                                    "type": "quran",
                                    "direction": "rtl",
                                    "narratorIdentifier": None
                                },
                                {
                                    "identifier": "ar.shaatree.hafs",
                                    "language": "ar",
                                    "name": "أبو بكر الشاطري",
                                    "englishName": "Abu Bakr Ash-Shaatree",
                                    "format": "audio",
                                    "type": "versebyverse",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/shaatree.jpg",
                                    "shortDescription": {"ar": "قارئ مشهور من السعودية"}
                                },
                                {
                                    "identifier": "ar.mukhtasar",
                                    "language": "ar",
                                    "name": "المختصر في التفسير",
                                    "englishName": "Al-Mukhtasar",
                                    "format": "text",
                                    "type": "tafsir",
                                    "direction": "rtl",
                                    "narratorIdentifier": None
                                }
                            ]
                        }
                    },
                    "english_editions": {
                        "summary": "English Language Editions",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {
                                    "identifier": "en.sahih",
                                    "language": "en",
                                    "name": "Saheeh International",
                                    "englishName": "Saheeh International",
                                    "format": "text",
                                    "type": "translation",
                                    "direction": "ltr",
                                    "narratorIdentifier": None
                                },
                                {
                                    "identifier": "en.maududi",
                                    "language": "en",
                                    "name": "Maududi",
                                    "englishName": "Abul Ala Maududi",
                                    "format": "text",
                                    "type": "translation",
                                    "direction": "ltr",
                                    "narratorIdentifier": None
                                }
                            ]
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid language code or no editions found",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: No editions found for this language"
                }
            }
        }
    }
}

getTheEditionTypesResponse = {
    200: {
        "description": "Successful Response - List of all available edition types categorized by content format and purpose",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        "quran",
                        "translation", 
                        "tafsir",
                        "narration",
                        "transliteration",
                        "versebyverse",
                        "surah"
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching edition types",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Types not found"
                }
            }
        }
    }
}

getTheEditionByTypeResponse = {
    200: {
        "description": "Successful Response - All editions of the specified type with comprehensive metadata",
        "content": {
            "application/json": {
                "examples": {
                    "tafsir_editions": {
                        "summary": "Tafsir (Commentary) Editions",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {
                                    "identifier": "ar.mukhtasar",
                                    "language": "ar",
                                    "name": "المختصر في التفسير",
                                    "englishName": "Al-Mukhtasar",
                                    "format": "text",
                                    "type": "tafsir",
                                    "direction": "rtl",
                                    "narratorIdentifier": None
                                },
                                {
                                    "identifier": "ur.mukhtasar",
                                    "language": "ur",
                                    "name": "المختصر",
                                    "englishName": "Al-Mukhtasar",
                                    "format": "text",
                                    "type": "tafsir",
                                    "direction": "rtl",
                                    "narratorIdentifier": None
                                }
                            ]
                        }
                    },
                    "audio_editions": {
                        "summary": "Audio Recitation Editions",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {
                                    "identifier": "ar.shaatree.hafs",
                                    "language": "ar",
                                    "name": "أبو بكر الشاطري",
                                    "englishName": "Abu Bakr Ash-Shaatree",
                                    "format": "audio",
                                    "type": "versebyverse",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/shaatree.jpg",
                                    "shortDescription": {"ar": "قارئ مشهور من السعودية"}
                                },
                                {
                                    "identifier": "ar.ahmedajamy.hafs",
                                    "language": "ar",
                                    "name": "أحمد بن علي العجمي",
                                    "englishName": "Ahmed ibn Ali al-Ajamy",
                                    "format": "audio",
                                    "type": "surah",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/ajamy.jpg",
                                    "shortDescription": {"ar": "إمام وخطيب الحرم المكي"}
                                }
                            ]
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid edition type or no editions found",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: No editions found for this type"
                }
            }
        }
    }
}

getTheEditionFormatsResponse = {
    200: {
        "description": "Successful Response - Available edition formats distinguishing between textual and audio content",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK", 
                    "data": [
                        "text",
                        "audio"
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching available formats",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Formats not found"
                }
            }
        }
    }
}

getTheEditionByFormatResponse = {
    200: {
        "description": "Successful Response - All editions in the specified format with detailed metadata and reciter information for audio editions",
        "content": {
            "application/json": {
                "examples": {
                    "audio_format": {
                        "summary": "Audio Format Editions",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {
                                    "identifier": "ar.shaatree.hafs",
                                    "language": "ar",
                                    "name": "أبو بكر الشاطري",
                                    "englishName": "Abu Bakr Ash-Shaatree",
                                    "format": "audio",
                                    "type": "versebyverse",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/shaatree.jpg",
                                    "shortDescription": {"ar": "قارئ مشهور من السعودية"}
                                },
                                {
                                    "identifier": "ar.ahmedajamy.hafs",
                                    "language": "ar",
                                    "name": "أحمد بن علي العجمي",
                                    "englishName": "Ahmed ibn Ali al-Ajamy",
                                    "format": "audio",
                                    "type": "surah",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/ajamy.jpg",
                                    "shortDescription": {"ar": "إمام وخطيب الحرم المكي"}
                                }
                            ]
                        }
                    },
                    "text_format": {
                        "summary": "Text Format Editions",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {
                                    "identifier": "quran-simple",
                                    "language": "ar",
                                    "name": "Simple",
                                    "englishName": "Simple",
                                    "format": "text",
                                    "type": "quran",
                                    "direction": "rtl",
                                    "narratorIdentifier": None
                                },
                                {
                                    "identifier": "en.sahih",
                                    "language": "en",
                                    "name": "Saheeh International",
                                    "englishName": "Saheeh International",
                                    "format": "text",
                                    "type": "translation",
                                    "direction": "ltr",
                                    "narratorIdentifier": None
                                }
                            ]
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid format specified or no editions found",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: No editions found for this format"
                }
            }
        }
    }
}

getTheEditionByFormatAndTypeResponse = {
    200: {
        "description": "Successful Response - Editions filtered by both format and type for precise content targeting",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "identifier": "quran-simple",
                            "language": "ar",
                            "name": "Simple",
                            "englishName": "Simple", 
                            "format": "text",
                            "type": "quran",
                            "direction": "rtl",
                            "narratorIdentifier": None
                        },
                        {
                            "identifier": "quran-hafs",
                            "language": "ar",
                            "name": "حفص عن عاصم",
                            "englishName": "Hafs from 'Aasem",
                            "format": "text",
                            "type": "narration",
                            "direction": "rtl",
                            "narratorIdentifier": None
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid format/type combination or no editions found",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: No editions found for this format and type combination"
                }
            }
        }
    }
}

getTheEditionNarratorIdentifiersResponse = {
    200: {
        "description": "Successful Response - List of all narrator identifiers used for different Quranic recitation styles and reading traditions",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        "quran-hafs",
                        "quran-warsh", 
                        "quran-qaloon",
                        "quran-qunbul",
                        "quran-albazzi",
                        "quran-aldouri",
                        "quran-alsoosi",
                        "quran-shoba"
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching narrator identifiers",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Narrator identifiers not found"
                }
            }
        }
    }
}

getTheAudioEditionByNarratorIdentifierResponse = {
    200: {
        "description": "Successful Response - Audio editions available for the specified narrator with reciter information and quality options",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "identifier": "ar.shaatree.warsh",
                            "language": "ar",
                            "name": "أبو بكر الشاطري",
                            "englishName": "Abu Bakr Ash-Shaatree",
                            "format": "audio",
                            "type": "versebyverse",
                            "direction": "rtl",
                            "narratorIdentifier": "quran-warsh",
                            "imageUrl": "https://example.com/reciters/shaatree.jpg",
                            "shortDescription": {"ar": "قارئ مشهور من السعودية برواية ورش"}
                        },
                        {
                            "identifier": "ar.warsh.premium",
                            "language": "ar",
                            "name": "قراءة ورش عالية الجودة",
                            "englishName": "Warsh Premium Quality",
                            "format": "audio",
                            "type": "versebyverse",
                            "direction": "rtl",
                            "narratorIdentifier": "quran-warsh",
                            "imageUrl": "https://example.com/reciters/warsh.jpg",
                            "shortDescription": {"ar": "تسجيل عالي الجودة برواية ورش عن نافع"}
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid narrator identifier or no audio editions found",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: No audio editions found for this narrator"
                }
            }
        }
    }
}
"""
Response documentation for the Editions Analysis endpoint.
Contains the comprehensive analysis response schema.
"""

getEditionsAnalysisResponse = {
    200: {
        "description": "Clean and organized analysis of all editions in the database with logical groupings and meaningful statistics",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "overview": {
                            "totalEditions": 330,
                            "textEditions": 230,
                            "audioEditions": 100,
                            "totalAudioFiles": 625140
                        },
                        "formats": {
                            "text": 230,
                            "audio": 100
                        },
                        "types": {
                            "tafsir": 85,
                            "translation": 65,
                            "surah": 55,
                            "versebyverse": 45,
                            "quran": 35,
                            "narration": 25,
                            "transliteration": 15,
                            "tajweed": 5
                        },
                        "languages": {
                            "ar": {
                                "total": 180,
                                "textEditions": 120,
                                "audioEditions": 60,
                                "textTypes": {
                                    "tafsir": 85,
                                    "quran": 25,
                                    "narration": 10
                                },
                                "audioTypes": {
                                    "versebyverse": 35,
                                    "surah": 25
                                }
                            },
                            "en": {
                                "total": 65,
                                "textEditions": 60,
                                "audioEditions": 5,
                                "textTypes": {
                                    "translation": 55,
                                    "transliteration": 5
                                },
                                "audioTypes": {
                                    "surah": 3,
                                    "versebyverse": 2
                                }
                            },
                            "fr": {
                                "total": 25,
                                "textEditions": 22,
                                "audioEditions": 3,
                                "textTypes": {
                                    "translation": 20,
                                    "tafsir": 2
                                },
                                "audioTypes": {
                                    "surah": 2,
                                    "versebyverse": 1
                                }
                            }
                        },
                        "narrations": {
                            "quran-hafs": {
                                "totalEditions": 65,
                                "textEditions": 1,
                                "audioEditions": 64
                            },
                            "quran-warsh": {
                                "totalEditions": 35,
                                "textEditions": 1,
                                "audioEditions": 34
                            },
                            "quran-qaloon": {
                                "totalEditions": 25,
                                "textEditions": 1,
                                "audioEditions": 24
                            },
                            "quran-shoba": {
                                "totalEditions": 15,
                                "textEditions": 1,
                                "audioEditions": 14
                            }
                        },
                        "reciters": {
                            "totalUniqueReciters": 42
                        },
                        "audioAnalysis": {
                            "byLanguage": {
                                "ar": {
                                    "editionCount": 85,
                                    "types": {
                                        "versebyverse": 45,
                                        "surah": 40
                                    },
                                    "uniqueNarrationsCount": 8
                                },
                                "en": {
                                    "editionCount": 8,
                                    "types": {
                                        "surah": 5,
                                        "versebyverse": 3
                                    },
                                    "uniqueNarrationsCount": 2
                                }
                            },
                            "byNarration": {
                                "quran-hafs": {
                                    "editionCount": 50,
                                    "languageCount": 5,
                                    "types": {
                                        "versebyverse": 30,
                                        "surah": 20
                                    }
                                },
                                "quran-warsh": {
                                    "editionCount": 25,
                                    "languageCount": 2,
                                    "types": {
                                        "versebyverse": 15,
                                        "surah": 10
                                    }
                                }
                            },
                            "bitrates": {
                                "uniqueBitrates": 6,
                                "availableBitrates": [32, 64, 96, 128, 192, 320],
                                "statistics": {
                                    "average": 108.5,
                                    "minimum": 32,
                                    "maximum": 320
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while analyzing editions",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something went wrong: An error occurred while performing editions analysis"
                }
            }
        }
    }
}
