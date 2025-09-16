# Enhanced Surah API Documentation
# Updated response examples based on current API structure and database samples

getAllSurahResponse = {
    200: {
        "description": "Returns the complete list of all 114 Surahs (chapters) in the Quran, with metadata such as page ranges, revelation details, and structural information. Useful for navigation, search, and LLM workflows.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "number": 1,
                            "startingPage": 1,
                            "endingPage": 1,
                            "name": "سورة الفاتحة",
                            "englishName": "Al-Faatiha",
                            "englishNameTranslation": "The Opening",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 7,
                            "revelationOrder": 5
                        },
                        {
                            "number": 2,
                            "startingPage": 2,
                            "endingPage": 49,
                            "name": "سورة البقرة",
                            "englishName": "Al-Baqarah",
                            "englishNameTranslation": "The Cow",
                            "revelationType": "Medinan",
                            "numberOfAyahs": 286,
                            "revelationOrder": 87
                        },
                        {
                            "number": 3,
                            "startingPage": 50,
                            "endingPage": 76,
                            "name": "سورة آل عمران",
                            "englishName": "Aal-i-Imraan",
                            "englishNameTranslation": "The Family of Imraan",
                            "revelationType": "Medinan",
                            "numberOfAyahs": 200,
                            "revelationOrder": 89
                        },
                        {
                            "number": 4,
                            "startingPage": 77,
                            "endingPage": 106,
                            "name": "سورة النساء",
                            "englishName": "An-Nisaa",
                            "englishNameTranslation": "The Women",
                            "revelationType": "Medinan",
                            "numberOfAyahs": 176,
                            "revelationOrder": 92
                        },
                        {
                            "number": 114,
                            "startingPage": 604,
                            "endingPage": 604,
                            "name": "سورة الناس",
                            "englishName": "An-Naas",
                            "englishNameTranslation": "Mankind",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 6,
                            "revelationOrder": 21
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Error occurred while fetching Surahs. The response contains an error message explaining the failure.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Unable to fetch Surah list"
                }
            }
        }
    }
}

