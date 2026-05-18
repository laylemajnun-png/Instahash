import telebot
import yt_dlp
import os
import re
import json
import tempfile
import time
from telebot import types
from dotenv import load_dotenv
from collections import defaultdict

# ==========================================
# ENV
# ==========================================

load_dotenv()

BOT_TOKEN = os.getenv("8944587981:AAH_HrO7hBph_BYe-0arAdlyAoZGAbOFSIA")
KANAL = "@ixo_uzz"
ADMIN_IDS = [6391668377]
USERS_FILE = "users.json"

bot = telebot.TeleBot(BOT_TOKEN)

user_states = defaultdict(lambda: None)

# ==========================================
# USER DATABASE
# ==========================================


def users_yukla():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def users_saqlash(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def foydalanuvchi_qoshish(user):
    users = users_yukla()

    uid = str(user.id)

    if uid not in users:
        users[uid] = {
            "id": user.id,
            "ism": user.first_name,
            "username": user.username
        }

        users_saqlash(users)


# ==========================================
# INSTAGRAM URL
# ==========================================

INSTAGRAM_REGEX = re.compile(
    r'(https?://)?(www\.)?instagram\.com/'
    r'(p|reel|reels|tv|stories)/[A-Za-z0-9_\-]+/?(\?.*)?'
)


def instagram_url_mi(text):
    return bool(INSTAGRAM_REGEX.search(text))


# ==========================================
# DOWNLOAD VIDEO
# ==========================================


def instagram_video_yukla(url):

    tmp_dir = tempfile.mkdtemp()

    out_file = os.path.join(tmp_dir, "%(id)s.%(ext)s")

    ydl_opts = {
        "outtmpl": out_file,
        "quiet": True,
        "format": "best[ext=mp4]/best",
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            return filename

    except Exception as e:
        print(e)
        return None


# ==========================================
# MAIN MENU
# ==========================================


def main_menu():

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )

    markup.add(
        types.KeyboardButton("📥 VIDEO YUKLASH"),
        types.KeyboardButton("🏷 HASHTAGLAR")
    )

    markup.add(
        types.KeyboardButton("🔥 TREND TAG"),
        types.KeyboardButton("📊 STATISTIKA")
    )

    markup.add(
        types.KeyboardButton("👑 PREMIUM"),
        types.KeyboardButton("⚙️ SOZLAMALAR")
    )

    markup.add(
        types.KeyboardButton("ℹ️ BOT HAQIDA")
    )

    return markup


# ==========================================
# HASHTAGS
# ==========================================

HASHTAGS = {
    "biznes": "#biznes #savdo #startup #marketing #money #success",
    "kino": "#kino #film #serial #netflix #movie #viral",
    "moda": "#fashion #style #moda #beauty #trend #ootd",
    "it": "#programming #python #coding #developer #it #tech",
    "travel": "#travel #adventure #trip #nature #vacation #tour",
    "fitness": "#fitness #gym #workout #health #body #sport",
    "food": "#food #burger #pizza #cooking #recipe #restaurant",
    "love": "#love #romantic #heart #couple #relationship #feelings"
}


# ==========================================
# START
# ==========================================

@bot.message_handler(commands=['start'])
def start(message):

    foydalanuvchi_qoshish(message.from_user)

    user_name = message.from_user.first_name

    text = f"""
╔══════════════════════╗
       🤖 HASHTAG BOT
╚══════════════════════╝

👋 Assalomu alaykum {user_name}

🔥 Premium Hashtag Botga xush kelibsiz.

━━━━━━━━━━━━━━━━━━
📥 Instagram video yuklash
🏷 Viral hashtaglar
⚡ Ultra tez ishlash
🎨 Premium dizayn
━━━━━━━━━━━━━━━━━━

👇 Quyidagi menyudan foydalaning
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


# ==========================================
# VIDEO MENU
# ==========================================

@bot.message_handler(func=lambda m: m.text == "📥 VIDEO YUKLASH")
def video_menu(message):

    user_states[message.from_user.id] = "video"

    text = """
🎬 INSTAGRAM VIDEO YUKLASH

🔗 Link yuboring:

https://instagram.com/reel/xxxx

✅ Reels
✅ Stories
✅ Post
"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⬅️ ORQAGA"))

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )


# ==========================================
# HASHTAG MENU
# ==========================================

@bot.message_handler(func=lambda m: m.text == "🏷 HASHTAGLAR")
def hashtag_menu(message):

    markup = types.InlineKeyboardMarkup(row_width=2)

    for key in HASHTAGS:
        markup.add(
            types.InlineKeyboardButton(
                key.upper(),
                callback_data=f"tag_{key}"
            )
        )

    bot.send_message(
        message.chat.id,
        "🔥 Kategoriya tanlang:",
        reply_markup=markup
    )


# ==========================================
# PREMIUM
# ==========================================

@bot.message_handler(func=lambda m: m.text == "👑 PREMIUM")
def premium(message):

    text = """
👑 PREMIUM PANEL

🚀 Tez yuklash
🔥 VIP hashtaglar
📈 Trend analytics
🎨 Exclusive UI

💎 Premium tez orada
"""

    bot.send_message(message.chat.id, text)


# ==========================================
# INFO
# ==========================================

@bot.message_handler(func=lambda m: m.text == "ℹ️ BOT HAQIDA")
def info(message):

    users = users_yukla()

    text = f"""
🤖 HASHTAG BOT

👥 Foydalanuvchilar: {len(users)}
⚡ Version: Premium
🎨 Dizayn: Modern UI
🇺🇿 O'zbek tilida
"""

    bot.send_message(message.chat.id, text)


# ==========================================
# BACK BUTTON
# ==========================================

@bot.message_handler(func=lambda m: m.text == "⬅️ ORQAGA")
def back(message):

    user_states[message.from_user.id] = None

    bot.send_message(
        message.chat.id,
        "🏠 Asosiy menyu",
        reply_markup=main_menu()
    )


# ==========================================
# VIDEO DOWNLOAD
# ==========================================

@bot.message_handler(content_types=['text'])
def text_handler(message):

    uid = message.from_user.id

    if user_states[uid] == "video":

        if instagram_url_mi(message.text):

            wait = bot.send_message(
                message.chat.id,
                "⏳ Yuklanmoqda..."
            )

            file = instagram_video_yukla(message.text)

            bot.delete_message(message.chat.id, wait.message_id)

            if file and os.path.exists(file):

                with open(file, "rb") as f:
                    bot.send_video(
                        message.chat.id,
                        f,
                        caption="✅ Video tayyor"
                    )

                os.remove(file)

            else:
                bot.send_message(
                    message.chat.id,
                    "❌ Yuklab bo'lmadi"
                )

        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Instagram link yuboring"
            )


# ==========================================
# CALLBACKS
# ==========================================

@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):

    if call.data.startswith("tag_"):

        category = call.data.split("_")[1]

        tags = HASHTAGS.get(category)

        bot.send_message(
            call.message.chat.id,
            bot.send_message(
    call.message.chat.id,
    f"✅ Nusxalang:\\n\\n`{tags}`",
    parse_mode="Markdown"
)

    
# ==========================================
# RUN BOT
# ==========================================

print("🤖 Premium Bot Ishga Tushdi")

while True:
    try:
        bot.infinity_polling(
            timeout=30,
            long_polling_timeout=30
        )
    except Exception as e:
        print("Xatolik:", e)
        time.sleep(5)
