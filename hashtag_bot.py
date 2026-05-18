"""
𝓤𝓷𝓲𝓿𝓮𝓻𝓼𝓪𝓵 𝓗𝓪𝓼𝓱𝓽𝓪𝓰 𝓑𝓸𝓽 - 𝕺'𝖟𝖇𝖊𝖐 𝖙𝖎𝖑𝖎
Platform: Telegram
Kutubxonalar:
  pip install pyTelegramBotAPI yt-dlp
"""

import telebot
import yt_dlp
import os
import re
import json
import tempfile
from telebot import types

BOT_TOKEN = "8944587981:AAF9K1j8_siX3xVpJPml6TtX8NBn7WlFnR8"
KANAL = "@ixo_uzz"
ADMIN_IDS = [6391668377]  # <-- O'z Telegram ID'ingizni yozing

USERS_FILE = "users.json"

bot = telebot.TeleBot(BOT_TOKEN)

# ═══════════════════════════════════════════════
# 𝗙𝗢𝗬𝗗𝗔𝗟𝗔𝗡𝗨𝗩𝗖𝗛𝗜𝗟𝗔𝗥  𝗕𝗔𝗭𝗔𝗦𝗜
# ═══════════════════════════════════════════════

def users_yukla():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def users_saqlash(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def foydalanuvchi_qoshish(user):
    users = users_yukla()
    uid = str(user.id)
    if uid not in users:
        users[uid] = {
            "id": user.id,
            "ism": user.first_name or "",
            "username": user.username or ""
        }
        users_saqlash(users)

def barcha_userlar():
    users = users_yukla()
    return [v["id"] for v in users.values()]

# ═══════════════════════════════════════════════
# 𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠  𝗨𝗥𝗟  𝗧𝗘𝗞𝗦𝗛𝗜𝗥𝗨𝗩𝗜
# ═══════════════════════════════════════════════

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

# ═══════════════════════════════════════════════
# 𝗩𝗜𝗗𝗘𝗢  𝗬𝗨𝗞𝗟𝗔𝗕  𝗢𝗟𝗜𝗦𝗛  (yt-dlp)
# ═══════════════════════════════════════════════

def instagram_video_yukla(url):
    tmp_dir = tempfile.mkdtemp()
    fayl_nomi = os.path.join(tmp_dir, "instagram_%(id)s.%(ext)s")

    ydl_opts = {
        "outtmpl": fayl_nomi,
        "quiet": True,
        "no_warnings": True,
        "format": "best[ext=mp4]/best",
        # "cookiefile": "instagram_cookies.txt",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            yuklab_fayl = ydl.prepare_filename(info)

            if os.path.exists(yuklab_fayl):
                return yuklab_fayl, "video"

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

# ═══════════════════════════════════════════════
# 𝗛𝗔𝗦𝗛𝗧𝗔𝗚  𝗞𝗨𝗧𝗨𝗕𝗫𝗢𝗡𝗔𝗦𝗜
# ═══════════════════════════════════════════════

HASHTAGS = {
    "biznes": {
        "nomi": "💼 𝗕𝗶𝘇𝗻𝗲𝘀 𝘃𝗮 𝗦𝗮𝘃𝗱𝗼",
        "taglar": [
            "#biznes #savdo #startup #tadbirkorlik #investitsiya",
            "#ecommerce #onlinebiznes #daromad #moliya #kapital",
            "#marketing #reklama #brend #mijozlar #sotish",
            "#b2b #b2c #sheriklik #hamkorlik #bitim",
            "#import #eksport #logistika #yetkazib_berish #ombor",
        ]
    },
    "lifestyle": {
        "nomi": "🌟 𝗟𝗶𝗳𝗲𝘀𝘁𝘆𝗹𝗲 𝘃𝗮 𝗕𝗹𝗼𝗴",
        "taglar": [
            "#lifestyle #hayot #motivatsiya #ilhom #muvaffaqiyat",
            "#blog #blogger #content #ijod #yaratuvchilik",
            "#travel #sayohat #dunyo #kashfiyot #adventure",
            "#fashion #moda #stil #trend #looks",
            "#fitness #sport #sog_lom #energia #harakat",
        ]
    },
    "talim": {
        "nomi": "📚 𝗧𝗮'𝗹𝗶𝗺 𝘃𝗮 𝗞𝘂𝗿𝘀",
        "taglar": [
            "#talim #kurs #onlinekurs #dars #oqish",
            "#dasturlash #programming #IT #texnologiya #kod",
            "#ingliz_tili #til_oqish #grammar #speaking #english",
            "#matematika #fizika #kimyo #biologiya #tarix",
            "#sertifikat #diplom #bilim #rivojlanish #career",
        ]
    },
    "oziq": {
        "nomi": "🍽️ 𝗢𝘃𝗾𝗮𝘁 𝘃𝗮 𝗥𝗲𝘀𝘁𝗼𝗿𝗮𝗻",
        "taglar": [
            "#ovqat #taom #restoran #cafe #yemak",
            "#milliy_taomlar #oshpaz #recipe #retsept #cooking",
            "#delivery #yetkazib_berish #pizza #burger #sushi",
            "#nonushta #tushlik #kechki_ovqat #ziyofat #tort",
            "#vegan #diet #sog_lom_ovqat #kaloriya #nutrition",
        ]
    },
    "texnologiya": {
        "nomi": "💻 𝗧𝗲𝘅𝗻𝗼𝗹𝗼𝗴𝗶𝘆𝗮",
        "taglar": [
            "#texnologiya #tech #innovation #gadget #smartphone",
            "#AI #suniy_intellekt #machinelearning #robot #future",
            "#cybersecurity #xavfsizlik #hacking #privacy #data",
            "#mobile #android #ios #app #ilovalar",
            "#cloud #server #hosting #database #software",
        ]
    },
    "soglik": {
        "nomi": "❤️ 𝗦𝗼𝗴'𝗹𝗶𝗾 𝘃𝗮 𝗙𝗶𝘁𝗻𝗲𝘀",
        "taglar": [
            "#soglik #salomatlik #tibbiyot #doktor #klinika",
            "#fitness #gym #workout #muskul #crossfit",
            "#yoga #meditatsiya #mindfulness #stresssiz #ruh",
            "#parhez #diet #ozayish #vaznni_kamaytirish #slim",
            "#vitamin #supplement #sog_lom_hayot #wellbeing #detox",
        ]
    },
    "kino": {
        "nomi": "🎬 𝗞𝗼'𝗻𝗴𝗶𝗹𝗼𝗰𝗵𝗮𝗿",
        "taglar": [
            "#kino #film #serial #anime #netflix",
            "#musiqa #qoshiq #artist #concert #live",
            "#gaming #oyin #playstation #xbox #mobile_game",
            "#komediya #hazil #meme #trend #viral",
            "#uzbekfilm #ozbekmusiqasi #milliy #madaniyat #sanaat",
        ]
    },
    "uy": {
        "nomi": "🏠 𝗨𝘆 𝘃𝗮 𝗗𝗶𝘇𝗮𝘆𝗻",
        "taglar": [
            "#uy #kvartira #interer #dizayn #dekor",
            "#remont #qurilish #mebel #mebeldesign #homedesign",
            "#bog #gul #ochilar #tabiat #green",
            "#realestate #kochirilmas_mulk #sotiladi #ijaraga #yangiuy",
            "#handmade #qolbola #crafts #DIY #homemade",
        ]
    },
    "moda": {
        "nomi": "👗 𝗠𝗼𝗱𝗮 𝘃𝗮 𝗚𝗼'𝘇𝗮𝗹𝗹𝗶𝗸",
        "taglar": [
            "#moda #fashion #style #trend #ootd",
            "#gozellik #makeup #beauty #skincare #parfum",
            "#kiyim #aksesuar #sumka #poyabzal #bijuteriya",
            "#milliy_kiyim #atlas #ipak #uzbekmoda #handmade",
            "#fitness_look #sport_kiyim #casual #formal #classic",
        ]
    },
    "uzbekiston": {
        "nomi": "🇺🇿 𝗢'𝘇𝗯𝗲𝗸𝗶𝘀𝘁𝗼𝗻",
        "taglar": [
            "#uzbekiston #toshkent #samarqand #buxoro #namangan",
            "#uzbek #ozbek #milliy #vatandosh #mening_yurtim",
            "#visituzbekistan #uzbektourism #silk_road #tariximiz #madaniyat",
            "#uzbekfood #osh #somsa #shashlik #lagmon",
            "#uzb #uzbek_blogger #ozbek_content #uzbekmedia #tashkent",
        ]
    }
}

# ═══════════════════════════════════════════════
# 𝗬𝗢𝗥𝗗𝗔𝗠𝗖𝗛𝗜  𝗙𝗨𝗡𝗞𝗦𝗜𝗬𝗔𝗟𝗔𝗥
# ═══════════════════════════════════════════════

def admin_mi(user_id):
    return user_id in ADMIN_IDS

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
        "🚫 *Botdan foydalanish uchun avval kanalga obuna bo'ling:*\n\n"
        f"👉 {KANAL}\n\n"
        "Obuna bo'lgach '🔄 Tekshirish' tugmasini bosing.",
        reply_markup=markup
    )

# ═══════════════════════════════════════════════
# 𝗞𝗟𝗔𝗩𝗜𝗔𝗧𝗨𝗥𝗔𝗟𝗔𝗥
# ═══════════════════════════════════════════════

def asosiy_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📥 Video Yuklab olish"),
        types.KeyboardButton("🏷 Hashtaglar")
    )
    markup.add(types.KeyboardButton("ℹ️ Bot haqida"))
    return markup

