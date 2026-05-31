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

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')