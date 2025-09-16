

getAllSajdaResponse={
        200: {
            "description": "Returns all ayahs (verses) in the Quran that require Sajda (prostration), including their metadata and sajda type. Useful for study, navigation, and LLM workflows.",
            "content": {
                "application/json": {
                    "example":   {
                           "ayahs": [
                        {
                            "number": 2138,
                            "text": "وَيَخِرُّونَ لِلْأَذْقَانِ يَبْكُونَ وَيَزِيدُهُمْ خُشُوعًا۩",
                            "surah": {
                            "number": 17,
                            "name": "سورة الإسراء",
                            "englishName": "Al-Israa",
                            "englishNameTranslation": "The Night Journey",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 111
                            },
                            "numberInSurah": 109,
                            "juz": 15,
                            "manzil": 4,
                            "page": 293,
                            "ruku": 251,
                            "hizbQuarter": 117,
                            "sajda": {
                            "id": 4,
                            "recommended": True,
                            "obligatory": False
                            }
                        },
                        {
                            "number": 3185,
                            "text": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ رَبُّ الْعَرْشِ الْعَظِيمِ۩",
                            "surah": {
                            "number": 27,
                            "name": "سورة النمل",
                            "englishName": "An-Naml",
                            "englishNameTranslation": "The Ant",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 93
                            },
                            "numberInSurah": 26,
                            "juz": 19,
                            "manzil": 5,
                            "page": 379,
                            "ruku": 328,
                            "hizbQuarter": 151,
                            "sajda": {
                            "id": 9,
                            "recommended": True,
                            "obligatory": False
                            }
                        },
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
        ,
        400: {
            "description": "Bad Request - Error occurred while fetching Sajda ayahs. The response contains an error message explaining the failure.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "Something Went Wrong, Sajdas not found"
                    }
                }
            }
        }
}

getSajdabyEditionResponse={
        200: {
            "description": "Returns all ayahs (verses) requiring Sajda from a particular edition, including their metadata and sajda type. Useful for edition-specific study, navigation, and LLM workflows.",
            "content": {
                "application/json": {
                    "example":   {
                    "ayahs": [
                        {
                            "number": 1951,
                            "text": "يَخَافُونَ رَبَّهُم مِّن فَوْقِهِمْ وَيَفْعَلُونَ مَا يُؤْمَرُونَ ۩",
                            "surah": {
                            "number": 16,
                            "name": "سورة النحل",
                            "englishName": "An-Nahl",
                            "englishNameTranslation": "The Bee",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 128
                            },
                            "numberInSurah": 50,
                            "juz": 14,
                            "manzil": 3,
                            "page": 272,
                            "ruku": 229,
                            "hizbQuarter": 108,
                            "sajda": {
                            "id": 3,
                            "recommended": True,
                            "obligatory": False
                            }
                        },
                        {
                            "number": 4256,
                            "text": "فَإِنِ ٱسْتَكْبَرُوا۟ فَٱلَّذِينَ عِندَ رَبِّكَ يُسَبِّحُونَ لَهُۥ بِٱلَّيْلِ وَٱلنَّهَارِ وَهُمْ لَا يَسْـَٔمُونَ ۩",
                            "surah": {
                            "number": 41,
                            "name": "سورة فصلت",
                            "englishName": "Fussilat",
                            "englishNameTranslation": "Explained in detail",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 54
                            },
                            "numberInSurah": 38,
                            "juz": 24,
                            "manzil": 6,
                            "page": 480,
                            "ruku": 417,
                            "hizbQuarter": 192,
                            "sajda": {
                            "id": 12,
                            "recommended": False,
                            "obligatory": True
                            }
                        },
                        {
                            "number": 2138,
                            "text": "وَيَخِرُّونَ لِلْأَذْقَانِ يَبْكُونَ وَيَزِيدُهُمْ خُشُوعًۭا ۩",
                            "surah": {
                            "number": 17,
                            "name": "سورة الإسراء",
                            "englishName": "Al-Israa",
                            "englishNameTranslation": "The Night Journey",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 111
                            },
                            "numberInSurah": 109,
                            "juz": 15,
                            "manzil": 4,
                            "page": 293,
                            "ruku": 251,
                            "hizbQuarter": 117,
                            "sajda": {
                            "id": 4,
                            "recommended": True,
                            "obligatory": False
                            }
                        },
                        {
                            "number": 2308,
                            "text": "أُو۟لَٰٓئِكَ ٱلَّذِينَ أَنْعَمَ ٱللَّهُ عَلَيْهِم مِّنَ ٱلنَّبِيِّۦنَ مِن ذُرِّيَّةِ ءَادَمَ وَمِمَّنْ حَمَلْنَا مَعَ نُوحٍۢ وَمِن ذُرِّيَّةِ إِبْرَٰهِيمَ وَإِسْرَٰٓءِيلَ وَمِمَّنْ هَدَيْنَا وَٱجْتَبَيْنَآ ۚ إِذَا تُتْلَىٰ عَلَيْهِمْ ءَايَٰتُ ٱلرَّحْمَٰنِ خَرُّوا۟ سُجَّدًۭا وَبُكِيًّۭا ۩",
                            "surah": {
                            "number": 19,
                            "name": "سورة مريم",
                            "englishName": "Maryam",
                            "englishNameTranslation": "Mary",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 98
                            },
                            "numberInSurah": 58,
                            "juz": 16,
                            "manzil": 4,
                            "page": 309,
                            "ruku": 267,
                            "hizbQuarter": 123,
                            "sajda": {
                            "id": 5,
                            "recommended": True,
                            "obligatory": False
                            }
                        },
                        ],
                    "edition": {
                    "identifier": "quran-uthmani",
                    "language": "ar",
                    "name": "Uthamani",
                    "englishName": "Uthamani",
                    "format": "text",
                    "type": "quran",
                    "direction": "rtl"
                    }
                    }
                }
                }
            }
        ,
        400: {
            "description": "Bad Request - Error occurred while fetching Sajda ayahs for the specified edition. The response contains an error message explaining the failure.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "Something Went Wrong, Edition not found"
                    }
                }
            }
        }
}
