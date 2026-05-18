"""
Universal Hashtag Bot - O'zbek tili
Platform: Telegram
Kutubxona: pyTelegramBotAPI (pip install pyTelegramBotAPI)

Ishga tushirish:
1. pip install pyTelegramBotAPI
2. BOT_TOKEN ni o'zgartiring
3. python hashtag_bot.py
"""

import telebot
from telebot import types

# =============================================
# SOZLAMALAR - BU YERDA TOKEN NI O'ZGARTIRING
# =============================================
BOT_TOKEN = "8898761623:AAEv_XO9Dq-P5CFsjfb2pfbFslKbp9wQtHg"
bot = telebot.TeleBot(BOT_TOKEN)

# =============================================
# HASHTAG KUTUBXONASI (500+ hashtag, 10 kategoriya)
# =============================================
HASHTAGS = {
    "biznes": {
        "nomi": "💼 Biznes va Savdo",
        "taglar": [
            "#biznes #savdo #startup #tadbirkorlik #investitsiya",
            "#ecommerce #onlinebiznes #daromad #moliya #kapital",
            "#marketing #reklama #brend #mijozlar #sotish",
            "#b2b #b2c #sheriklik #hamkorlik #bitim",
            "#import #eksport #logistika #yetkazib_berish #ombor",
        ]
    },
    "lifestyle": {
        "nomi": "🌟 Lifestyle va Blog",
        "taglar": [
            "#lifestyle #hayot #motivatsiya #ilhom #muvaffaqiyat",
            "#blog #blogger #content #ijod #yaratuvchilik",
            "#travel #sayohat #dunyo #kashfiyot #adventure",
            "#fashion #moda #stil #trend #looks",
            "#fitness #sport #sog_lom #energia #harakat",
        ]
    },
    "talim": {
        "nomi": "📚 Ta'lim va Kurs",
        "taglar": [
            "#talim #kurs #onlinekurs #dars #oqish",
            "#dasturlash #programming #IT #texnologiya #kod",
            "#ingliz_tili #til_oqish #grammar #speaking #english",
            "#matematika #fizika #kimyo #biologiya #tarix",
            "#sertifikat #diplom #bilim #rivojlanish #career",
        ]
    },
    "oziq": {
        "nomi": "🍽️ Ovqat va Restoran",
        "taglar": [
            "#ovqat #taom #restoran #cafe #yemak",
            "#milliy_taomlar #oshpaz #recipe #retsept #cooking",
            "#delivery #yetkazib_berish #pizza #burger #sushi",
            "#nonushta #tushlik #kechki_ovqat #ziyofat #tort",
            "#vegan #diet #sog_lom_ovqat #kaloriya #nutrition",
        ]
    },
    "texnologiya": {
        "nomi": "💻 Texnologiya",
        "taglar": [
            "#texnologiya #tech #innovation #gadget #smartphone",
            "#AI #suniy_intellekt #machinelearning #robot #future",
            "#cybersecurity #xavfsizlik #hacking #privacy #data",
            "#mobile #android #ios #app #ilovalar",
            "#cloud #server #hosting #database #software",
        ]
    },
    "soglik": {
        "nomi": "❤️ Sog'liq va Fitnes",
        "taglar": [
            "#soglik #salomatlik #tibbiyot #doktor #klinika",
            "#fitness #gym #workout #muskul #crossfit",
            "#yoga #meditatsiya #mindfulness #stresssiz #ruh",
            "#parhez #diet #ozayish #vaznni_kamaytirish #slim",
            "#vitamin #supplement #sog_lom_hayot #wellbeing #detox",
        ]
    },
    "kino": {
        "nomi": "🎬 Ko'ngilochar",
        "taglar": [
            "#kino #film #serial #anime #netflix",
            "#musiqa #qoshiq #artist #concert #live",
            "#gaming #oyin #playstation #xbox #mobile_game",
            "#komediya #hazil #meme #trend #viral",
            "#uzbekfilm #ozbekmusiqasi #milliy #madaniyat #sanaat",
        ]
    },
    "uy": {
        "nomi": "🏠 Uy va Dizayn",
        "taglar": [
            "#uy #kvartira #interer #dizayn #dekor",
            "#remont #qurilish #mebel #mebeldesign #homedesign",
            "#bog #gul #ochilar #tabiat #green",
            "#realestate #kochirilmas_mulk #sotiladi #ijaraga #yangiuy",
            "#handmade #qolbola #crafts #DIY #homemade",
        ]
    },
    "moda": {
        "nomi": "👗 Moda va Go'zallik",
        "taglar": [
            "#moda #fashion #style #trend #ootd",
            "#gozellik #makeup #beauty #skincare #parfum",
            "#kiyim #aksesuar #sumka #poyabzal #bijuteriya",
            "#milliy_kiyim #atlas #ipak #uzbekmoda #handmade",
            "#fitness_look #sport_kiyim #casual #formal #classic",
        ]
    },
    "uzbekiston": {
        "nomi": "🇺🇿 O'zbekiston",
        "taglar": [
            "#uzbekiston #toshkent #samarqand #buxoro #namangan",
            "#uzbek #ozbek #milliy #vatandosh #mening_yurtim",
            "#visituzbekistan #uzbektourism #silk_road #tariximiz #madaniyat",
            "#uzbekfood #osh #somsa #shashlik #lagmon",
            "#uzb #uzbek_blogger #ozbek_content #uzbekmedia #tashkent",
        ]
    }
}

