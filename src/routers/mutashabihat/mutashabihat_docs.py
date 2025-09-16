
APPLICATION_JSON = "application/json"

getMutashabihatPhrasesResponse = {
	200: {
		"description": "Returns a list of mutashabihat ayah objects, each with canonical ayah and surah metadata, plus startPos, endPos, phraseText, and audio fields if edition is audio.",
		"content": {
			APPLICATION_JSON: {
				"examples": {
					"success": {
						"summary": "Canonical success response",
						"value": [
							{
								"number": 30,
								"text": "وإن كنتم في ريب مما نزلنا على عبدنا فأتوا بسورة من مثله وادعوا شهداءكم من دون الله إن كنتم صادقين",
								"numberInSurah": 23,
								"juz": 1,
								"manzil": 1,
								"page": 5,
								"ruku": 1,
								"hizbQuarter": 1,
								"sajda": False,
								"surah": {
									"number": 2,
									"name": "سورة البقرة",
									"englishName": "Al-Baqarah",
									"englishNameTranslation": "The Cow",
									"revelationType": "Medinan",
									"numberOfAyahs": 286
								},
								"startPos": 15,
								"endPos": 17,
								"phraseText": "مِّن دُونِ ٱللَّهِ",
															"audio": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdulsamad.warsh/30.mp3",
															"audioSecondary": [
																"https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.husary.hafs/30.mp3"
															]
							},
							{
								"number": 3357,
								"text": "إِنَّمَا تَعْبُدُونَ مِنْ دُونِ اللَّهِ أَوْثَانًا ...",
								"numberInSurah": 17,
								"juz": 20,
								"manzil": 5,
								"page": 398,
								"ruku": 343,
								"hizbQuarter": 159,
								"sajda": False,
								"surah": {
									"number": 29,
									"name": "سورة العنكبوت",
									"englishName": "Al-Ankaboot",
									"englishNameTranslation": "The Spider",
									"revelationType": "Meccan",
									"numberOfAyahs": 69
								},
								"startPos": 15,
								"endPos": 17,
								"phraseText": "مِّن دُونِ ٱللَّهِ",
															"audio": "https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.abdulsamad.warsh/3357.mp3",
															"audioSecondary": [
																"https://quranhub.b-cdn.net/quran/audio/versebyverse/128/ar.husary.hafs/3357.mp3"
															]
							}
						]
					},
					"empty": {
						"summary": "No mutashabihat found",
						"value": []
					}
				}
			}
		}
	},
	400: {
		"description": "Bad Request - Invalid surah or ayah number",
		"content": {
			APPLICATION_JSON: {
				"examples": {
					"invalid_surah": {
						"summary": "Invalid Surah Number",
						"value": {"code": 400, "status": "Error", "data": "Surah number must be between 1 and 114"}
					},
					"invalid_ayah": {
						"summary": "Invalid Ayah Number",
						"value": {"code": 400, "status": "Error", "data": "Invalid ayah number for this surah"}
					}
				}
			}
		}
	},
	404: {
		"description": "No mutashabihat phrases found for the given parameters or ayah does not exist in this narration.",
		"content": {
			APPLICATION_JSON: {
				"examples": {
					"not_found": {
						"summary": "No mutashabihat found",
						"value": {"code": 404, "status": "Not Found", "data": "No mutashabihat phrases found for the given parameters or ayah does not exist in this narration."}
					}
				}
			}
		}
	}
}
