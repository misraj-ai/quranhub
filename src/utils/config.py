import os
from dotenv import load_dotenv

DEFAULT_EDITION_IDENTIFIER="quran-simple"
TAFSIR_BOOKS_LANGUAGES=["en","id","tr","es","ur"]
TAFSIR_BOOKS_LEVELS={"Tafsir Gharib al-Qur'an Ibn Qatayba":1,"Al Muyassar Fi Al-Ghareeb":1,"Al-Tafsir al-Muyassar al-Mogamaa":2,"Al-Mukhtasar":2,"Tafseer Al-Fatihah for Saleh AL-Osaimi":2,"Tafsir al-Saddi":3,"Tafsir al-Jalalayn":3,"Tafsir al-Baghawi":4,"Tafsir al-Qurtubi":4,"Tafsir al-Tabari":5,"Tafsir Ibn Kathir":5}
TAFSIR_BOOKS_TRANSLATION={
    "تفسير ابن كثير":{"en":"Tafsir Ibn Kathir", "id":"Tafsir Ibnu Katsir", "tr":"Tefsir İbn Kesir", "es":"Tafsir Ibn Kathir", "ur":"تفسير ابن كثير"},
    "تفسير الطبري":{"en":"Tafsir al-Tabari", "id":"Tafsir al-Tabari", "tr":"Tefsir Taberi", "es":"Tafsir al-Tabari", "ur":"تفسير الطبري"},
    "تفسير القرطبي":{"en":"Tafsir al-Qurtubi", "id":"Tafsir al-Qurtubi", "tr":"Tefsir el-Kurtubi", "es":"Tafsir al-Qurtubi", "ur":"تفسير القرطبي"},
    "تفسير الجلالين":{"en":"Jalal ad-Din al-Mahalli and Jalal ad-Din as-Suyuti", "id":"Tafsir al-Jalalayn", "tr":"Tefsir el-Celaleyn", "es":"Tafsir al-Jalalayn", "ur":"تفسير الجلالين"},
    "التفسير الميسر المجمع":{"en":"Al-Tafsir al-Muyassar al-Mogamaa", "id":"Al-Tafsir al-Muyassar al-Mogamaa", "tr":"Al-Tafsir al-Muyassar al-Mogamaa", "es":"Al-Tafsir al-Muyassar al-Mogamaa", "ur":"التفسير الميسر المجمع"},
    "تفسير السعدي":{"en":"Tafsir al-Saddi", "id":"Tafsir al-Saddi", "tr":"Tefsir es-Saddi", "es":"Tafsir al-Saddi", "ur":"تفسير السعدي"},
    "تفسير البغوي":{"en":"Tafsir al-Baghawi", "id":"Tafsir al-Baghawi", "tr":"Tefsir el-Begavi", "es":"Tafsir al-Baghawi", "ur":"تفسير البغوي"},
    "التفسير الوسيط":{"en":"Tafsir al-Wasit", "id":"Tafsir al-Wasit", "tr":"Tefsir el-Vasit", "es":"Tafsir al-Wasit", "ur":"التفسير الوسيط"},
    "تنوير المقباس من تفسير بن عباس":{"en":"Tanwir al-Miqbas min Tafsir ibn Abbas", "id":"Tafsir Ibnu Abbas", "tr":"Tefsir İbn Abbas", "es":"Tafsir Ibn Abbas", "ur":"تنوير المقباس من تفسير بن عباس"},
    "غريب القرآن لابن قتيبة":{"en":"Tafsir Gharib al-Qur'an Ibn Qatayba", "id":"Tafsir Gharib al-Qur'an Ibn Qatayba", "tr":"Tefsir Gharib al-Qur'an İbn Kuteybe", "es":"Tafsir Gharib al-Qur'an Ibn Qatayba", "ur":"غريب القرآن لابن قتيبة"},
    "الميسر في الغريب":{"en":"Al Muyassar Fi Al-Ghareeb", "id":"Al Muyassar Fi Al-Ghareeb", "tr":"Al Muyassar Fi Al-Ghareeb", "es":"Al Muyassar Fi Al-Ghareeb", "ur":"الميسر في الغريب"},
    "المختصر في التفسير":{"en":"Al-Mukhtasar", "id":"Al-Mukhtasar", "tr":"Al-Mukhtasar", "es":"Al-Mukhtasar", "ur":"المختصر في التفسير"},
    "تفسير الفاتحة للشيخ صالح العصيمي":{"en":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "id":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "tr":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "es":"Tafseer Al-Fatihah for Saleh AL-Osaimi", "ur":"تفسير الفاتحة للشيخ صالح العصيمي"},
    "تفسير ابن عاشور":{"en":"Tafsir Ibn Ashur", "id":"Tafsir Ibnu Ashur", "tr":"Tefsir İbn Aşur", "es":"Tafsir Ibn Ashur", "ur":"تفسير ابن عاشور"},
    "مختصر تفسير ابن كثير":{"en":"Summary of Ibn Kathir's Tafsir", "id":"Ringkasan Tafsir Ibnu Katsir", "tr":"İbn Kesir Tefsirinin Özeti", "es":"Resumen del Tafsir de Ibn Kathir", "ur":"مختصر تفسير ابن كثير"},
    "أيسر التفاسير لكلام العلي الكبير":{"en":"Tafsir Abu Bakr Al-Jaza'iry", "id":"Tafsir Abu Bakar Al-Jazairy", "tr":"Tefsir Ebu Bekir el-Cezairi", "es":"Tafsir Abu Bakr Al-Jaza'iry", "ur":"أيسر التفاسير لكلام العلي الكبير"},
    "الدر المنثور في التفسير بالمأثور":{"en":"Tafsir al-Suyuti", "id":"Tafsir al-Suyuti", "tr":"Tefsir es-Suyuti", "es":"Tafsir al-Suyuti", "ur":"الدر المنثور في التفسير بالمأثور"},
    "تفسير فتح القدير للشوكاني":{"en":"Tafsir Fath al-Qadir", "id":"Tafsir Fath al-Qadir", "tr":"Tefsir Feth el-Kadir", "es":"Tafsir Fath al-Qadir", "ur":"تفسير فتح القدير للشوكاني"},
    "أحسن البيان":{"en":"Tafsir Ahsanul Bayaan", "id":"Tafsir Ahsanul Bayaan", "tr":"Tafsir Ahsanul Bayaan", "es":"Tafsir Ahsanul Bayaan", "ur":"أحسن البيان"},
    "أضواء البيان":{"en":"Adwa' Al-Bayan", "id":"Adwa' Al-Bayan", "tr":"Adwa' Al-Bayan", "es":"Adwa' Al-Bayan", "ur":"أضواء البيان"},
    "إعراب القرآن لدعاس":{"en":"Alrab Al-Quran li-Da'as", "id":"Alrab Al-Quran li-Da'as", "tr":"Alrab Al-Quran li-Da'as", "es":"Alrab Al-Quran li-Da'as", "ur":"إعراب القرآن لدعاس"},
    "إعراب القرآن للدرويش":{"en":"I'rab Al Quran li Al Darwish", "id":"I'rab Al Quran li Al Darwish", "tr":"I'rab Al Quran li Al Darwish", "es":"I'rab Al Quran li Al Darwish", "ur":"إعراب القرآن للدرويش"},
    "الإعراب الميسر":{"en":"Iraab Al-Muyassar", "id":"Iraab Al-Muyassar", "tr":"Iraab Al-Muyassar", "es":"Iraab Al-Muyassar", "ur":"الإعراب الميسر"},
    "البحر المحيط":{"en":"Al-Bahr Al-Muhit", "id":"Al-Bahr Al-Muhit", "tr":"Al-Bahr Al-Muhit", "es":"Al-Bahr Al-Muhit", "ur":"البحر المحيط"},
    "البسيط":{"en":"Al-Basit", "id":"Al-Basit", "tr":"Al-Basit", "es":"Al-Basit", "ur":"البسيط"},
    "الجدول في إعراب القرآن":{"en":"Al Jadwal fi I'rab Al Quran", "id":"Al Jadwal fi I'rab Al Quran", "tr":"Al Jadwal fi I'rab Al Quran", "es":"Al Jadwal fi I'rab Al Quran", "ur":"الجدول في إعراب القرآن"},
    "الدر المصون للسمين الحلبي":{"en":"Al Dur Al Masun Lil Samin Al Halabi", "id":"Al Dur Al Masun Lil Samin Al Halabi", "tr":"Al Dur Al Masun Lil Samin Al Halabi", "es":"Al Dur Al Masun Lil Samin Al Halabi", "ur":"الدر المصون للسمين الحلبي"},
    "السراج في بيان غريب القرآن":{"en":"Asseraj fi Bayan Gharib AlQuran", "id":"Asseraj fi Bayan Gharib AlQuran", "tr":"Asseraj fi Bayan Gharib AlQuran", "es":"Asseraj fi Bayan Gharib AlQuran", "ur":"السراج في بيان غريب القرآن"},
    "القراءات الموسوعة القرآنية":{"en":"Al Qira'at Al Mawsoo'ah Al Qur'aniyyah", "id":"Al Qira'at Al Mawsoo'ah Al Qur'aniyyah", "tr":"Al Qira'at Al Mawsoo'ah Al Qur'aniyyah", "es":"Al Qira'at Al Mawsoo'ah Al Qur'aniyyah", "ur":"القراءات الموسوعة القرآنية"},
    "الكشاف للزمخشري":{"en":"Al-Kashshaf Al-Zamakhshari", "id":"Al-Kashshaf Al-Zamakhshari", "tr":"Al-Kashshaf Al-Zamakhshari", "es":"Al-Kashshaf Al-Zamakhshari", "ur":"الكشاف للزمخشري"},
    "اللباب في علوم الكتاب":{"en":"Al Lubab fi Ulum Al Kitab", "id":"Al Lubab fi Ulum Al Kitab", "tr":"Al Lubab fi Ulum Al Kitab", "es":"Al Lubab fi Ulum Al Kitab", "ur":"اللباب في علوم الكتاب"},
    "المحرر الوجيز لابن عطية":{"en":"Al-Muharrar Al-Wajiz Ibn Atiyyah", "id":"Al-Muharrar Al-Wajiz Ibn Atiyyah", "tr":"Al-Muharrar Al-Wajiz Ibn Atiyyah", "es":"Al-Muharrar Al-Wajiz Ibn Atiyyah", "ur":"المحرر الوجيز لابن عطية"},
    "النشر لابن الجزري":{"en":"Al Nashr li Ibn Al Jazari", "id":"Al Nashr li Ibn Al Jazari", "tr":"Al Nashr li Ibn Al Jazari", "es":"Al Nashr li Ibn Al Jazari", "ur":"النشر لابن الجزري"},
    "بيان القرآن":{"en":"Tafsir Bayan ul Quran", "id":"Tafsir Bayan ul Quran", "tr":"Tafsir Bayan ul Quran", "es":"Tafsir Bayan ul Quran", "ur":"بيان القرآن"},
    "تحليل كلمات القرآن":{"en":"Tahlil Kalimat al-Qur'an", "id":"Tahlil Kalimat al-Qur'an", "tr":"Tahlil Kalimat al-Qur'an", "es":"Tahlil Kalimat al-Qur'an", "ur":"تحليل كلمات القرآن"},
    "تدبر وعمل":{"en":"Tadabbur wa 'Amal", "id":"Tadabbur wa 'Amal", "tr":"Tadabbur wa 'Amal", "es":"Tadabbur wa 'Amal", "ur":"تدبر وعمل"},
    "تذكرة القرآن":{"en":"Tazkirul Quran (Maulana Wahiduddin Khan)", "id":"Tazkirul Quran (Maulana Wahiduddin Khan)", "tr":"Tazkirul Quran (Maulana Wahiduddin Khan)", "es":"Tazkirul Quran (Maulana Wahiduddin Khan)", "ur":"تذكرة القرآن"},
    "تفسير أبو بكر زكريا":{"en":"Tafsir Abu Bakr Zakaria", "id":"Tafsir Abu Bakr Zakaria", "tr":"Tafsir Abu Bakr Zakaria", "es":"Tafsir Abu Bakr Zakaria", "ur":"تفسير أبو بكر زكريا"},
    "تفسير أبي السعود":{"en":"Tafsir Abi Al-Suaood", "id":"Tafsir Abi Al-Suaood", "tr":"Tafsir Abi Al-Suaood", "es":"Tafsir Abi Al-Suaood", "ur":"تفسير أبي السعود"},
    "تفسير ابن أبي حاتم":{"en":"Tafsir Ibn Abi Hatim", "id":"Tafsir Ibn Abi Hatim", "tr":"Tafsir Ibn Abi Hatim", "es":"Tafsir Ibn Abi Hatim", "ur":"تفسير ابن أبي حاتم"},
    "تفسير ابن أبي زمنين":{"en":"Tafsir Ibn Abi Zamanin", "id":"Tafsir Ibn Abi Zamanin", "tr":"Tafsir Ibn Abi Zamanin", "es":"Tafsir Ibn Abi Zamanin", "ur":"تفسير ابن أبي زمنين"},
    "تفسير ابن الجوزي":{"en":"Tafsir Ibn Al-Jawzi", "id":"Tafsir Ibn Al-Jawzi", "tr":"Tafsir Ibn Al-Jawzi", "es":"Tafsir Ibn Al-Jawzi", "ur":"تفسير ابن الجوزي"},
    "تفسير ابن جزي":{"en":"Tafsir Ibn Juzay", "id":"Tafsir Ibn Juzay", "tr":"Tafsir Ibn Juzay", "es":"Tafsir Ibn Juzay", "ur":"تفسير ابن جزي"},
    "تفسير الألوسي":{"en":"Tafsir Al-Alusi", "id":"Tafsir Al-Alusi", "tr":"Tafsir Al-Alusi", "es":"Tafsir Al-Alusi", "ur":"تفسير الألوسي"},
    "تفسير الثعالبي":{"en":"Tafsir Al-Tha'alibi", "id":"Tafsir Al-Tha'alibi", "tr":"Tafsir Al-Tha'alibi", "es":"Tafsir Al-Tha'alibi", "ur":"تفسير الثعالبي"},
    "تفسير الرازي":{"en":"Tafsir Al-Razi", "id":"Tafsir Al-Razi", "tr":"Tafsir Al-Razi", "es":"Tafsir Al-Razi", "ur":"تفسير الرازي"},
    "تفسير السمرقندي":{"en":"Tafsir Al-Samarqandi", "id":"Tafsir Al-Samarqandi", "tr":"Tafsir Al-Samarqandi", "es":"Tafsir Al-Samarqandi", "ur":"تفسير السمرقندي"},
    "تفسير السمعاني":{"en":"Tafsir Al-Sam'ani", "id":"Tafsir Al-Sam'ani", "tr":"Tafsir Al-Sam'ani", "es":"Tafsir Al-Sam'ani", "ur":"تفسير السمعاني"},
    "تفسير الماوردي":{"en":"Tafsir Al-Mawardi", "id":"Tafsir Al-Mawardi", "tr":"Tafsir Al-Mawardi", "es":"Tafsir Al-Mawardi", "ur":"تفسير الماوردي"},
    "تفسير المكي":{"en":"Tafsir Makki", "id":"Tafsir Makki", "tr":"Tafsir Makki", "es":"Tafsir Makki", "ur":"تفسير المكي"},
    "تفسير النسفي":{"en":"Tafsir Al-Nasafi", "id":"Tafsir Al-Nasafi", "tr":"Tafsir Al-Nasafi", "es":"Tafsir Al-Nasafi", "ur":"تفسير النسفي"},
    "تفسير رێبهر":{"en":"Rebar Kurdish Tafsir", "id":"Rebar Kurdish Tafsir", "tr":"Rebar Kurdish Tafsir", "es":"Rebar Kurdish Tafsir", "ur":"تفسير رێبهر"},
    "جامع البيان للإيجي":{"en":"Jamia Al-Bayan AlIji", "id":"Jamia Al-Bayan AlIji", "tr":"Jamia Al-Bayan AlIji", "es":"Jamia Al-Bayan AlIji", "ur":"جامع البيان للإيجي"},
    "فتح البيان للقنوجي":{"en":"Fath Al-Bayan li Al-Qanuji", "id":"Fath Al-Bayan li Al-Qanuji", "tr":"Fath Al-Bayan li Al-Qanuji", "es":"Fath Al-Bayan li Al-Qanuji", "ur":"فتح البيان للقنوجي"},
    "فتح المجيد":{"en":"Tafsir Fathul Majid", "id":"Tafsir Fathul Majid", "tr":"Tafsir Fathul Majid", "es":"Tafsir Fathul Majid", "ur":"فتح المجيد"},
    "في ظلال القرآن":{"en":"Fi Zilal al-Quran", "id":"Fi Zilal al-Quran", "tr":"Fi Zilal al-Quran", "es":"Fi Zilal al-Quran", "ur":"في ظلال القرآن"},
    "محاسن التأويل للقاسمي":{"en":"Mahasin Al-Ta'wil Al-Qasimi", "id":"Mahasin Al-Ta'wil Al-Qasimi", "tr":"Mahasin Al-Ta'wil Al-Qasimi", "es":"Mahasin Al-Ta'wil Al-Qasimi", "ur":"محاسن التأويل للقاسمي"},
    "معارف القرآن":{"en":"Maarif-ul-Quran", "id":"Maarif-ul-Quran", "tr":"Maarif-ul-Quran", "es":"Maarif-ul-Quran", "ur":"معارف القرآن"},
    "موسوعة التفسير المأثور":{"en":"Mawsoo'at Al-Tafsir Al-Ma'thoor", "id":"Mawsoo'at Al-Tafsir Al-Ma'thoor", "tr":"Mawsoo'at Al-Tafsir Al-Ma'thoor", "es":"Mawsoo'at Al-Tafsir Al-Ma'thoor", "ur":"موسوعة التفسير المأثور"},
    "نظم الدرر للبقاعي":{"en":"Nazam Al-Durar Al-Biqa'i", "id":"Nazam Al-Durar Al-Biqa'i", "tr":"Nazam Al-Durar Al-Biqa'i", "es":"Nazam Al-Durar Al-Biqa'i", "ur":"نظم الدرر للبقاعي"}
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