def video_bolim_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("⬅️ Orqaga"))
    return markup

def hashtag_bolim_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    tugmalar = [types.KeyboardButton(v["nomi"]) for v in HASHTAGS.values()]
    markup.add(*tugmalar)
    markup.add(types.KeyboardButton("⬅️ Orqaga"))
    return markup

def admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📢 Xabar yuborish"),
        types.KeyboardButton("👥 Foydalanuvchilar soni")
    )
    markup.add(types.KeyboardButton("🔙 Oddiy menyu"))
    return markup

def hashtaglar_inline(kategoriya_kodi):
    markup = types.InlineKeyboardMarkup(row_width=1)
    taglar = HASHTAGS[kategoriya_kodi]["taglar"]
    for i, guruh in enumerate(taglar):
        birinchi = guruh.split()[0]
        markup.add(types.InlineKeyboardButton(
            f"📋 {birinchi} … ({len(guruh.split())} ta)",
            callback_data=f"tag_{kategoriya_kodi}_{i}"
        ))
    return markup

def kategoriya_kodini_top(nomi):
    for kod, v in HASHTAGS.items():
        if v["nomi"] == nomi:
            return kod
    return None

# ═══════════════════════════════════════════════
# 𝗛𝗢𝗟𝗔𝗧  𝗕𝗢𝗦𝗛𝗤𝗔𝗥𝗜𝗦𝗛  (state)
# ═══════════════════════════════════════════════

