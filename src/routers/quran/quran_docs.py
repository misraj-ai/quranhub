
getTheQuranResponse={
        200: {
            "description": "Returns the complete Quran in the default edition. Use this to retrieve all surahs and ayahs for display, analysis, or further processing. The response includes all Quranic text and metadata.",
            "content": {
                "application/json": {
                "example":    {
                        "surahs": [
                    {
                        "number": 1,
                        "name": "سورة الفاتحة",
                        "englishName": "Al-Faatiha",
                        "englishNameTranslation": "The Opening",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 7,
                        "ayahs": [
                        {
                            "number": 1,
                            "text": "﻿بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
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
                            "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
                            "numberInSurah": 2,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 3,
                            "text": "الرَّحْمَٰنِ الرَّحِيمِ",
                            "numberInSurah": 3,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 4,
                            "text": "مَالِكِ يَوْمِ الدِّينِ",
                            "numberInSurah": 4,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 5,
                            "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
                            "numberInSurah": 5,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 6,
                            "text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
                            "numberInSurah": 6,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 7,
                            "text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
                            "numberInSurah": 7,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        }
                        ]
                    },
                    {
                        "number": 2,
                        "name": "سورة البقرة",
                        "englishName": "Al-Baqara",
                        "englishNameTranslation": "The Cow",
                        "revelationType": "Medinan",
                        "numberOfAyahs": 286,
                        "ayahs": [
                        {
                            "number": 8,
                            "text": "الم",
                            "numberInSurah": 1,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 9,
                            "text": "ذَٰلِكَ الْكِتَابُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًى لِلْمُتَّقِينَ",
                            "numberInSurah": 2,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 10,
                            "text": "الَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ وَيُقِيمُونَ الصَّلَاةَ وَمِمَّا رَزَقْنَاهُمْ يُنْفِقُونَ",
                            "numberInSurah": 3,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 11,
                            "text": "وَالَّذِينَ يُؤْمِنُونَ بِمَا أُنْزِلَ إِلَيْكَ وَمَا أُنْزِلَ مِنْ قَبْلِكَ وَبِالْآخِرَةِ هُمْ يُوقِنُونَ",
                            "numberInSurah": 4,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 12,
                            "text": "أُولَٰئِكَ عَلَىٰ هُدًى مِنْ رَبِّهِمْ ۖ وَأُولَٰئِكَ هُمُ الْمُفْلِحُونَ",
                            "numberInSurah": 5,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 13,
                            "text": "إِنَّ الَّذِينَ كَفَرُوا سَوَاءٌ عَلَيْهِمْ أَأَنْذَرْتَهُمْ أَمْ لَمْ تُنْذِرْهُمْ لَا يُؤْمِنُونَ",
                            "numberInSurah": 6,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 14,
                            "text": "خَتَمَ اللَّهُ عَلَىٰ قُلُوبِهِمْ وَعَلَىٰ سَمْعِهِمْ ۖ وَعَلَىٰ أَبْصَارِهِمْ غِشَاوَةٌ ۖ وَلَهُمْ عَذَابٌ عَظِيمٌ",
                            "numberInSurah": 7,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 15,
                            "text": "وَمِنَ النَّاسِ مَنْ يَقُولُ آمَنَّا بِاللَّهِ وَبِالْيَوْمِ الْآخِرِ وَمَا هُمْ بِمُؤْمِنِينَ",
                            "numberInSurah": 8,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 16,
                            "text": "يُخَادِعُونَ اللَّهَ وَالَّذِينَ آمَنُوا وَمَا يَخْدَعُونَ إِلَّا أَنْفُسَهُمْ وَمَا يَشْعُرُونَ",
                            "numberInSurah": 9,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 17,
                            "text": "فِي قُلُوبِهِمْ مَرَضٌ فَزَادَهُمُ اللَّهُ مَرَضًا ۖ وَلَهُمْ عَذَابٌ أَلِيمٌ بِمَا كَانُوا يَكْذِبُونَ",
                            "numberInSurah": 10,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 18,
                            "text": "وَإِذَا قِيلَ لَهُمْ لَا تُفْسِدُوا فِي الْأَرْضِ قَالُوا إِنَّمَا نَحْنُ مُصْلِحُونَ",
                            "numberInSurah": 11,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 19,
                            "text": "أَلَا إِنَّهُمْ هُمُ الْمُفْسِدُونَ وَلَٰكِنْ لَا يَشْعُرُونَ",
                            "numberInSurah": 12,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 20,
                            "text": "وَإِذَا قِيلَ لَهُمْ آمِنُوا كَمَا آمَنَ النَّاسُ قَالُوا أَنُؤْمِنُ كَمَا آمَنَ السُّفَهَاءُ ۗ أَلَا إِنَّهُمْ هُمُ السُّفَهَاءُ وَلَٰكِنْ لَا يَعْلَمُونَ",
                            "numberInSurah": 13,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 21,
                            "text": "وَإِذَا لَقُوا الَّذِينَ آمَنُوا قَالُوا آمَنَّا وَإِذَا خَلَوْا إِلَىٰ شَيَاطِينِهِمْ قَالُوا إِنَّا مَعَكُمْ إِنَّمَا نَحْنُ مُسْتَهْزِئُونَ",
                            "numberInSurah": 14,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        }
                        ]
                    }
                        ]
                }
                        
                
            }
        }
        }
        ,
        400: {
            "description": "Bad request. The Quran could not be retrieved. Check the request or try again later.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "Something wrong happened: Data not found"
                    }
            }
        }
        }
}