getOneSurahResponse = {
    200: {
    "description": "Returns detailed information about a specific Surah (chapter), including all ayahs, metadata, structural divisions, and edition-specific formatting. The editionIdentifier (e.g., 'ar.abdulbasitmurattal.hafs') must be provided as a path parameter, not as a query parameter. Useful for retrieving the full text and structure of a chapter.",
        "content": {
            "application/json": {
                "examples": {
                    "text_edition_surah": {
                        "summary": "Text Edition Surah Response",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 1,
                                "name": "سورة الفاتحة",
                                "englishName": "Al-Faatiha",
                                "englishNameTranslation": "The Opening",
                                "revelationType": "Meccan",
                                "numberOfAyahs": 7,
                                "revelationOrder": 5,
                                "edition": {
                                    "identifier": "quran-simple",
                                    "language": "ar",
                                    "name": "Simple",
                                    "englishName": "Simple",
                                    "format": "text",
                                    "type": "quran",
                                    "direction": "rtl"
                                },
                                "ayahs": [
                                    {
                                        "number": 1,
                                        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
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
                                        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
                                        "numberInSurah": 2,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 1,
                                        "ruku": 1,
                                        "hizbQuarter": 1,
                                        "sajda": False
                                    },
                                    {
                                        "number": 7,
                                        "text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
                                        "numberInSurah": 7,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 1,
                                        "ruku": 1,
                                        "hizbQuarter": 1,
                                        "sajda": False
                                    }
                                ]
                            }
                        }
                    },
                    "audio_edition_surah": {
                        "summary": "Audio Edition Surah with Streaming URLs",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 1,
                                "name": "سورة الفاتحة", 
                                "englishName": "Al-Faatiha",
                                "englishNameTranslation": "The Opening",
                                "revelationType": "Meccan",
                                "numberOfAyahs": 7,
                                "revelationOrder": 5,
                                "edition": {
                                    "identifier": "ar.mahmoudkhalilalhusary.hafs",
                                    "language": "ar",
                                    "name": "محمود خليل الحصري",
                                    "englishName": "Mahmoud Khalil Al-Husary",
                                    "format": "audio",
                                    "type": "versebyverse",
                                    "direction": "rtl",
                                    "description": {
                                        "ar": "محمود خليل الحصري (1917-1980): قارئ مصري كبير حفظ القرآن في سن 8. أول من سجّل المصحف المرتل كاملاً، حمل لقب شيخ المقارئ وفاز بمسابقة الإذاعة المصرية 1944. وُلد في طنطا.",
                                        "en": "Mahmoud Khalil Al-Husary (1917-1980): Egyptian master reciter who memorized the Quran by age 8. First to record the complete Murattal Quran, he held the title Shaykh al-Maqari and won Egypt Radio's 1944 competition. Born in Tanta."
                                    },
                                    "imageUrl": "https://quranhub.b-cdn.net/quran/images/reciters/mahmoud-khalil-al-husary.jpeg"
                                },
                                "ayahs": [
                                    {
                                        "number": 1,
                                        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                                        "numberInSurah": 1,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 1,
                                        "ruku": 1,
                                        "hizbQuarter": 1,
                                        "sajda": False,
                                        "audio": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.mahmoudkhalilalhusary.hafs/1.mp3",
                                        "audioSecondary": [
                                            "https://quranhub.b-cdn.net/quran/audio/versebyverse/64/ar.mahmoudkhalilalhusary.hafs/1.mp3"
                                        ]
                                    }
                                ]
                            }
                        }
                    },
                    "tafsir_edition_surah": {
                        "summary": "Tafsir Edition Surah with Commentary",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "number": 1,
                                "name": "سورة الفاتحة",
                                "englishName": "Al-Faatiha",
                                "englishNameTranslation": "The Opening",
                                "revelationType": "Meccan",
                                "numberOfAyahs": 7,
                                "revelationOrder": 5,
                                "edition": {
                                    "identifier": "ar.mukhtasar",
                                    "language": "ar",
                                    "name": "المختصر في التفسير",
                                    "englishName": "Al-Mukhtasar",
                                    "format": "text",
                                    "type": "tafsir",
                                    "direction": "rtl"
                                },
                                "ayahs": [
                                    {
                                        "number": 1,
                                        "text": "سورة الفاتحة سميت هذه السورة بالفاتحة؛ لأنه يفتتح بها القرآن العظيم، وتسمى المثاني؛ لأنها تقرأ في كل ركعة، ولها أسماء أخر. أبتدئ قراءة القرآن بسم الله مستعينا به(اللهِ) علم على الرب -تبارك وتعالى- المعبود بحق دون سواه، وهو أخص أسماء الله تعالى، ولا يسمى به غيره سبحانه.",
                                        "numberInSurah": 1,
                                        "juz": 1,
                                        "manzil": 1,
                                        "page": 1,
                                        "ruku": 1,
                                        "hizbQuarter": 1,
                                        "sajda": False
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid Surah number or edition not found",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_surah_number": {
                        "summary": "Invalid Surah Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Surah number must be between 1 and 114"
                        }
                    },
                    "edition_not_found": {
                        "summary": "Edition Not Found",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Something wrong happened: Edition not found"
                        }
                    }
                }
            }
        }
    }
}

