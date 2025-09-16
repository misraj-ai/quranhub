import os
from dotenv import load_dotenv

DEFAULT_EDITION_IDENTIFIER="quran-simple"
TAFSIR_BOOKS_LANGUAGES=["en","id","tr","es","ur"]
TAFSIR_BOOKS_LEVELS={"Tafsir Gharib al-Qur'an Ibn Qatayba":1,"Al Muyassar Fi Al-Ghareeb":1,"Al-Tafsir al-Muyassar al-Mogamaa":2,"Al-Mukhtasar":2,"Tafseer Al-Fatihah for Saleh AL-Osaimi":2,"Tafsir al-Saadi":3,"Tafsir al-Jalalayn":3,"Tafsir al-Baghawi":4,"Tafsir al-Qurtubi":4,"Tafsir al-Tabari":5,"Tafsir Ibn Kathir":5}
TAFSIR_BOOKS_TRANSLATION={
    "تفسير ابن كثير":{"en":"Tafsir Ibn Kathir", "id":"Tafsir Ibnu Katsir", "tr":"Tefsir İbn Kesir", "es":"Tafsir Ibn Kathir", "ur":"تفسير ابن كثير"},
    "تفسير الطبري":{"en":"Tafsir al-Tabari", "id":"Tafsir al-Tabari", "tr":"Tefsir Taberi", "es":"Tafsir al-Tabari", "ur":"تفسير الطبري"},
    "تفسير القرطبي":{"en":"Tafsir al-Qurtubi", "id":"Tafsir al-Qurtubi", "tr":"Tefsir el-Kurtubi", "es":"Tafsir al-Qurtubi", "ur":"تفسير القرطبي"},
    "تفسير الجلالين":{"en":"Tafsir al-Jalalayn", "id":"Tafsir al-Jalalayn", "tr":"Tefsir el-Celaleyn", "es":"Tafsir al-Jalalayn", "ur":"تفسير الجلالين"},
    "التفسير الميسر المجمع":{"en":"Al-Tafsir al-Muyassar al-Mogamaa", "id":"Al-Tafsir al-Muyassar al-Mogamaa", "tr":"Al-Tafsir al-Muyassar al-Mogamaa", "es":"Al-Tafsir al-Muyassar al-Mogamaa", "ur":"التفسير الميسر المجمع"},
    "تفسير السعدي":{"en":"Tafsir al-Saadi", "id":"Tafsir al-Saadi", "tr":"Tefsir es-Saadi", "es":"Tafsir al-Saadi", "ur":"تفسير السعدي"},
    "تفسير البغوي":{"en":"Tafsir al-Baghawi", "id":"Tafsir al-Baghawi", "tr":"Tefsir el-Begavi", "es":"Tafsir al-Baghawi", "ur":"تفسير البغوي"},
    "التفسير الوسيط":{"en":"Tafsir al-Waseet", "id":"Tafsir al-Waseet", "tr":"Tefsir el-Vasit", "es":"Tafsir al-Waseet", "ur":"التفسير الوسيط"},
    "تنوير المقباس من تفسير بن عباس":{"en":"Tafsir Ibn Abbas", "id":"Tafsir Ibnu Abbas", "tr":"Tefsir İbn Abbas", "es":"Tafsir Ibn Abbas", "ur":"تنوير المقباس من تفسير بن عباس"},
    "غريب القرآن لابن قتيبة":{"en":"Tafsir Gharib al-Qur'an Ibn Qatayba", "id":"Tafsir Gharib al-Qur'an Ibn Qatayba", "tr":"Tefsir Gharib al-Qur'an İbn Kuteybe", "es":"Tafsir Gharib al-Qur'an Ibn Qatayba", "ur":"غريب القرآن لابن قتيبة"},
    "الميسر في الغريب":{"en":"Al Muyassar Fi Al-Ghareeb", "id":"Al Muyassar Fi Al-Ghareeb", "tr":"Al Muyassar Fi Al-Ghareeb", "es":"Al Muyassar Fi Al-Ghareeb", "ur":"الميسر في الغريب"},
    "المختصر في التفسير":{"en":"Al-Mukhtasar", "id":"Al-Mukhtasar", "tr":"Al-Mukhtasar", "es":"Al-Mukhtasar", "ur":"المختصر في التفسير"},
    "تفسير الفاتحة للشيخ صالح العصيمي":{"en":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "id":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "tr":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "es":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "ur":"تفسير الفاتحة للشيخ صالح العصيمي"},
    "تفسير ابن عاشور":{"en":"Tafsir Ibn Ashur", "id":"Tafsir Ibnu Ashur", "tr":"Tefsir İbn Aşur", "es":"Tafsir Ibn Ashur", "ur":"تفسير ابن عاشور"},
    "مختصر تفسير ابن كثير":{"en":"Summary of Ibn Kathir's Tafsir", "id":"Ringkasan Tafsir Ibnu Katsir", "tr":"İbn Kesir Tefsirinin Özeti", "es":"Resumen del Tafsir de Ibn Kathir", "ur":"مختصر تفسير ابن كثير"},
    "أيسر التفاسير لكلام العلي الكبير":{"en":"Tafsir Abu Bakr Al-Jaza'iry", "id":"Tafsir Abu Bakar Al-Jazairy", "tr":"Tefsir Ebu Bekir el-Cezairi", "es":"Tafsir Abu Bakr Al-Jaza'iry", "ur":"أيسر التفاسير لكلام العلي الكبير"},
    "الدر المنثور في التفسير بالمأثور":{"en":"Tafsir al-Suyuti", "id":"Tafsir al-Suyuti", "tr":"Tefsir es-Suyuti", "es":"Tafsir al-Suyuti", "ur":"الدر المنثور في التفسير بالمأثور"},
    "تفسير فتح القدير للشوكاني":{"en":"Tafsir Fath al-Qadir", "id":"Tafsir Fath al-Qadir", "tr":"Tefsir Feth el-Kadir", "es":"Tafsir Fath al-Qadir", "ur":"تفسير فتح القدير للشوكاني"}
}

WESTERN_ARABIC = '0123456789'
EASTERN_ARABIC = '٠١٢٣٤٥٦٧٨٩'
NUMBERS_TRANSLATION_TABLE = str.maketrans(WESTERN_ARABIC, EASTERN_ARABIC)
QURANIC_SYMBOLS = ["۞", "۩"]
SPECIAL_CHARACTERS=['ۗ', 'ۛ', 'ۖ', 'ۚ', 'ۘ', 'ۜ', 'ۙ']
QURANIC_SYMBOLS_TRANSLATION_TABLE = str.maketrans("", "", "".join(QURANIC_SYMBOLS))

BUNNY_URL="https://quranhub.b-cdn.net/quran"

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')