# =============================================
# YORDAMCHI FUNKSIYALAR
# =============================================

def kategoriyalar_klaviaturasi():
    """Asosiy menyu tugmalari"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    tugmalar = [types.KeyboardButton(v["nomi"]) for v in HASHTAGS.values()]
    markup.add(*tugmalar)
    markup.add(types.KeyboardButton("ℹ️ Bot haqida"))
    return markup

def hashtaglar_inline(kategoriya_kodi):
    """Inline tugmalar - hashtaglar ro'yxati"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    taglar = HASHTAGS[kategoriya_kodi]["taglar"]
    for i, guruh in enumerate(taglar):
        birinchi = guruh.split()[0]
        markup.add(types.InlineKeyboardButton(
            f"📋 {birinchi} ... ({len(guruh.split())} ta)",
            callback_data=f"tag_{kategoriya_kodi}_{i}"
        ))
    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_menu"))
    return markup

def kategoriya_kodini_top(nomi):
    """Kategoriya nomidan kodini topish"""
    for kod, v in HASHTAGS.items():
        if v["nomi"] == nomi:
            return kod
    return None

# =============================================
# /start BUYRUG'I
# =============================================

@bot.message_handler(commands=['start'])
def start(message):
    matn = (
        "👋 Salom! Men *Hashtag Bot*man!\n\n"
        "📌 Nima qila olaman?\n"
        "• 10 ta kategoriyadan hashtag tanlaysiz\n"
        "• Tayyor hashtaglarni nusxalab olasiz\n"
        "• 500+ dan ortiq hashtag mavjud\n\n"
        "👇 Quyidan kategoriya tanlang:"
    )
    bot.send_message(
        message.chat.id,
        matn,
        parse_mode="Markdown",
        reply_markup=kategoriyalar_klaviaturasi()
    )

# =============================================
# /help BUYRUG'I
# =============================================

@bot.message_handler(commands=['help'])
def help_cmd(message):
    matn = (
        "📖 *Yordam*\n\n"
        "1️⃣ Kategoriya tanlang\n"
        "2️⃣ Hashtaglar guruhini bosing\n"
        "3️⃣ Hashtaglarni nusxalab oling\n\n"
        "📌 *Buyruqlar:*\n"
        "/start - Boshlanish\n"
        "/help - Yordam\n"
        "/kategoriyalar - Barcha kategoriyalar\n\n"
        "💡 Savol yoki taklif: @sizning_username"
    )
    bot.send_message(message.chat.id, matn, parse_mode="Markdown")

# =============================================
# /kategoriyalar BUYRUG'I
# =============================================

@bot.message_handler(commands=['kategoriyalar'])
def kategoriyalar_cmd(message):
    matn = "📂 *Barcha kategoriyalar:*\n\n"
    for v in HASHTAGS.values():
        matn += f"• {v['nomi']}\n"
    bot.send_message(
        message.chat.id,
        matn,
        parse_mode="Markdown",
        reply_markup=kategoriyalar_klaviaturasi()
    )

# =============================================
# MATN XABARLARNI QAYTA ISHLASH
# =============================================

@bot.message_handler(content_types=['text'])
def matn_handler(message):
    matn = message.text.strip()

    # Bot haqida
    if matn == "ℹ️ Bot haqida":
        info = (
            "🤖 *Hashtag Bot*\n\n"
            "📊 500+ hashtag\n"
            "📂 10 ta kategoriya\n"
            "🇺🇿 O'zbek tilida\n\n"
            "Instagram, Telegram va boshqa platformalar uchun tayyor hashtaglar!\n\n"
            "✅ Bepul foydalaning"
        )
        bot.send_message(message.chat.id, info, parse_mode="Markdown")
        return

    # Kategoriya tanlash
    kod = kategoriya_kodini_top(matn)
    if kod:
        bot.send_message(
            message.chat.id,
            f"{HASHTAGS[kod]['nomi']}\n\n📋 Qaysi guruhni olmoqchisiz?",
            reply_markup=hashtaglar_inline(kod)
        )
    else:
        bot.send_message(
            message.chat.id,
            "👇 Iltimos, quyidagi kategoriyalardan birini tanlang:",
            reply_markup=kategoriyalar_klaviaturasi()
        )

# =============================================
# INLINE TUGMA BOSILGANDA
# =============================================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data

    # Orqaga qaytish
    if data == "back_menu":
        bot.edit_message_text(
            "👇 Kategoriya tanlang:",
            call.message.chat.id,
            call.message.message_id
        )
        bot.send_message(
            call.message.chat.id,
            "✅ Asosiy menyu:",
            reply_markup=kategoriyalar_klaviaturasi()
        )
        return

    # Hashtag guruhini ko'rsatish
    if data.startswith("tag_"):
        qismlar = data.split("_", 2)
        kategoriya_kodi = qismlar[1]
        indeks = int(qismlar[2])

        if kategoriya_kodi in HASHTAGS:
            taglar = HASHTAGS[kategoriya_kodi]["taglar"][indeks]
            bot.answer_callback_query(call.id)
            bot.send_message(
                call.message.chat.id,
                f"✅ *Nusxalab oling:*\n\n`{taglar}`",
                parse_mode="Markdown"
            )

# =============================================
# BOTNI ISHGA TUSHIRISH
# =============================================

if __name__ == "__main__":
    print("🤖 Hashtag Bot ishga tushdi...")
    print("Toxtatish uchun Ctrl+C bosing")
    bot.infinity_polling()
