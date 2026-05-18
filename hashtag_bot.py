"""
Universal Hashtag Bot - O'zbek tili
Platform: Telegram
Kutubxona: pyTelegramBotAPI (pip install pyTelegramBotAPI)
"""

import telebot
from telebot import types

BOT_TOKEN = "8898761623:AAEv_XO9Dq-P5CFsjfb2pfbFslKbp9wQtHg"
KANAL = "@instaheshteg_uz"
ADMIN_ID = 6391668377

bot = telebot.TeleBot(BOT_TOKEN)
USERS = set()

# =============================================
# HASHTAG KUTUBXONASI
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

def obuna_tekshir(user_id):
    try:
        obuna = bot.get_chat_member(KANAL, user_id)
        return obuna.status in ["member", "administrator", "creator"]
    except:
        return False

def obuna_xabari(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Kanalga obuna bo'lish", url=f"https://t.me/{KANAL[1:]}"))
    markup.add(types.InlineKeyboardButton("🔄 Tekshirish", callback_data="obuna_tekshir"))
    bot.send_message(
        chat_id,
        "❗ Botdan foydalanish uchun avval kanalga obuna bo'ling:\n\n"
        f"👉 {KANAL}\n\n"
        "Obuna bo'lgach '🔄 Tekshirish' tugmasini bosing.",
        reply_markup=markup
    )

def kategoriyalar_klaviaturasi(user_id=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    tugmalar = [types.KeyboardButton(v["nomi"]) for v in HASHTAGS.values()]
    markup.add(*tugmalar)
    markup.add(types.KeyboardButton("ℹ️ Bot haqida"))
    if user_id and user_id == ADMIN_ID:
        markup.add(types.KeyboardButton("📢 Xabar yuborish"))
        markup.add(types.KeyboardButton("👥 Foydalanuvchilar soni"))
    return markup

def hashtaglar_inline(kategoriya_kodi):
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
    for kod, v in HASHTAGS.items():
        if v["nomi"] == nomi:
            return kod
    return None

# =============================================
# /start
# =============================================

@bot.message_handler(commands=['start'])
def start(message):
    USERS.add(message.from_user.id)

    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    matn = (
        "👋 Salom! Men *Hashtag Bot*man!\n"
        "👨‍💼 Bot egasi: Jumanazarov Behruz\n\n"
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
        reply_markup=kategoriyalar_klaviaturasi(message.from_user.id)
    )

# =============================================
# /habar - ADMIN UCHUN BROADCAST
# =============================================

@bot.message_handler(commands=['habar'])
def habar_yuborish(message):
    if message.from_user.id != ADMIN_ID:
        return

    matn = message.text.replace('/habar', '').strip()
    if not matn:
        bot.send_message(message.chat.id, "❗ Xabar yozing:\n/habar Salom hammaga!")
        return

    bot.send_message(message.chat.id, f"⏳ {len(USERS)} ta foydalanuvchiga yuborilmoqda...")

    muvaffaq = 0
    xato = 0

    for user_id in USERS:
        try:
            bot.send_message(user_id, f"📢 *Xabar:*\n\n{matn}", parse_mode="Markdown")
            muvaffaq += 1
        except:
            xato += 1

    bot.send_message(message.chat.id, f"✅ Yuborildi: {muvaffaq} ta\n❌ Xato: {xato} ta")

# =============================================
# /help
# =============================================

@bot.message_handler(commands=['help'])
def help_cmd(message):
    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    matn = (
        "📖 *Yordam*\n\n"
        "1️⃣ Kategoriya tanlang\n"
        "2️⃣ Hashtaglar guruhini bosing\n"
        "3️⃣ Hashtaglarni nusxalab oling\n\n"
        "📌 *Buyruqlar:*\n"
        "/start - Boshlanish\n"
        "/help - Yordam\n"
    )
    bot.send_message(message.chat.id, matn, parse_mode="Markdown")

# =============================================
# MATN XABARLAR
# =============================================

@bot.message_handler(content_types=['text'])
def matn_handler(message):
    USERS.add(message.from_user.id)

    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    matn = message.text.strip()

    if message.from_user.id == ADMIN_ID:
        if matn == "📢 Xabar yuborish":
            bot.send_message(
                message.chat.id,
                "✍️ Xabarni yozing:\n/habar Salom hammaga!\n\nBarcha foydalanuvchilarga yuboriladi."
            )
            return
        if matn == "👥 Foydalanuvchilar soni":
            bot.send_message(message.chat.id, f"👥 Jami foydalanuvchilar: *{len(USERS)} ta*", parse_mode="Markdown")
            return

    if matn == "ℹ️ Bot haqida":
        info = (
            "🤖 *Hashtag Bot*\n\n"
            "📊 500+ hashtag\n"
            "📂 10 ta kategoriya\n"
            "🇺🇿 O'zbek tilida\n\n"
            "✅ Bepul foydalaning"
        )
        bot.send_message(message.chat.id, info, parse_mode="Markdown")
        return

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
            reply_markup=kategoriyalar_klaviaturasi(message.from_user.id)
        )

# =============================================
# INLINE TUGMALAR
# =============================================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data

    if data == "obuna_tekshir":
        if obuna_tekshir(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            matn = (
                "✅ Rahmat! Obuna bo'ldingiz!\n\n"
                "👋 Salom! Men *Hashtag Bot*man!\n"
                "👨‍💼 Bot egasi: Jumanazarov Behruz\n\n"
                "👇 Quyidan kategoriya tanlang:"
            )
            bot.send_message(
                call.message.chat.id,
                matn,
                parse_mode="Markdown",
                reply_markup=kategoriyalar_klaviaturasi(call.from_user.id)
            )
        else:
            bot.answer_callback_query(call.id, "❗ Hali obuna bo'lmadingiz!", show_alert=True)
        return

    if not obuna_tekshir(call.from_user.id):
        bot.answer_callback_query(call.id, "❗ Avval kanalga obuna bo'ling!", show_alert=True)
        return

    if data == "back_menu":
        bot.edit_message_text(
            "👇 Kategoriya tanlang:",
            call.message.chat.id,
            call.message.message_id
        )
        bot.send_message(
            call.message.chat.id,
            "✅ Asosiy menyu:",
            reply_markup=kategoriyalar_klaviaturasi(call.from_user.id)
        )
        return

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
