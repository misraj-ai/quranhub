# Enhanced Ayah API Documentation
# Updated response examples based on current API structure and database samples

getRandomAyahResponse = {
    200: {
    "description": "Returns a random ayah from the Quran in the default edition. Use this to discover or display a random verse, or as a starting point for further exploration.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 5876,
                        "text": "عَيْنًا يَشْرَبُ بِهَا الْمُقَرَّبُونَ",
                        "edition": {
                            "identifier": "quran-simple",
                            "language": "ar",
                            "name": "Simple",
                            "englishName": "Simple",
                            "format": "text",
                            "type": "quran",
                            "direction": "rtl"
                        },
                        "surah": {
                            "number": 83,
                            "name": "سورة المطففين",
                            "englishName": "Al-Mutaffifin",
                            "englishNameTranslation": "Defrauding",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 36
                        },
                        "numberInSurah": 28,
                        "juz": 30,
                        "manzil": 7,
                        "page": 588,
                        "ruku": 525,
                        "hizbQuarter": 235,
                        "sajda": False
                    }
                }
            }
        }
    },
    400: {
    "description": "Bad request. The random ayah could not be retrieved. Check the request or try again later.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Ayah not found"
                }
            }
        }
    }
}

getRandomAyahbyEditionResponse = {
    200: {
    "description": "Returns a random ayah from the Quran in the specified edition. The editionIdentifier (e.g., 'ar.abdulbasitmurattal.hafs') must be provided as a path parameter, not as a query parameter. Use this to discover a random verse in a particular translation or script.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 1697,
                        "text": "۞ رَبِّ قَدْ ءَاتَيْتَنِى مِنَ ٱلْمُلْكِ وَعَلَّمْتَنِى مِن تَأْوِيلِ ٱلْأَحَادِيثِ ۚ فَاطِرَ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضِ أَنتَ وَلِىِّۦ فِى ٱلدُّنْيَا وَٱلْءَاخِرَةِ ۖ تَوَفَّنِى مُسْلِمًۭا وَأَلْحِقْنِى بِٱلصَّٰلِحِينَ",
                        "edition": {
                            "identifier": "quran-uthmani",
                            "language": "ar",
                            "name": "Uthamani",
                            "englishName": "Uthamani",
                            "format": "text",
                            "type": "quran",
                            "direction": "rtl"
                        },
                        "surah": {
                            "number": 12,
                            "name": "سورة يوسف",
                            "englishName": "Yusuf",
                            "englishNameTranslation": "Joseph",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 111
                        },
                        "numberInSurah": 101,
                        "juz": 13,
                        "manzil": 3,
                        "page": 247,
                        "ruku": 203,
                        "hizbQuarter": 99,
                        "sajda": False
                    }
                }
            }
        }
    },
    400: {
    "description": "Bad request. The random ayah for the specified edition could not be retrieved. Check the edition identifier or try again later.",
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

getRandomAyahbyEditionsResponse = {
    200: {
    "description": "Returns a random ayah from the Quran in the specified editions. Use this to compare a random verse across different translations or scripts.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "number": 2843,
                            "text": "وَمَا كَانَ اللَّهُ لِيُعَذِّبَهُمْ وَأَنتَ فِيهِمْ ۚ وَمَا كَانَ اللَّهُ مُعَذِّبَهُمْ وَهُمْ يَسْتَغْفِرُونَ",
                            "edition": {
                                "identifier": "quran-simple",
                                "language": "ar",
                                "name": "Simple",
                                "englishName": "Simple",
                                "format": "text",
                                "type": "quran",
                                "direction": "rtl"
                            },
                            "surah": {
                                "number": 8,
                                "name": "سورة الأنفال",
                                "englishName": "Al-Anfal",
                                "englishNameTranslation": "The Spoils of War",
                                "revelationType": "Medinan",
                                "numberOfAyahs": 75
                            },
                            "numberInSurah": 33,
                            "juz": 10,
                            "manzil": 3,
                            "page": 183,
                            "ruku": 149,
                            "hizbQuarter": 73,
                            "sajda": False
                        },
                        {
                            "number": 2843,
                            "text": "But Allah would not punish them while you, [O Muhammad], are among them, and Allah would not punish them while they seek forgiveness.",
                            "edition": {
                                "identifier": "en.sahih",
                                "language": "en",
                                "name": "Saheeh International",
                                "englishName": "Saheeh International",
                                "format": "text",
                                "type": "translation",
                                "direction": "ltr"
                            },
                            "surah": {
                                "number": 8,
                                "name": "سورة الأنفال",
                                "englishName": "Al-Anfal",
                                "englishNameTranslation": "The Spoils of War",
                                "revelationType": "Medinan",
                                "numberOfAyahs": 75
                            },
                            "numberInSurah": 33,
                            "juz": 10,
                            "manzil": 3,
                            "page": 183,
                            "ruku": 149,
                            "hizbQuarter": 73,
                            "sajda": False
                        }
                    ]
                }
            }
        }
    },
    400: {
    "description": "Bad request. The random ayah for the specified editions could not be retrieved. Check the edition identifiers or try again later.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: One or more editions not found"
                }
            }
        }
    }
}

