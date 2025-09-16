

getAllMetaResponse={
        200: {
            "description": "Returns all available meta data about the Qur'an, including ayahs, surahs, sajdas, rukus, pages, manzils, hizbquarters, and juzs. Use this to understand the structure and references for navigation or analysis.",
            "content": {
                "application/json": {
                    "example":   {
                    "ayahs": {
                        "count": 6236
                        },
                        "surahs": {
                        "count": 114,
                        "references": [
                            {
                            "number": 2,
                            "name": "سورة البقرة",
                            "englishName": "Al-Baqara",
                            "englishNameTranslation": "The Cow",
                            "numberOfAyahs": 286,
                            "revelationType": "Medinan"
                            },
                            {
                            "number": 3,
                            "name": "سورة آل عمران",
                            "englishName": "Aal-i-Imraan",
                            "englishNameTranslation": "The Family of Imraan",
                            "numberOfAyahs": 200,
                            "revelationType": "Medinan"
                            },
                            {
                            "number": 4,
                            "name": "سورة النساء",
                            "englishName": "An-Nisaa",
                            "englishNameTranslation": "The Women",
                            "numberOfAyahs": 176,
                            "revelationType": "Medinan"
                            },
                            {
                            "number": 5,
                            "name": "سورة المائدة",
                            "englishName": "Al-Maaida",
                            "englishNameTranslation": "The Table",
                            "numberOfAyahs": 120,
                            "revelationType": "Medinan"
                            },
                            {
                            "number": 6,
                            "name": "سورة الأنعام",
                            "englishName": "Al-An'aam",
                            "englishNameTranslation": "The Cattle",
                            "numberOfAyahs": 165,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 7,
                            "name": "سورة الأعراف",
                            "englishName": "Al-A'raaf",
                            "englishNameTranslation": "The Heights",
                            "numberOfAyahs": 206,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 8,
                            "name": "سورة الأنفال",
                            "englishName": "Al-Anfaal",
                            "englishNameTranslation": "The Spoils of War",
                            "numberOfAyahs": 75,
                            "revelationType": "Medinan"
                            },
                            {
                            "number": 9,
                            "name": "سورة التوبة",
                            "englishName": "At-Tawba",
                            "englishNameTranslation": "The Repentance",
                            "numberOfAyahs": 129,
                            "revelationType": "Medinan"
                            },
                            {
                            "number": 10,
                            "name": "سورة يونس",
                            "englishName": "Yunus",
                            "englishNameTranslation": "Jonas",
                            "numberOfAyahs": 109,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 11,
                            "name": "سورة هود",
                            "englishName": "Hud",
                            "englishNameTranslation": "Hud",
                            "numberOfAyahs": 123,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 12,
                            "name": "سورة يوسف",
                            "englishName": "Yusuf",
                            "englishNameTranslation": "Joseph",
                            "numberOfAyahs": 111,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 13,
                            "name": "سورة الرعد",
                            "englishName": "Ar-Ra'd",
                            "englishNameTranslation": "The Thunder",
                            "numberOfAyahs": 43,
                            "revelationType": "Medinan"
                            },
                            {
                            "number": 14,
                            "name": "سورة ابراهيم",
                            "englishName": "Ibrahim",
                            "englishNameTranslation": "Abraham",
                            "numberOfAyahs": 52,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 15,
                            "name": "سورة الحجر",
                            "englishName": "Al-Hijr",
                            "englishNameTranslation": "The Rock",
                            "numberOfAyahs": 99,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 16,
                            "name": "سورة النحل",
                            "englishName": "An-Nahl",
                            "englishNameTranslation": "The Bee",
                            "numberOfAyahs": 128,
                            "revelationType": "Meccan"
                            },
                            {
                            "number": 17,
                            "name": "سورة الإسراء",
                            "englishName": "Al-Israa",
                            "englishNameTranslation": "The Night Journey",
                            "numberOfAyahs": 111,
                            "revelationType": "Meccan"
                            }
                            ]
                        }
                    }
                }
            }
        }
        ,
        400: {
            "description": "Bad request. The meta data could not be retrieved. Check the request or try again later.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "Something Went Wrong, Meta not found"
                    }
            }
        }
        }
}

