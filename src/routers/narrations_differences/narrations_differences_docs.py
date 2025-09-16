# Enhanced Narrations Differences API Documentation
# Updated examples with real CDN URLs and reciter descriptions

getNarrationsDifferencesByPageResponse = {
    200: {
        "description": "Returns a comprehensive comparison of different Quranic narrations (Hafs, Warsh, Qaloon, etc.) for a given page, showing textual differences with precise word-level positioning, audio recitation URLs, and detailed scholarly commentary. Supports automatic ayah number conversion between narration systems. Useful for advanced study, LLMs, and agent workflows.",
        "content": {
            "application/json": {
                "examples": {
                    "complete_narrations_differences": {
                        "summary": "Complete Narrations Differences with Real Audio URLs",
                        "value": {
                            "code": 200,
                            "status": "OK",
                            "data": {
                                "page": 1,
                                "total_pages": 604,
                                "ayah_count": 7,
                                "differences_count": 12,
                                "surahs": [
                                    {
                                        "number": 1,
                                        "name": "سورة الفاتحة",
                                        "englishName": "Al-Faatiha",
                                        "englishNameTranslation": "The Opening",
                                        "revelationType": "Meccan",
                                        "numberOfAyahs": 7,
                                        "revelationOrder": 5
                                    }
                                ],
                                "differences": [
                                    {
                                        "words": [
                                            {
                                                "text": "مالك",
                                                "location": "1:4:1",
                                                "audio": {
                                                    "url": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdullahbasfar.hafs/4.mp3",
                                                    "reader_name": "عبد الله بصفر - رواية حفص",
                                                    "reader_description": {
                                                        "ar": "عبد الله بصفر: قارئ سعودي بارز وأستاذ مشارك في جامعة الملك عبد العزيز بجدة. الأمين العام السابق للهيئة العالمية للكتاب والسنة، معروف بصوته العذب وإسهاماته العلمية.",
                                                        "en": "Abdullah Basfar: Prominent Saudi reciter and associate professor at King Abdulaziz University in Jeddah. Former Secretary-General of the World Book and Sunnah Organization, known for his melodious voice and scholarly contributions."
                                                    },
                                                    "reader_image": "https://quranhub.b-cdn.net/quran/images/reciters/abdullah-basfar.jpeg"
                                                }
                                            }
                                        ],
                                        "narrator_name": "حفص عن عاصم",
                                        "difference_text": "في قوله تعالى { مالك }",
                                        "difference_content": "قرأ (مَالِكِ) بالألف بين الميم واللام، وهي القراءة المشهورة في رواية حفص."
                                    },
                                    {
                                        "words": [
                                            {
                                                "text": "ملك",
                                                "location": "1:4:1",
                                                "audio": {
                                                    "url": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdulsamad.warsh/4.mp3",
                                                    "reader_name": "عبد الباسط عبد الصمد - رواية ورش",
                                                    "reader_description": {
                                                        "ar": "عبد الباسط عبد الصمد (1927-1988): قارئ مصري شهير حفظ القرآن في سن التاسعة. معروف بصوته الجميل وتلاوته المؤثرة، وله تسجيلات مشهورة للقرآن الكريم في عدة روايات.",
                                                        "en": "Abdul Basit Abdul Samad (1927-1988): Famous Egyptian reciter who memorized the Quran at age nine. Known for his beautiful voice and emotional recitation, he has famous recordings of the Quran in multiple narrations."
                                                    },
                                                    "reader_image": "https://quranhub.b-cdn.net/quran/images/reciters/abdul-basit-abdul-samad.jpeg"
                                                }
                                            }
                                        ],
                                        "narrator_name": "ورش عن نافع",
                                        "difference_text": "في قوله تعالى { ملك }",
                                        "difference_content": "قرأ (مَـلِـكِ) بحذف الألف بين الميم واللام، وهي القراءة المشهورة في رواية ورش."
                                    },
                                    {
                                        "words": [
                                            {
                                                "text": "الصراط",
                                                "location": "1:6:2",
                                                "audio": {
                                                    "url": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdulkarimaldaghush.warsh/6.mp3",
                                                    "reader_name": "عبد الكريم الدغوش - رواية ورش",
                                                    "reader_description": {
                                                        "ar": "عبد الكريم الدغوش: قارئ مغربي متميز متخصص في رواية ورش عن نافع، معروف بالتزامه الدقيق بأسلوب التلاوة المغربي التقليدي وتسجيلاته عالية الجودة للقرآن الكريم.",
                                                        "en": "Abdul Karim Al-Daghoush: Distinguished Moroccan reciter specializing in the Warsh narration from Nafi', known for his precise adherence to traditional Moroccan recitation style and high-quality Quran recordings."
                                                    },
                                                    "reader_image": "https://quranhub.b-cdn.net/quran/images/reciters/abdul-karim-al-daghoush.jpeg"
                                                }
                                            }
                                        ],
                                        "narrator_name": "ورش عن نافع",
                                        "difference_text": "في قوله تعالى { الصراط }",
                                        "difference_content": "يقرأ الصراط بالصاد مع ترقيق الراء في بعض المواضع حسب الأصول المغربية."
                                    },
                                    {
                                        "words": [
                                            {
                                                "text": "صراط",
                                                "location": "1:7:1",
                                                "audio": {
                                                    "url": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.maheralmuaiqly.hafs/7.mp3",
                                                    "reader_name": "ماهر المعيقلي - رواية حفص",
                                                    "reader_description": {
                                                        "ar": "ماهر المعيقلي (مواليد 1969): إمام المسجد الحرام بمكة المكرمة، وُلد في المدينة المنورة. حاصل على دكتوراه في التفسير والفقه من جامعة أم القرى. معروف بتلاوته المؤثرة، أمّ المصلين في الحرمين منذ 1984.",
                                                        "en": "Maher Al Muaiqly (b. 1969): Imam of the Grand Mosque in Makkah, born in Madinah. Holds PhDs in Tafsir and Fiqh from Umm al-Qura University. Known for his emotional recitation style, he has led prayers at both Haramain since 1984."
                                                    },
                                                    "reader_image": "https://quranhub.b-cdn.net/quran/images/reciters/maher-al-muaiqly.jpeg"
                                                }
                                            }
                                        ],
                                        "narrator_name": "حفص عن عاصم",
                                        "difference_text": "في قوله تعالى { صراط }",
                                        "difference_content": "يقرأ صراط بتفخيم الراء والصاد حسب أصول رواية حفص."
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
        "description": "Bad Request - Invalid page number or other parameters",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_page": {
                        "summary": "Invalid Page Number",
                        "value": {
                            "code": 400,
                            "status": "Error",
                            "data": "Page number must be between 1 and 604"
                        }
                    }
                }
            }
        }
    }
}
