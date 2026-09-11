import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Read tokens from Railway environment variables
RENOVA_TOKEN = os.getenv("RENOVA_BOT_TOKEN")
NERO_TOKEN = os.getenv("NERO_BOT_TOKEN")

renova_bot = telebot.TeleBot(RENOVA_TOKEN)
nero_bot = telebot.TeleBot(NERO_TOKEN)

# Live Square Payment Links
SQUARE_TEXT_READING_URL = "https://square.link/u/yaq743A5"
SQUARE_VOICE_READING_URL = "https://square.link/u/oYibDkgK"
WEBSITE_URL = "https://renovaaetherandstone.com"


# ==========================================
# 🌟 RENOVA CLIENT BOT (@RenovaAetherStone1Bot)
# ==========================================
@renova_bot.message_handler(commands=['start', 'menu'])
def renova_welcome(message):
    welcome_text = (
        "✨ **Welcome to Renova Aether & Stone** ✨\n\n"
        "Grounded intuitive guidance, tarot analysis, and energy readings with Jarrod.\n\n"
        "Select an option below to book your reading or explore the site:"
    )

    markup = InlineKeyboardMarkup(row_width=1)
    
    # Square Payment Buttons
    btn_text_reading = InlineKeyboardButton(
        "📜 $25 — 3-Question Text Reading", 
        url=SQUARE_TEXT_READING_URL
    )
    btn_voice_reading = InlineKeyboardButton(
        "🎙️ $50 — 15-Minute Voice Note Reading", 
        url=SQUARE_VOICE_READING_URL
    )
    
    # Telegram Mini App Webview Button
    btn_miniapp = InlineKeyboardButton(
        "🌐 Open Interactive Site (Mini App)", 
        web_app=WebAppInfo(url=WEBSITE_URL)
    )
    
    markup.add(btn_text_reading, btn_voice_reading, btn_miniapp)

    renova_bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")


# ==========================================
# 🧪 NERO TEST BOT (@Nerolabtestbot)
# ==========================================
@nero_bot.message_handler(commands=['start'])
def nero_welcome(message):
    nero_msg = (
        "🧪 **Nero Sandbox Active** (@Nerolabtestbot)\n\n"
        "Testing inline webviews and features."
    )
    markup = InlineKeyboardMarkup()
    btn_test = InlineKeyboardButton("🧪 Test Webview", web_app=WebAppInfo(url=WEBSITE_URL))
    markup.add(btn_test)

    nero_bot.send_message(message.chat.id, nero_msg, reply_markup=markup, parse_mode="Markdown")


# ==========================================
# 🚀 RUN BOTH BOTS
# ==========================================
if __name__ == "__main__":
    t1 = threading.Thread(target=lambda: renova_bot.infinity_polling(), daemon=True)
    t1.start()
    nero_bot.infinity_polling()
