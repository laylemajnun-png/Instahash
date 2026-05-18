"""
Universal Hashtag Bot - O'zbek tili
Platform: Telegram
Kutubxonalar:
  pip install pyTelegramBotAPI yt-dlp
"""

import telebot
import yt_dlp
import os
import re
import tempfile
from telebot import types

BOT_TOKEN = "8898761623:AAFvubHB-KPaj7QMurVUMPBs7eKXNgzJDGY"
KANAL = "@instaheshteg_uz"

bot = telebot.TeleBot(BOT_TOKEN)

# =============================================
# INSTAGRAM URL TEKSHIRUVI
# =============================================

INSTAGRAM_REGEX = re.compile(
    r'(https?://)?(www\.)?instagram\.com/'
    r'(p|reel|reels|tv|stories)/[A-Za-z0-9_\-]+/?'
)

def instagram_url_mi(matn):
    return bool(INSTAGRAM_REGEX.search(matn))

def url_ajrat(matn):
    natija = INSTAGRAM_REGEX.search(matn)
    if natija:
        return natija.group(0)
    return None

# =============================================
# VIDEO YUKLAB OLISH (yt-dlp)
# =============================================

def instagram_video_yukla(url):
    """
    Qaytaradi: (fayl_yoli, tur) yoki (None, xato_xabar)
    tur: 'video' yoki 'photo'
    """
    tmp_dir = tempfile.mkdtemp()
    fayl_nomi = os.path.join(tmp_dir, "instagram_%(id)s.%(ext)s")

    ydl_opts = {
        "outtmpl": fayl_nomi,
        "quiet": True,
        "no_warnings": True,
        "format": "best[ext=mp4]/best",
        # Agar Instagram cookie kerak bo'lsa quyidagini yoching:
        # "cookiefile": "instagram_cookies.txt",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            yuklab_fayl = ydl.prepare_filename(info)

            # Fayl mavjudmi tekshir
            if os.path.exists(yuklab_fayl):
                return yuklab_fayl, "video"

            # Ba'zan kengaytma o'zgarishi mumkin
            for f in os.listdir(tmp_dir):
                to_liq = os.path.join(tmp_dir, f)
                if os.path.isfile(to_liq):
                    return to_liq, "video"

        return None, "❌ Fayl topilmadi. URL to'g'riligini tekshiring."

    except yt_dlp.utils.DownloadError as e:
        xato = str(e)
        if "Private" in xato or "login" in xato.lower():
            return None, "🔒 Bu post yopiq (private) yoki login talab qiladi."
        if "not found" in xato.lower() or "404" in xato:
            return None, "❌ Post topilmadi. O'chirilgan bo'lishi mumkin."
        return None, f"⚠️ Yuklab bo'lmadi: {xato[:200]}"
    except Exception as e:
        return None, f"⚠️ Xatolik: {str(e)[:200]}"

def faylni_tozala(yol):
    try:
        if yol and os.path.exists(yol):
            os.remove(yol)
            parent = os.path.dirname(yol)
            if os.path.isdir(parent):
                os.rmdir(parent)
    except:
        pass

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

def kategoriyalar_klaviaturasi():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    tugmalar = [types.KeyboardButton(v["nomi"]) for v in HASHTAGS.values()]
    markup.add(*tugmalar)
    markup.add(types.KeyboardButton("📥 Video Yuklab olish"))
    markup.add(types.KeyboardButton("ℹ️ Bot haqida"))
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
    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    matn = (
        "👋 Salom! Men *Hashtag Bot*man!\n\n"
        "📌 Nima qila olaman?\n"
        "• 10 ta kategoriyadan hashtag tanlaysiz\n"
        "• Tayyor hashtaglarni nusxalab olasiz\n"
        "• 500+ dan ortiq hashtag mavjud\n"
        "• 📥 Instagram video/reel/stories yuklab olish\n\n"
        "👇 Quyidan kategoriya tanlang yoki Instagram havolasini yuboring:"
    )
    bot.send_message(
        message.chat.id,
        matn,
        parse_mode="Markdown",
        reply_markup=kategoriyalar_klaviaturasi()
    )

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
        "📥 *Video yuklab olish:*\n"
        "Instagram Reel, Post yoki Stories havolasini yuboring — bot avtomatik yuklab beradi!\n\n"
        "📌 *Buyruqlar:*\n"
        "/start - Boshlanish\n"
        "/help - Yordam\n"
        "/yukla - Video yuklab olish haqida\n"
    )
    bot.send_message(message.chat.id, matn, parse_mode="Markdown")