getTheAyahResponse = {
    200: {
    "description": "Returns an ayah by its global number or by surah:ayah format (e.g., 2:255). Use this to fetch a specific verse for display, analysis, or further processing.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 1,
                        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                        "edition": {
                            "identifier": "quran-simple",
                            "language": "ar",
                            "name": "Simple",
                            "englishName": "Simple",
                            "format": "text",
                            "type": "quran",
                            "direction": "rtl"
                        },
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
                    }
                }
            }
        }
    },
    400: {
    "description": "Bad request. The ayah could not be retrieved. Check the reference or try again later.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Ayah not found"
                }
            }
        }
    }
}

getTheAyahbyEditionResponse = {
    200: {
    "description": "Returns an ayah by its global number or surah:ayah format for a specified edition. Use this to fetch a specific verse in a particular translation or script.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 1,
                        "text": "سورة الفاتحة سميت هذه السورة بالفاتحة؛ لأنه يفتتح بها القرآن العظيم، وتسمى المثاني؛ لأنها تقرأ في كل ركعة، ولها أسماء أخر. أبتدئ قراءة القرآن بسم الله مستعينا به(اللهِ) علم على الرب -تبارك وتعالى- المعبود بحق دون سواه، وهو أخص أسماء الله تعالى، ولا يسمى به غيره سبحانه. (الرَّحْمَنِ) ذي الرحمة العامة الذي وسعت رحمته جميع الخلق،(الرَّحِيمِ) بالمؤمنين، وهما اسمان من أسمائه تعالى، يتضمنان إثبات صفة الرحمة لله تعالى كما يليق بجلاله.",
                        "edition": {
                            "identifier": "ar.mukhtasar",
                            "language": "ar",
                            "name": "المختصر في التفسير",
                            "englishName": "Al-Mukhtasar",
                            "format": "text",
                            "type": "tafsir",
                            "direction": "rtl"
                        },
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
                    }
                }
            }
        }
    },
    400: {
    "description": "Bad request. The ayah for the specified edition could not be retrieved. Check the reference or edition identifier and try again.",
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

getTheAyahbyEditionsResponse = {
    200: {
    "description": "Returns an ayah by its global number or surah:ayah format for the specified editions. Use this to compare a specific verse across different translations or scripts.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": [
                        {
                            "number": 1,
                            "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                            "edition": {
                                "identifier": "quran-simple",
                                "language": "ar",
                                "name": "Simple",
                                "englishName": "Simple",
                                "format": "text",
                                "type": "quran",
                                "direction": "rtl"
                            },
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
                            "number": 1,
                            "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
                            "edition": {
                                "identifier": "en.sahih",
                                "language": "en",
                                "name": "Saheeh International",
                                "englishName": "Saheeh International",
                                "format": "text",
                                "type": "translation",
                                "direction": "ltr"
                            },
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
                        }
                    ]
                }
            }
        }
    },
    400: {
    "description": "Bad request. The ayah for the specified editions could not be retrieved. Check the reference or edition identifiers and try again.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: One or more editions not found"
                }
            }
        }
    }
}

# Audio Response Examples for Audio Editions
getTheAyahAudioResponse = {
    200: {
    "description": "Returns an ayah with audio URLs for recitation. Use this to play or download the recitation for a specific verse in a particular audio edition.",
        "content": {
            "application/json": {
                "example": {
                    "code": 200,
                    "status": "OK",
                    "data": {
                        "number": 1,
                        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                        "edition": {
                            "identifier": "ar.abdullahbasfar.hafs",
                            "language": "ar",
                            "name": "عبد الله بصفر",
                            "englishName": "Abdullah Basfar",
                            "format": "audio",
                            "type": "versebyverse",
                            "direction": "rtl",
                            "description": {
                                "ar": "عبد الله بصفر: قارئ سعودي بارز وأستاذ مشارك في جامعة الملك عبد العزيز بجدة. الأمين العام السابق للهيئة العالمية للكتاب والسنة، معروف بصوته العذب وإسهاماته العلمية.",
                                "en": "Abdullah Basfar: Prominent Saudi reciter and associate professor at King Abdulaziz University in Jeddah. Former Secretary-General of the World Book and Sunnah Organization, known for his melodious voice and scholarly contributions."
                            },
                            "imageUrl": "https://quranhub.b-cdn.net/quran/images/reciters/abdullah-basfar.jpeg"
                        },
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
                        "audio": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdullahbasfar.hafs/1.mp3",
                        "audioSecondary": [
                            "https://quranhub.b-cdn.net/quran/audio/versebyverse/64/ar.abdullahbasfar.hafs/1.mp3"
                        ]
                    }
                }
            }
        }
    },
    400: {
    "description": "Bad request. The audio edition could not be retrieved. Check the audio edition identifier and try again.",
        "content": {
            "application/json": {
                "example": {
                    "code": 400,
                    "status": "Error",
                    "data": "Something wrong happened: Audio edition not found"
                }
            }
        }
    }
}