getSurahByRangeResponse = {
    200: {
        "description": "Successful Response - Specific range of ayahs from a Surah with complete metadata and edition-specific formatting. Perfect for pagination and targeted content retrieval",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 2,
                        "name": "سورة البقرة",
                        "englishName": "Al-Baqarah",
                        "englishNameTranslation": "The Cow",
                        "revelationType": "Medinan",
                        "numberOfAyahs": 286,
                        "revelationOrder": 87,
                        "edition": {
                            "identifier": "en.sahih",
                            "language": "en",
                            "name": "Saheeh International",
                            "englishName": "Saheeh International",
                            "format": "text",
                            "type": "translation",
                            "direction": "ltr"
                        },
                        "ayahs": [
                            {
                                "number": 255,
                                "text": "Allah - there is no deity except Him, the Ever-Living, the Sustainer of existence. Neither drowsiness overtakes Him nor sleep. To Him belongs whatever is in the heavens and whatever is on the earth. Who is it that can intercede with Him except by His permission? He knows what is [presently] before them and what will be after them, and they encompass not a thing of His knowledge except for what He wills. His Kursi extends over the heavens and the earth, and their preservation tires Him not. And He is the Most High, the Most Great.",
                                "numberInSurah": 255,
                                "juz": 3,
                                "manzil": 1,
                                "page": 42,
                                "ruku": 33,
                                "hizbQuarter": 17,
                                "sajda": False
                            },
                            {
                                "number": 256,
                                "text": "There shall be no compulsion in [acceptance of] the religion. The right course has become clear from the wrong. So whoever disbelieves in Taghut and believes in Allah has grasped the most trustworthy handhold with no break in it. And Allah is Hearing and Knowing.",
                                "numberInSurah": 256,
                                "juz": 3,
                                "manzil": 1,
                                "page": 42,
                                "ruku": 33,
                                "hizbQuarter": 17,
                                "sajda": False
                            }
                        ],
                        "requestedRange": {
                            "startAyah": 255,
                            "endAyah": 256,
                            "totalInRange": 2
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request - Invalid range parameters or Surah not found",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_range": {
                        "summary": "Invalid Ayah Range",
                        "value": {
                            "code": 400,
                            "status": "Error", 
                            "data": "Start ayah number must be less than or equal to end ayah number"
                        }
                    },
                    "range_exceeds_surah": {
                        "summary": "Range Exceeds Surah Length",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "End ayah number exceeds the total number of ayahs in this Surah"
                        }
                    }
                }
            }
        }
    }
}

# Alias for getOneSurahResponse - Get Single Surah
getTheSurahResponse = getOneSurahResponse

# GET /surah/{surahNumber}/{editionIdentifier} - Get Surah by Number and Edition
getTheSurahbyEditionResponse = {
    200: {
        "description": "Returns a specific Surah (chapter) from a particular edition (translation, script, or recitation), including all ayahs and edition metadata. Useful for retrieving a chapter in a specific format or language.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 1,
                        "startingPage": 1,
                        "endingPage": 1,
                        "name": "سورة الفاتحة",
                        "englishName": "Al-Faatiha",
                        "englishNameTranslation": "The Opening",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 7,
                        "revelationOrder": 5,
                        "ayahs": [
                            {
                                "number": 1,
                                "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
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
                                "numberInSurah": 2,
                                "juz": 1,
                                "manzil": 1,
                                "page": 1,
                                "ruku": 1,
                                "hizbQuarter": 1,
                                "sajda": False
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
        "description": "Bad Request",
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

# GET /surah/{surahNumber}/{editionIdentifiers} - Get Surah from Multiple Editions
getTheSurahbyEditionsResponse = {
    200: {
        "description": "Returns a Surah (chapter) from multiple editions (comma-separated) for comparison, including all ayahs and edition metadata. Useful for comparing translations, scripts, or recitations side by side.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 1,
                        "startingPage": 1,
                        "endingPage": 1,
                        "name": "سورة الفاتحة",
                        "englishName": "Al-Faatiha",
                        "englishNameTranslation": "The Opening",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 7,
                        "revelationOrder": 5,
                        "ayahs": [
                            {
                                "number": 1,
                                "editions": [
                                    {
                                        "text": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
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
                                        "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
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
                                ],
                                "numberInSurah": 1,
                                "juz": 1,
                                "manzil": 1,
                                "page": 1,
                                "ruku": 1,
                                "hizbQuarter": 1,
                                "sajda": False
                            }
                        ]
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something went wrong: One or more editions not found"
                }
            }
        }
    }
}