# =============================================
# /yukla
# =============================================

@bot.message_handler(commands=['yukla'])
def yukla_cmd(message):
    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    matn = (
        "📥 *Instagram Video Yuklab Olish*\n\n"
        "Qo'llab-quvvatlanadigan turlar:\n"
        "• 🎬 Reels\n"
        "• 🖼 Post (video)\n"
        "• 📖 Stories\n\n"
        "Faqat Instagram havolasini yuboring, masalan:\n"
        "`https://www.instagram.com/reel/ABC123/`\n\n"
        "⚠️ Yopiq (private) postlar yuklanmaydi."
    )
    bot.send_message(message.chat.id, matn, parse_mode="Markdown")

# =============================================
# MATN XABARLAR
# =============================================

@bot.message_handler(content_types=['text'])
def matn_handler(message):
    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    matn = message.text.strip()

    # --- Instagram URL bo'lsa ---
    if instagram_url_mi(matn):
        url = url_ajrat(matn)
        kutish = bot.send_message(
            message.chat.id,
            "⏳ Video yuklanmoqda, biroz kuting..."
        )
        fayl_yoli, tur = instagram_video_yukla(url)

        bot.delete_message(message.chat.id, kutish.message_id)

        if fayl_yoli:
            try:
                with open(fayl_yoli, "rb") as f:
                    bot.send_video(
                        message.chat.id,
                        f,
                        caption="✅ Mana sizning videongiz!\n\n📥 @instaheshtegbot",
                        supports_streaming=True
                    )
            except Exception:
                # Agar video yuborib bo'lmasa, fayl sifatida yuborish
                try:
                    with open(fayl_yoli, "rb") as f:
                        bot.send_document(
                            message.chat.id,
                            f,
                            caption="✅ Mana sizning faylingiz!\n\n📥 @instaheshtegbot"
                        )
                except Exception as e:
                    bot.send_message(message.chat.id, f"⚠️ Yuborishda xatolik: {str(e)[:200]}")
            finally:
                faylni_tozala(fayl_yoli)
        else:
            bot.send_message(message.chat.id, tur)  # tur = xato xabari
        return

    # --- Video yuklab olish tugmasi ---
    if matn == "📥 Video Yuklab olish":
        bot.send_message(
            message.chat.id,
            "📥 *Instagram Video Yuklab Olish*\n\n"
            "Instagram Reel, Post yoki Stories havolasini yuboring:\n\n"
            "Masalan:\n"
            "`https://www.instagram.com/reel/ABC123/`\n\n"
            "⚠️ Yopiq (private) postlar yuklanmaydi.",
            parse_mode="Markdown"
        )
        return

    # --- Bot haqida ---
    if matn == "ℹ️ Bot haqida":
        info = (
            "🤖 *Hashtag Bot*\n\n"
            "📊 500+ hashtag\n"
            "📂 10 ta kategoriya\n"
            "📥 Instagram video yuklab olish\n"
            "🇺🇿 O'zbek tilida\n\n"
            "✅ Bepul foydalaning"
        )
        bot.send_message(message.chat.id, info, parse_mode="Markdown")
        return

    # --- Kategoriya ---
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
            "👇 Iltimos, quyidagi kategoriyalardan birini tanlang yoki Instagram havolasini yuboring:",
            reply_markup=kategoriyalar_klaviaturasi()
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
                "👋 Salom! Men *Hashtag Bot*man!\n\n"
                "👇 Quyidan kategoriya tanlang yoki Instagram havolasini yuboring:"
            )
            bot.send_message(
                call.message.chat.id,
                matn,
                parse_mode="Markdown",
                reply_markup=kategoriyalar_klaviaturasi()
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
            reply_markup=kategoriyalar_klaviaturasi()
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
    print("🤖 Hashtag Bot (Video yuklab olish bilan) ishga tushdi...")
    print("Toxtatish uchun Ctrl+C bosing")
    bot.infinity_polling()
