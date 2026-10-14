# --- New endpoint: /tafsir/{editionIdentifier} ---
getTafsirEditionByIdentifierResponse = {
    200: {
        "description": "Successful Response - Single tafsir edition metadata, matching the canonical tafsir edition response shape.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "identifier": "ar.mukhtasar",
                        "language": "ar",
                        "name": "المختصر في التفسير",
                        "englishName": "Al-Mukhtasar",
                        "format": "text",
                        "type": "tafsir",
                            "subtype": "tafsir",
                        "direction": "rtl",
                        "narratorIdentifier": None,
                        "imageUrl": "https://quranhub.b-cdn.net/quran/images/tafsirs/al-mukhtasar.jpg"
                    }
                }
            }
        }
    },
    404: {
        "description": "Not Found - Edition identifier does not exist or is not a tafsir edition",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Edition not found",
                        "value": {
                            "code": 404,
                            "status": "Not Found",
                            "data": "Edition not found"
                        }
                    },
                    "not_tafsir": {
                        "summary": "Edition is not tafsir",
                        "value": {
                            "code": 404,
                            "status": "Not Found",
                            "data": "Edition is not tafsir"
                        }
                    }
                }
            }
        }
    }
}
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
                            "subtype": "mushaf",
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
                            "subtype": "recitation",
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
                            "subtype": "translation",
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
                            "subtype": "tafsir",
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
                            "subtype": "narration",
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
                            "subtype": "mushaf",
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
                            "subtype": "recitation",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/shaatree.jpg",
                                    "shortDescription": {"ar": "قارئ مشهور من السعودية"},
                                    "nationality": {"code": "SA", "en": "Saudi Arabia", "ar": "السعودية"}
                                },
                                {
                                    "identifier": "ar.mukhtasar",
                                    "language": "ar",
                                    "name": "المختصر في التفسير",
                                    "englishName": "Al-Mukhtasar",
                                    "format": "text",
                                    "type": "tafsir",
                            "subtype": "tafsir",
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
                            "subtype": "translation",
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
                            "subtype": "translation",
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
                            "subtype": "tafsir",
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
                            "subtype": "tafsir",
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
                            "subtype": "recitation",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/shaatree.jpg",
                                    "shortDescription": {"ar": "قارئ مشهور من السعودية"},
                                    "nationality": {"code": "SA", "en": "Saudi Arabia", "ar": "السعودية"}
                                },
                                {
                                    "identifier": "ar.ahmedajamy.hafs",
                                    "language": "ar",
                                    "name": "أحمد بن علي العجمي",
                                    "englishName": "Ahmed ibn Ali al-Ajamy",
                                    "format": "audio",
                                    "type": "surah",
                            "subtype": "recitation",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/ajamy.jpg",
                                    "shortDescription": {"ar": "إمام وخطيب الحرم المكي"},
                                    "nationality": {"code": "SA", "en": "Saudi Arabia", "ar": "السعودية"}
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

getTheEditionByTypeAndLanguageResponse = {
    200: {
        "description": "Successful Response - All editions matching the specified type and language combination",
        "content": {
            "application/json": {
                "examples": {
                    "arabic_translations": {
                        "summary": "Arabic Translation Editions",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": [
                                {
                                    "identifier": "ar.muyassar",
                                    "language": "ar",
                                    "name": "تفسير المیسر",
                                    "englishName": "Al-Muyassar",
                                    "format": "text",
                                    "type": "translation",
                            "subtype": "translation",
                                    "direction": "rtl",
                                    "narratorIdentifier": None
                                }
                            ]
                        }
                    },
                    "english_translations": {
                        "summary": "English Translation Editions",
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
                            "subtype": "translation",
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
                            "subtype": "translation",
                                    "direction": "ltr",
                                    "narratorIdentifier": None
                                }
                            ]
                        }
                    },
                    "arabic_tafsir": {
                        "summary": "Arabic Tafsir Editions",
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
                            "subtype": "tafsir",
                                    "direction": "rtl",
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
        "description": "Bad Request - Invalid type/language combination or no editions found",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: No editions found for this type and language combination"
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
                            "subtype": "recitation",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/shaatree.jpg",
                                    "shortDescription": {"ar": "قارئ مشهور من السعودية"},
                                    "nationality": {"code": "SA", "en": "Saudi Arabia", "ar": "السعودية"}
                                },
                                {
                                    "identifier": "ar.ahmedajamy.hafs",
                                    "language": "ar",
                                    "name": "أحمد بن علي العجمي",
                                    "englishName": "Ahmed ibn Ali al-Ajamy",
                                    "format": "audio",
                                    "type": "surah",
                            "subtype": "recitation",
                                    "direction": "rtl",
                                    "narratorIdentifier": "quran-hafs",
                                    "imageUrl": "https://example.com/reciters/ajamy.jpg",
                                    "shortDescription": {"ar": "إمام وخطيب الحرم المكي"},
                                    "nationality": {"code": "SA", "en": "Saudi Arabia", "ar": "السعودية"}
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
                            "subtype": "mushaf",
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
                            "subtype": "translation",
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
                            "subtype": "mushaf",
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
                            "subtype": "narration",
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
                            "subtype": "recitation",
                            "direction": "rtl",
                            "narratorIdentifier": "quran-warsh",
                            "imageUrl": "https://example.com/reciters/shaatree.jpg",
                            "shortDescription": {"ar": "قارئ مشهور من السعودية برواية ورش"},
                            "nationality": {"code": "SA", "en": "Saudi Arabia", "ar": "السعودية"},
                            "recitationType": "murattal",
                            "types": [
                                {"type": "versebyverse", "bitrates": [128, 64]},
                                {"type": "surah", "bitrates": [128]}
                            ]
                        },
                        {
                            "identifier": "ar.alkouchi.warsh",
                            "language": "ar",
                            "name": "العيون الكوشي",
                            "englishName": "Al-Ayoune Al-Kouchi",
                            "format": "audio",
                            "type": "surah",
                            "subtype": "recitation",
                            "direction": None,
                            "narratorIdentifier": "quran-warsh",
                            "imageUrl": "https://quranhub.b-cdn.net/quran/images/reciters/al-ayoune-al-kouchi.jpeg",
                            "shortDescription": {"ar": "قارئ مغربي بارز متخصص في رواية ورش عن نافع"},
                            "nationality": {"code": "MA", "en": "Morocco", "ar": "المغرب"},
                            "recitationType": "murattal",
                            "types": [
                                {"type": "surah", "bitrates": [64]}
                            ]
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

# --- New endpoint: /audio/{editionIdentifier} ---
getDistinctAudioEditionByIdentifierResponse = {
    200: {
        "description": "Successful Response - Single audio edition with reciter and narration details, matching the canonical audio edition response shape.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "identifier": "ar.abdullahbasfar.hafs",
                        "language": "ar",
                        "name": "عبد الله بصفر",
                        "englishName": "Abdullah Basfar",
                        "format": "audio",
                        "type": "versebyverse",
                            "subtype": "recitation",
                        "direction": "rtl",
                        "narratorIdentifier": "quran-hafs",
                        "description": {
                            "ar": "عبد الله بصفر: قارئ سعودي بارز وأستاذ مشارك في جامعة الملك عبد العزيز بجدة. الأمين العام السابق للهيئة العالمية للكتاب والسنة، معروف بصوته العذب وإسهاماته العلمية.",
                            "en": "Abdullah Basfar: Prominent Saudi reciter and associate professor at King Abdulaziz University in Jeddah. Former Secretary-General of the World Book and Sunnah Organization, known for his melodious voice and scholarly contributions."
                        },
                        "imageUrl": "https://quranhub.b-cdn.net/quran/images/reciters/abdullah-basfar.jpeg"
                    }
                }
            }
        }
    },
    404: {
        "description": "Not Found - Edition identifier does not exist or is not an audio edition",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Edition not found",
                        "value": {
                            "code": 404,
                            "status": "Not Found",
                            "data": "Edition not found"
                        }
                    },
                    "not_audio": {
                        "summary": "Edition is not audio",
                        "value": {
                            "code": 404,
                            "status": "Not Found",
                            "data": "Edition is not audio"
                        }
                    }
                }
            }
        }
    }
}
getTheAudioNationalitiesResponse = {
    200: {
        "description": "Successful Response - Nationalities of the reciters that have audio editions, with the number of reciters and audio editions for each",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "code": "SA",
                            "en": "Saudi Arabia",
                            "ar": "السعودية",
                            "reciters": 65,
                            "editions": 65
                        },
                        {
                            "code": "EG",
                            "en": "Egypt",
                            "ar": "مصر",
                            "reciters": 26,
                            "editions": 36
                        },
                        {
                            "code": "KW",
                            "en": "Kuwait",
                            "ar": "الكويت",
                            "reciters": 6,
                            "editions": 6
                        },
                        {
                            "code": "YE",
                            "en": "Yemen",
                            "ar": "اليمن",
                            "reciters": 6,
                            "editions": 6
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching nationalities",
        "content": {
            "application/json": {
                "example": {"code": 400, "status": "Error", "data": "Something went wrong: A database error occurred while fetching nationalities."}
            }
        }
    }
}

