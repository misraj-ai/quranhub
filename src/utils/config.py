import os
from dotenv import load_dotenv

DEFAULT_EDITION_IDENTIFIER="quran-simple"
TAFSIR_BOOKS_LANGUAGES=["en","id","tr","es","ur"]
TAFSIR_BOOKS_LEVELS={"Tafsir Gharib al-Qur'an Ibn Qatayba":1,"Al Muyassar Fi Al-Ghareeb":1,"Al-Tafsir al-Muyassar al-Mogamaa":2,"Al-Mukhtasar":2,"Tafseer Al-Fatihah for Saleh AL-Osaimi":2,"Tafsir al-Saddi":3,"Tafsir al-Jalalayn":3,"Tafsir al-Baghawi":4,"Tafsir al-Qurtubi":4,"Tafsir al-Tabari":5,"Tafsir Ibn Kathir":5}


WESTERN_ARABIC = '0123456789'
EASTERN_ARABIC = '٠١٢٣٤٥٦٧٨٩'
NUMBERS_TRANSLATION_TABLE = str.maketrans(WESTERN_ARABIC, EASTERN_ARABIC)
QURANIC_SYMBOLS = ["۞", "۩"]
SPECIAL_CHARACTERS=['ۗ', 'ۛ', 'ۖ', 'ۚ', 'ۘ', 'ۜ', 'ۙ']
QURANIC_SYMBOLS_TRANSLATION_TABLE = str.maketrans("", "", "".join(QURANIC_SYMBOLS))

BASIC_TAJWEED_RULES = {
    "ghunnah",
    "idgham_ghunnah",
    "idgham_shafawi",
    "idgham_wo_ghunnah",
    "ikhafa",
    "ikhafa_shafawi",
    "iqlab",
    "izhar",
    "izhar_shafawi",
    "madda_necessary",
    "madda_normal",
    "madda_obligatory_mottasel",
    "madda_permissible",
    "qalaqah",
    "tafkheem",
    "tarqeeq"
}

BUNNY_URL="https://quranhub.b-cdn.net/quran"

# Audio edition types. Only verse-by-verse editions carry per-ayah audio URLs;
# word-by-word editions carry per-word audio URLs instead.
AUDIO_TYPE_VERSEBYVERSE = "versebyverse"
AUDIO_TYPE_SURAH = "surah"
AUDIO_TYPE_WORDBYWORD = "wordbyword"

TOTAL_AYAHS = 6236
TOTAL_WORDS = 77432

# Word locations (surah:ayah:position) with no source audio on Quran.com,
# verified by requesting every file on 2026-10-12. These return audio=null.
WORDBYWORD_MISSING_AUDIO = frozenset({
    "8:66:2", "12:8:15", "18:49:20", "18:54:7", "60:2:7", "79:1:2", "98:7:1",
})

# The quran-hafs text splits "إِلۡ يَاسِينَ" (37:130) into two tokens, but the word
# table and the audio have it as one word, so token 4 plays the word-3 clip.
WORDBYWORD_POSITION_ALIASES = {"37:130:4": "37:130:3"}

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')