user_states = {}
# None        → asosiy menyu
# "video"     → video bo'limida
# "hashtag"   → hashtag bo'limida
# "admin"     → admin panelda
# "broadcast" → xabar yozish kutilmoqda

# ═══════════════════════════════════════════════
# /𝘀𝘁𝗮𝗿𝘁
# ═══════════════════════════════════════════════

@bot.message_handler(commands=['start'])
def start(message):
    foydalanuvchi_qoshish(message.from_user)

    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    user_states[message.from_user.id] = None

    matn = (
        "👋 *Salom! Men* 𝗛𝗮𝘀𝗵𝘁𝗮𝗴 𝗕𝗼𝘁 *man!*\n\n"
        "📌 *Nimalar bor?*\n"
        "📥 *Video Yuklab olish* — Instagram Reel/Post/Stories\n"
        "🏷 *Hashtaglar* — 500+ tayyor hashtag\n\n"
        "👇 Bo'lim tanlang:"
    )
    bot.send_message(
        message.chat.id,
        matn,
        parse_mode="Markdown",
        reply_markup=asosiy_menu()
    )

# ═══════════════════════════════════════════════
# /𝗮𝗱𝗺𝗶𝗻
# ═══════════════════════════════════════════════

@bot.message_handler(commands=['admin'])
def admin_cmd(message):
    if not admin_mi(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")
        return

    user_states[message.from_user.id] = "admin"
    users = users_yukla()
    bot.send_message(
        message.chat.id,
        f"🔐 *𝗔𝗱𝗺𝗶𝗻 𝗣𝗮𝗻𝗲𝗹*\n\n"
        f"👥 Jami foydalanuvchilar: *{len(users)}* ta\n\n"
        "Quyidan amal tanlang:",
        parse_mode="Markdown",
        reply_markup=admin_menu()
    )

# ═══════════════════════════════════════════════
# /𝗵𝗲𝗹𝗽
# ═══════════════════════════════════════════════

@bot.message_handler(commands=['help'])
def help_cmd(message):
    if not obuna_tekshir(message.from_user.id):
        obuna_xabari(message.chat.id)
        return

    matn = (
        "📖 *𝗬𝗼𝗿𝗱𝗮𝗺*\n\n"
        "📥 *Video bo'limi:*\n"
        "Instagram Reel, Post yoki Stories havolasini yuboring\n\n"
        "🏷 *Hashtag bo'limi:*\n"
        "Kategoriya tanlab, tayyor hashtaglarni nusxalab oling\n\n"
        "📌 *Buyruqlar:*\n"
        "/start — Boshlanish\n"
        "/help — Yordam\n"
        "/admin — Admin panel (faqat adminlar)\n"
    )
    bot.send_message(message.chat.id, matn, parse_mode="Markdown")

# ═══════════════════════════════════════════════
# 𝗠𝗔𝗧𝗡  𝗫𝗔𝗕𝗔𝗥𝗟𝗔𝗥
# ═══════════════════════════════════════════════

@bot.message_handler(content_types=['text'])
def matn_handler(message):
    uid = message.from_user.id
    matn = message.text.strip()
    holat = user_states.get(uid)

    foydalanuvchi_qoshish(message.from_user)

    # ── ADMIN PANEL ──────────────────────────────
    if holat == "admin" and admin_mi(uid):
        if matn == "📢 Xabar yuborish":
            user_states[uid] = "broadcast"
            bot.send_message(
                message.chat.id,
                "✏️ Barcha foydalanuvchilarga yuboriladigan xabarni yozing:\n\n"
                "(Bekor qilish uchun /bekor yozing)"
            )
            return

        if matn == "👥 Foydalanuvchilar soni":
            users = users_yukla()
            bot.send_message(
                message.chat.id,
                f"👥 Jami foydalanuvchilar: *{len(users)}* ta",
                parse_mode="Markdown"
            )
            return

        if matn == "🔙 Oddiy menyu":
            user_states[uid] = None
            bot.send_message(
                message.chat.id,
                "✅ Asosiy menyuga qaytdingiz.",
                reply_markup=asosiy_menu()
            )
            return

    # ── BROADCAST ────────────────────────────────
    if holat == "broadcast" and admin_mi(uid):
        if matn == "/bekor":
            user_states[uid] = "admin"
            bot.send_message(
                message.chat.id,
                "❌ Bekor qilindi.",
                reply_markup=admin_menu()
            )
            return

        userlar = barcha_userlar()
        yuborildi = 0
        xato = 0

        progress_xabar = bot.send_message(
            message.chat.id,
            f"⏳ Yuborilmoqda… 0/{len(userlar)}"
        )

        for i, user_id in enumerate(userlar):
            try:
                bot.send_message(user_id, f"📢 *Yangilik:*\n\n{matn}", parse_mode="Markdown")
                yuborildi += 1
            except:
                xato += 1

            if (i + 1) % 20 == 0:
                try:
                    bot.edit_message_text(
                        f"⏳ Yuborilmoqda… {i+1}/{len(userlar)}",
                        message.chat.id,
                        progress_xabar.message_id
                    )
                except:
                    pass

        bot.edit_message_text(
            f"✅ *𝗬𝘂𝗯𝗼𝗿𝗶𝗹𝗱𝗶!*\n\n"
            f"✔️ Muvaffaqiyatli: {yuborildi}\n"
            f"❌ Xato (bloklagan): {xato}\n"
            f"📊 Jami: {len(userlar)}",
            message.chat.id,
            progress_xabar.message_id,
            parse_mode="Markdown"
        )
        user_states[uid] = "admin"
        bot.send_message(message.chat.id, "𝗔𝗱𝗺𝗶𝗻 𝗽𝗮𝗻𝗲𝗹:", reply_markup=admin_menu())
        return

    # ── OBUNA TEKSHIRISH ─────────────────────────
    if not obuna_tekshir(uid):
        obuna_xabari(message.chat.id)
        return

    # ── ORQAGA ───────────────────────────────────
    if matn == "⬅️ Orqaga":
        user_states[uid] = None
        bot.send_message(
            message.chat.id,
            "🏠 𝗔𝘀𝗼𝘀𝗶𝘆 𝗺𝗲𝗻𝘆𝘂:",
            reply_markup=asosiy_menu()
        )
        return

    # ── ASOSIY MENYU ─────────────────────────────
    if holat is None:
        if matn == "📥 Video Yuklab olish":
            user_states[uid] = "video"
            bot.send_message(
                message.chat.id,
                "📥 *𝗩𝗶𝗱𝗲𝗼 𝗬𝘂𝗸𝗹𝗮𝗯 𝗢𝗹𝗶𝘀𝗵 𝗕𝗼'𝗹𝗶𝗺𝗶*\n\n"
                "Qo'llab-quvvatlanadigan turlar:\n"
                "🎬 Reels\n"
                "🖼 Post (video)\n"
                "📖 Stories\n\n"
                "Instagram havolasini yuboring:\n"
                "`https://www.instagram.com/reel/ABC123/`\n\n"
                "⚠️ Yopiq (private) postlar yuklanmaydi.",
                parse_mode="Markdown",
                reply_markup=video_bolim_menu()
            )
            return

        if matn == "🏷 Hashtaglar":
            user_states[uid] = "hashtag"
            bot.send_message(
                message.chat.id,
                "🏷 *𝗛𝗮𝘀𝗵𝘁𝗮𝗴 𝗕𝗼'𝗹𝗶𝗺𝗶*\n\n"
                "Kategoriya tanlang:",
                parse_mode="Markdown",
                reply_markup=hashtag_bolim_menu()
            )
            return

        if matn == "ℹ️ Bot haqida":
            users = users_yukla()
            info = (
                "🤖 *𝗛𝗮𝘀𝗵𝘁𝗮𝗴 𝗕𝗼𝘁*\n\n"
                f"👥 Foydalanuvchilar: {len(users)} ta\n"
                "📊 500+ hashtag\n"
                "📂 10 ta kategoriya\n"
                "📥 Instagram video yuklab olish\n"
                "🇺🇿 O'zbek tilida\n\n"
                "✅ Bepul foydalaning"
            )
            bot.send_message(message.chat.id, info, parse_mode="Markdown")
            return

        bot.send_message(
            message.chat.id,
            "👇 Bo'lim tanlang:",
            reply_markup=asosiy_menu()
        )
        return

    # ── VIDEO BO'LIMI ─────────────────────────────
    if holat == "video":
        if instagram_url_mi(matn):
            url = url_ajrat(matn)
            kutish = bot.send_message(message.chat.id, "⏳ Video yuklanmoqda, biroz kuting…")
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
                bot.send_message(message.chat.id, tur)
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Instagram havolasi emas.\n\n"
                "To'g'ri havola misoli:\n"
                "`https://www.instagram.com/reel/ABC123/`",
                parse_mode="Markdown"
            )
        return

    # ── HASHTAG BO'LIMI ───────────────────────────
    if holat == "hashtag":
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
                "👇 Kategoriya tanlang:",
                reply_markup=hashtag_bolim_menu()
            )
        return

