import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

RENOVA_TOKEN = os.getenv("RENOVA_BOT_TOKEN")
NERO_TOKEN = os.getenv("NERO_BOT_TOKEN")

renova_bot = telebot.TeleBot(RENOVA_TOKEN)
nero_bot = telebot.TeleBot(NERO_TOKEN)

# Live Links
SQUARE_TEXT_READING_URL = "https://square.link/u/yaq743A5"
SQUARE_VOICE_READING_URL = "https://square.link/u/oYibDkgK"
WEBSITE_URL = "https://www.renovaaetherandstone.com"
TELEGRAM_GROUP_URL = "https://t.me/+3ClNaQ3t5KJjZTJl"
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/LTIVL6u2QFl3zEzX2ARKNE"


# ==========================================
# 🌟 RENOVA CLIENT BOT (@RenovaAetherStone1Bot)
# ==========================================

def get_main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    
    btn_readings = InlineKeyboardButton("📜 Book a Reading", callback_data="menu_readings")
    btn_about = InlineKeyboardButton("🔮 About Jarrod & Practice", callback_data="menu_about")
    btn_tele_group = InlineKeyboardButton("📖 Telegram Insights Group", url=TELEGRAM_GROUP_URL)
    btn_wa_group = InlineKeyboardButton("💬 WhatsApp Insights Community", url=WHATSAPP_GROUP_URL)
    btn_contact = InlineKeyboardButton("📞 Contact / PayID", callback_data="menu_contact")
    btn_miniapp = InlineKeyboardButton("🌐 Open Interactive Site", web_app=WebAppInfo(url=WEBSITE_URL))
    
    markup.add(btn_readings, btn_about, btn_tele_group, btn_wa_group, btn_contact, btn_miniapp)
    return markup


@renova_bot.message_handler(commands=['start', 'menu'])
def renova_welcome(message):
    welcome_text = (
        "✨ **Welcome to Renova Aether & Stone** ✨\n\n"
        "Grounded intuitive guidance, tarot analysis, and energy readings with Jarrod.\n\n"
        "Select an option below:"
    )
    renova_bot.send_message(
        message.chat.id, 
        welcome_text, 
        reply_markup=get_main_menu_markup(), 
        parse_mode="Markdown"
    )


@renova_bot.callback_query_handler(func=lambda call: True)
def handle_menu_callbacks(call):
    if call.data == "menu_readings":
        readings_text = (
            "✨ **CHOOSE YOUR READING FORMAT** ✨\n\n"
            "📜 **3-Question Text Reading ($25 AUD)**\n"
            "Share three questions and receive a focused written reading with space to return to it in your own time.\n\n"
            "🎙️ **15-Minute Voice Note Reading ($50 AUD)**\n"
            "A concise spoken reading for the thread that needs more nuance, delivered in Jarrod's clear and considered voice."
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("💳 Pay $25 & Book Text Reading", url=SQUARE_TEXT_READING_URL),
            InlineKeyboardButton("💳 Pay $50 & Book Voice Reading", url=SQUARE_VOICE_READING_URL),
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")
        )
        renova_bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=readings_text,
            reply_markup=markup,
            parse_mode="Markdown"
        )

    elif call.data == "menu_about":
        about_text = (
            "🔮 **ABOUT JARROD & RENOVA AETHER & STONE**\n\n"
            "A reading practice rooted in attention.\n\n"
            "Jarrod works at the meeting point of intuitive listening and practical reflection. "
            "Through tarot, clairaudient insight, and the energetic character of a place, "
            "each reading makes room for the patterns that want to be noticed — without rushing toward certainty."
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📜 View Readings & Pricing", callback_data="menu_readings"),
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")
        )
        renova_bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=about_text,
            reply_markup=markup,
            parse_mode="Markdown"
        )

    elif call.data == "menu_contact":
        contact_text = (
            "💬 **CONTACT & DIRECT PAYMENT**\n\n"
            "• **WhatsApp Community:** Join for updates & insights\n"
            "• **PayID:** `+61479129590`\n"
            "• **Website:** https://www.renovaaetherandstone.com"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📖 Join Telegram Insights Group", url=TELEGRAM_GROUP_URL),
            InlineKeyboardButton("💬 Join WhatsApp Community", url=WHATSAPP_GROUP_URL),
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main")
        )
        renova_bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=contact_text,
            reply_markup=markup,
            parse_mode="Markdown"
        )

    elif call.data == "menu_main":
        welcome_text = (
            "✨ **Welcome to Renova Aether & Stone** ✨\n\n"
            "Grounded intuitive guidance, tarot analysis, and energy readings with Jarrod.\n\n"
            "Select an option below:"
        )
        renova_bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=welcome_text,
            reply_markup=get_main_menu_markup(),
            parse_mode="Markdown"
        )


# ==========================================
# 🧪 NERO TEST BOT (@Nerolabtestbot)
# ==========================================
@nero_bot.message_handler(commands=['start'])
def nero_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🧪 Test Webview", web_app=WebAppInfo(url=WEBSITE_URL)))
    nero_bot.send_message(message.chat.id, "🧪 **Nero Sandbox Active**", reply_markup=markup, parse_mode="Markdown")


# ==========================================
# 🚀 RUN BOTH BOTS
# ==========================================
if __name__ == "__main__":
    t1 = threading.Thread(target=lambda: renova_bot.infinity_polling(), daemon=True)
    t1.start()
    nero_bot.infinity_polling()