getTheAudioEditionsByNationalityResponse = {
    200: {
        "description": "Successful Response - Audio editions of the reciters with the given nationality, one entry per edition identifier (`types` lists the available layouts and bitrates)",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "identifier": "ar.alafasy.hafs",
                            "language": "ar",
                            "name": "مشاري راشد العفاسي",
                            "englishName": "Mishary Rashid Alafasy",
                            "imageUrl": "https://quranhub.b-cdn.net/quran/images/reciters/alafasy.jpeg",
                            "shortDescription": {
                                "ar": "قارئ كويتي وإمام مسجد الكبير",
                                "en": "Kuwaiti reciter and Imam of the Grand Mosque in Kuwait"
                            },
                            "nationality": {
                                "code": "KW",
                                "en": "Kuwait",
                                "ar": "الكويت"
                            },
                            "format": "audio",
                            "type": "versebyverse",
                            "direction": "rtl",
                            "narratorIdentifier": "quran-hafs",
                            "recitationType": "murattal",
                            "types": [
                                {
                                    "type": "versebyverse",
                                    "bitrates": [
                                        128,
                                        64
                                    ]
                                },
                                {
                                    "type": "surah",
                                    "bitrates": [
                                        128
                                    ]
                                }
                            ]
                        },
                        {
                            "identifier": "ar.alkandari.hafs",
                            "language": "ar",
                            "name": "عبدالله الكندري",
                            "englishName": "Abdullah Al-Kandari",
                            "imageUrl": "https://quranhub.b-cdn.net/quran/images/reciters/abdullah-al-kandari.jpeg",
                            "shortDescription": {
                                "ar": "قارئ كويتي",
                                "en": "Kuwaiti reciter"
                            },
                            "nationality": {
                                "code": "KW",
                                "en": "Kuwait",
                                "ar": "الكويت"
                            },
                            "format": "audio",
                            "type": "surah",
                            "direction": None,
                            "narratorIdentifier": "quran-hafs",
                            "recitationType": "murattal",
                            "types": [
                                {
                                    "type": "surah",
                                    "bitrates": [
                                        256
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid country code or an error occurred while fetching the editions",
        "content": {
            "application/json": {
                "example": {"code": 400, "status": "Error", "data": "countryCode must be a two-letter ISO 3166-1 alpha-2 code (e.g. SA, EG, KW)"}
            }
        }
    },
    404: {
        "description": "Not Found - No audio edition matches this nationality",
        "content": {
            "application/json": {
                "example": {"code": 404, "status": "Error", "data": "No audio editions found for nationality 'XX'"}
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
                            "totalEditions": 551,
                            "textEditions": 343,
                            "audioEditions": 208,
                            "totalAudioFiles": 522762
                        },
                        "formats": {
                            "text": 343,
                            "audio": 208
                        },
                        "types": {
                            "tafsir": 157,
                            "surah": 164,
                            "quran": 12,
                            "translation": 164,
                            "versebyverse": 43,
                            "wordbyword": 1,
                            "narration": 8,
                            "transliteration": 2
                        },
                        "languages": {
                            "ar": {
                                "total": 272,
                                "textEditions": 74,
                                "audioEditions": 198,
                                "textTypes": {
                                    "tafsir": 53,
                                    "quran": 12,
                                    "translation": 1,
                                    "narration": 8
                                },
                                "audioTypes": {
                                    "surah": 159,
                                    "versebyverse": 38,
                                    "wordbyword": 1
                                }
                            },
                            "en": {
                                "total": 33,
                                "textEditions": 31,
                                "audioEditions": 2,
                                "textTypes": {
                                    "tafsir": 15,
                                    "translation": 15,
                                    "transliteration": 1
                                },
                                "audioTypes": {
                                    "surah": 1,
                                    "versebyverse": 1
                                }
                            },
                            "fr": {
                                "total": 4,
                                "textEditions": 2,
                                "audioEditions": 2,
                                "textTypes": {
                                    "tafsir": 1,
                                    "translation": 1
                                },
                                "audioTypes": {
                                    "surah": 1,
                                    "versebyverse": 1
                                }
                            }
                        },
                        "narrations": {
                            "quran-hafs": {
                                "totalEditions": 162,
                                "textEditions": 1,
                                "audioEditions": 162
                            },
                            "quran-warsh": {
                                "totalEditions": 17,
                                "textEditions": 1,
                                "audioEditions": 17
                            },
                            "quran-qaloon": {
                                "totalEditions": 12,
                                "textEditions": 1,
                                "audioEditions": 12
                            },
                            "quran-aldouri": {
                                "totalEditions": 6,
                                "textEditions": 1,
                                "audioEditions": 6
                            },
                            "quran-albazzi": {
                                "totalEditions": 3,
                                "textEditions": 1,
                                "audioEditions": 3
                            },
                            "quran-shoba": {
                                "totalEditions": 4,
                                "textEditions": 1,
                                "audioEditions": 4
                            },
                            "quran-alsoosi": {
                                "totalEditions": 2,
                                "textEditions": 1,
                                "audioEditions": 2
                            },
                            "quran-qunbul": {
                                "totalEditions": 2,
                                "textEditions": 1,
                                "audioEditions": 2
                            }
                        },
                        "reciters": {
                            "totalUniqueReciters": 151,
                            "byNationality": {
                                "SA": 65,
                                "EG": 26,
                                "KW": 6,
                                "LY": 6,
                                "YE": 6,
                                "MA": 5,
                                "SY": 5,
                                "IQ": 4,
                                "SD": 4,
                                "BH": 3,
                                "AE": 2,
                                "DZ": 2,
                                "IR": 2,
                                "JO": 2,
                                "PK": 2,
                                "PS": 2,
                                "QA": 2,
                                "GH": 1,
                                "IN": 1,
                                "TN": 1
                            }
                        },
                        "audioAnalysis": {
                            "byLanguage": {
                                "ar": {
                                    "editionCount": 198,
                                    "types": {
                                        "surah": 159,
                                        "versebyverse": 38,
                                        "wordbyword": 1
                                    },
                                    "uniqueNarrationsCount": 8
                                },
                                "en": {
                                    "editionCount": 2,
                                    "types": {
                                        "surah": 1,
                                        "versebyverse": 1
                                    },
                                    "uniqueNarrationsCount": 1
                                },
                                "fa": {
                                    "editionCount": 2,
                                    "types": {
                                        "surah": 1,
                                        "versebyverse": 1
                                    },
                                    "uniqueNarrationsCount": 1
                                },
                                "ur": {
                                    "editionCount": 2,
                                    "types": {
                                        "surah": 1,
                                        "versebyverse": 1
                                    },
                                    "uniqueNarrationsCount": 1
                                },
                                "zh": {
                                    "editionCount": 2,
                                    "types": {
                                        "surah": 1,
                                        "versebyverse": 1
                                    },
                                    "uniqueNarrationsCount": 1
                                },
                                "fr": {
                                    "editionCount": 2,
                                    "types": {
                                        "surah": 1,
                                        "versebyverse": 1
                                    },
                                    "uniqueNarrationsCount": 1
                                }
                            },
                            "byNarration": {
                                "quran-hafs": {
                                    "editionCount": 162,
                                    "types": {
                                        "surah": 136,
                                        "versebyverse": 25,
                                        "wordbyword": 1
                                    },
                                    "languageCount": 6
                                },
                                "quran-warsh": {
                                    "editionCount": 17,
                                    "types": {
                                        "surah": 10,
                                        "versebyverse": 7
                                    },
                                    "languageCount": 1
                                },
                                "quran-qaloon": {
                                    "editionCount": 12,
                                    "types": {
                                        "surah": 8,
                                        "versebyverse": 4
                                    },
                                    "languageCount": 1
                                },
                                "quran-aldouri": {
                                    "editionCount": 6,
                                    "types": {
                                        "surah": 4,
                                        "versebyverse": 2
                                    },
                                    "languageCount": 1
                                },
                                "quran-albazzi": {
                                    "editionCount": 3,
                                    "types": {
                                        "surah": 2,
                                        "versebyverse": 1
                                    },
                                    "languageCount": 1
                                },
                                "quran-shoba": {
                                    "editionCount": 4,
                                    "types": {
                                        "surah": 2,
                                        "versebyverse": 2
                                    },
                                    "languageCount": 1
                                },
                                "quran-alsoosi": {
                                    "editionCount": 2,
                                    "types": {
                                        "surah": 1,
                                        "versebyverse": 1
                                    },
                                    "languageCount": 1
                                },
                                "quran-qunbul": {
                                    "editionCount": 2,
                                    "types": {
                                        "surah": 1,
                                        "versebyverse": 1
                                    },
                                    "languageCount": 1
                                }
                            },
                            "bitrates": {
                                "uniqueBitrates": 12,
                                "availableBitrates": [
                                    16,
                                    32,
                                    40,
                                    48,
                                    56,
                                    64,
                                    96,
                                    128,
                                    160,
                                    192,
                                    256,
                                    320
                                ],
                                "statistics": {
                                    "average": 120.14,
                                    "minimum": 16,
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

getTheEditionSubtypesByTypeResponse = {
    200: {
        "description": "Successful Response - List of all available subtypes for the specified edition type",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        "irab",
                        "gharib",
                        "tafsir"
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching subtypes",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Subtypes not found"
                }
            }
        }
    }
}