# ═══════════════════════════════════════════════
# 𝗜𝗡𝗟𝗜𝗡𝗘  𝗧𝗨𝗚𝗠𝗔𝗟𝗔𝗥
# ═══════════════════════════════════════════════

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data

    if data == "obuna_tekshir":
        if obuna_tekshir(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_states[call.from_user.id] = None
            matn = (
                "✅ *Rahmat! Obuna bo'ldingiz!*\n\n"
                "👋 Salom! Men *𝗛𝗮𝘀𝗵𝘁𝗮𝗴 𝗕𝗼𝘁* man!\n\n"
                "👇 Bo'lim tanlang:"
            )
            bot.send_message(
                call.message.chat.id,
                matn,
                parse_mode="Markdown",
                reply_markup=asosiy_menu()
            )
        else:
            bot.answer_callback_query(call.id, "❗ Hali obuna bo'lmadingiz!", show_alert=True)
        return

    if not obuna_tekshir(call.from_user.id):
        bot.answer_callback_query(call.id, "❗ Avval kanalga obuna bo'ling!", show_alert=True)
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
                f"✅ *𝗡𝘂𝘀𝘅𝗮𝗹𝗮𝗯 𝗼𝗹𝗶𝗻𝗴:*\n\n`{taglar}`",
                parse_mode="Markdown"
            )

# ═══════════════════════════════════════════════
# 𝗕𝗢𝗧𝗡𝗜  𝗜𝗦𝗛𝗚𝗔  𝗧𝗨𝗦𝗛𝗜𝗥𝗜𝗦𝗛
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("🤖 𝗛𝗮𝘀𝗵𝘁𝗮𝗴 𝗕𝗼𝘁 ishga tushdi…")
    print("Admin ID:", ADMIN_IDS)
    print("Toxtatish uchun Ctrl+C bosing")
    bot.infinity_polling()
