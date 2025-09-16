
getHizbQuarterbyNumberResponse={
        200: {
        "description": "Returns the requested Hizb Quarter by its number (1-240). Use this to fetch the content of a specific Hizb Quarter for display or analysis.",
            "content": {
                "application/json": {
                    "example":   {
                        "number": 240,
                        "ayahs": [
                        {
                            "number": 6155,
                            "text": "۞أَفَلَا يَعْلَمُ إِذَا بُعْثِرَ مَا فِي الْقُبُورِ",
                            "surah": {
                            "number": 100,
                            "name": "سورة العاديات",
                            "englishName": "Al-Aadiyaat",
                            "englishNameTranslation": "The Chargers",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 11
                            },
                            "numberInSurah": 9,
                            "juz": 30,
                            "manzil": 7,
                            "page": 599,
                            "ruku": 542,
                            "hizbQuarter": 240,
                            "sajda": False
                        },
                        {
                            "number": 6156,
                            "text": "وَحُصِّلَ مَا فِي الصُّدُورِ",
                            "surah": {
                            "number": 100,
                            "name": "سورة العاديات",
                            "englishName": "Al-Aadiyaat",
                            "englishNameTranslation": "The Chargers",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 11
                            },
                            "numberInSurah": 10,
                            "juz": 30,
                            "manzil": 7,
                            "page": 600,
                            "ruku": 542,
                            "hizbQuarter": 240,
                            "sajda": False
                        },
                        {
                            "number": 6157,
                            "text": "إِنَّ رَبَّهُمْ بِهِمْ يَوْمَئِذٍ لَخَبِيرٌ",
                            "surah": {
                            "number": 100,
                            "name": "سورة العاديات",
                            "englishName": "Al-Aadiyaat",
                            "englishNameTranslation": "The Chargers",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 11
                            },
                            "numberInSurah": 11,
                            "juz": 30,
                            "manzil": 7,
                            "page": 600,
                            "ruku": 542,
                            "hizbQuarter": 240,
                            "sajda": False
                        },
                        {
                            "number": 6158,
                            "text": "الْقَارِعَةُ",
                            "surah": {
                            "number": 101,
                            "name": "سورة القارعة",
                            "englishName": "Al-Qaari'a",
                            "englishNameTranslation": "The Calamity",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 11
                            },
                            "numberInSurah": 1,
                            "juz": 30,
                            "manzil": 7,
                            "page": 600,
                            "ruku": 543,
                            "hizbQuarter": 240,
                            "sajda": False
                        },
                        {
                            "number": 6159,
                            "text": "مَا الْقَارِعَةُ",
                            "surah": {
                            "number": 101,
                            "name": "سورة القارعة",
                            "englishName": "Al-Qaari'a",
                            "englishNameTranslation": "The Calamity",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 11
                            },
                            "numberInSurah": 2,
                            "juz": 30,
                            "manzil": 7,
                            "page": 600,
                            "ruku": 543,
                            "hizbQuarter": 240,
                            "sajda": False
                        }
                        ],
                        "surahs": [
                        {
                            "number": 100,
                            "name": "سورة العاديات",
                            "englishName": "Al-Aadiyaat",
                            "englishNameTranslation": "The Chargers",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 11
                        },
                        {
                            "number": 101,
                            "name": "سورة القارعة",
                            "englishName": "Al-Qaari'a",
                            "englishNameTranslation": "The Calamity",
                            "revelationType": "Meccan",
                            "numberOfAyahs": 11
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
        },
        400: {
        "description": "Bad request. The Hizb Quarter could not be retrieved. Check the hizbQuarterNumber or try again later.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "HizbQuarter number should be betwen 1 and 240"
                    }
                }
            }
        }
    }

getHizbQuarterbyEditionResponse={
        200: {
        "description": "Returns the requested Hizb Quarter from a particular edition. Use this to fetch the content of a specific Hizb Quarter in a specific edition for display or analysis.",
            "content": {
                "application/json": {
                    "example":   {
                    "number": 240,
                    "ayahs": [
                    {
                        "number": 6155,
                        "text": "۞ أَفَلَا يَعْلَمُ إِذَا بُعْثِرَ مَا فِى ٱلْقُبُورِ",
                        "surah": {
                        "number": 100,
                        "name": "سورة العاديات",
                        "englishName": "Al-Aadiyaat",
                        "englishNameTranslation": "The Chargers",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 11
                        },
                        "numberInSurah": 9,
                        "juz": 30,
                        "manzil": 7,
                        "page": 599,
                        "ruku": 542,
                        "hizbQuarter": 240,
                        "sajda": False
                    },
                    {
                        "number": 6156,
                        "text": "وَحُصِّلَ مَا فِى ٱلصُّدُورِ",
                        "surah": {
                        "number": 100,
                        "name": "سورة العاديات",
                        "englishName": "Al-Aadiyaat",
                        "englishNameTranslation": "The Chargers",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 11
                        },
                        "numberInSurah": 10,
                        "juz": 30,
                        "manzil": 7,
                        "page": 600,
                        "ruku": 542,
                        "hizbQuarter": 240,
                        "sajda": False
                    },
                    {
                        "number": 6157,
                        "text": "إِنَّ رَبَّهُم بِهِمْ يَوْمَئِذٍۢ لَّخَبِيرٌۢ",
                        "surah": {
                        "number": 100,
                        "name": "سورة العاديات",
                        "englishName": "Al-Aadiyaat",
                        "englishNameTranslation": "The Chargers",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 11
                        },
                        "numberInSurah": 11,
                        "juz": 30,
                        "manzil": 7,
                        "page": 600,
                        "ruku": 542,
                        "hizbQuarter": 240,
                        "sajda": False
                    },
                    {
                        "number": 6158,
                        "text": "ٱلْقَارِعَةُ",
                        "surah": {
                        "number": 101,
                        "name": "سورة القارعة",
                        "englishName": "Al-Qaari'a",
                        "englishNameTranslation": "The Calamity",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 11
                        },
                        "numberInSurah": 1,
                        "juz": 30,
                        "manzil": 7,
                        "page": 600,
                        "ruku": 543,
                        "hizbQuarter": 240,
                        "sajda": False
                    },
                    {
                        "number": 6159,
                        "text": "مَا ٱلْقَارِعَةُ",
                        "surah": {
                        "number": 101,
                        "name": "سورة القارعة",
                        "englishName": "Al-Qaari'a",
                        "englishNameTranslation": "The Calamity",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 11
                        },
                        "numberInSurah": 2,
                        "juz": 30,
                        "manzil": 7,
                        "page": 600,
                        "ruku": 543,
                        "hizbQuarter": 240,
                        "sajda": False
                    }
                    ],
                    "surahs": [
                    {
                        "number": 100,
                        "name": "سورة العاديات",
                        "englishName": "Al-Aadiyaat",
                        "englishNameTranslation": "The Chargers",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 11
                    },
                    {
                        "number": 101,
                        "name": "سورة القارعة",
                        "englishName": "Al-Qaari'a",
                        "englishNameTranslation": "The Calamity",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 11
                    }
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
        },
        400: {
        "description": "Bad request. The Hizb Quarter for the specified edition could not be retrieved. Check the hizbQuarterNumber, editionIdentifier, or try again later.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "HizbQuarter number should be betwen 1 and 240"
                    }
                }
            }
        }
    }