getTheQuranbyEditionResponse={
        200: {
            "description": "Returns the complete Quran for a specified edition. Use this to retrieve all surahs and ayahs in a particular text or translation edition. The response includes all Quranic text and metadata for the chosen edition.",
            "content": {
                "application/json": {
                "example":    {
                    "surahs": [
                    {
                        "number": 1,
                        "name": "سورة الفاتحة",
                        "englishName": "Al-Faatiha",
                        "englishNameTranslation": "The Opening",
                        "revelationType": "Meccan",
                        "numberOfAyahs": 7,
                        "ayahs": [
                        {
                            "number": 1,
                            "text": "﻿بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
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
                            "text": "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ",
                            "numberInSurah": 2,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 3,
                            "text": "ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
                            "numberInSurah": 3,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 4,
                            "text": "مَٰلِكِ يَوْمِ ٱلدِّينِ",
                            "numberInSurah": 4,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 5,
                            "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
                            "numberInSurah": 5,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 6,
                            "text": "ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ",
                            "numberInSurah": 6,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 7,
                            "text": "صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ",
                            "numberInSurah": 7,
                            "juz": 1,
                            "manzil": 1,
                            "page": 1,
                            "ruku": 1,
                            "hizbQuarter": 1,
                            "sajda": False
                        }
                        ]
                    },
                    {
                        "number": 2,
                        "name": "سورة البقرة",
                        "englishName": "Al-Baqara",
                        "englishNameTranslation": "The Cow",
                        "revelationType": "Medinan",
                        "numberOfAyahs": 286,
                        "ayahs": [
                        {
                            "number": 8,
                            "text": "الٓمٓ",
                            "numberInSurah": 1,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 9,
                            "text": "ذَٰلِكَ ٱلْكِتَٰبُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًۭى لِّلْمُتَّقِينَ",
                            "numberInSurah": 2,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 10,
                            "text": "ٱلَّذِينَ يُؤْمِنُونَ بِٱلْغَيْبِ وَيُقِيمُونَ ٱلصَّلَوٰةَ وَمِمَّا رَزَقْنَٰهُمْ يُنفِقُونَ",
                            "numberInSurah": 3,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 11,
                            "text": "وَٱلَّذِينَ يُؤْمِنُونَ بِمَآ أُنزِلَ إِلَيْكَ وَمَآ أُنزِلَ مِن قَبْلِكَ وَبِٱلْءَاخِرَةِ هُمْ يُوقِنُونَ",
                            "numberInSurah": 4,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 12,
                            "text": "أُو۟لَٰٓئِكَ عَلَىٰ هُدًۭى مِّن رَّبِّهِمْ ۖ وَأُو۟لَٰٓئِكَ هُمُ ٱلْمُفْلِحُونَ",
                            "numberInSurah": 5,
                            "juz": 1,
                            "manzil": 1,
                            "page": 2,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 13,
                            "text": "إِنَّ ٱلَّذِينَ كَفَرُوا۟ سَوَآءٌ عَلَيْهِمْ ءَأَنذَرْتَهُمْ أَمْ لَمْ تُنذِرْهُمْ لَا يُؤْمِنُونَ",
                            "numberInSurah": 6,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 14,
                            "text": "خَتَمَ ٱللَّهُ عَلَىٰ قُلُوبِهِمْ وَعَلَىٰ سَمْعِهِمْ ۖ وَعَلَىٰٓ أَبْصَٰرِهِمْ غِشَٰوَةٌۭ ۖ وَلَهُمْ عَذَابٌ عَظِيمٌۭ",
                            "numberInSurah": 7,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 2,
                            "hizbQuarter": 1,
                            "sajda": False
                        },
                        {
                            "number": 15,
                            "text": "وَمِنَ ٱلنَّاسِ مَن يَقُولُ ءَامَنَّا بِٱللَّهِ وَبِٱلْيَوْمِ ٱلْءَاخِرِ وَمَا هُم بِمُؤْمِنِينَ",
                            "numberInSurah": 8,
                            "juz": 1,
                            "manzil": 1,
                            "page": 3,
                            "ruku": 3,
                            "hizbQuarter": 1,
                            "sajda": False
                        }
                        ]
                    }
                        ]
                            }
                                        
                                
                            }
        }
        }
        ,
        400: {
            "description": "Bad request. The Quran for the specified edition could not be retrieved. Check the edition identifier or try again later.",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "status": "Error",
                        "data": "Something wrong happened: Data not found"
                    }
            }
        }
        }
}