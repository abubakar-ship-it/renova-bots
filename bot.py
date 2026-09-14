import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

RENOVA_TOKEN = os.getenv("RENOVA_BOT_TOKEN")
NERO_TOKEN = os.getenv("NERO_BOT_TOKEN")
CLAIR_TOKEN = os.getenv("CLAIR_BOT_TOKEN")
CLAIR_ADMIN_ID = int(os.getenv("CLAIR_ADMIN_ID", "0"))

renova_bot = telebot.TeleBot(RENOVA_TOKEN)
nero_bot = telebot.TeleBot(NERO_TOKEN)
clair_bot = telebot.TeleBot(CLAIR_TOKEN) if CLAIR_TOKEN else None

SQUARE_TEXT_READING_URL = "https://square.link/u/yaq743A5"
SQUARE_VOICE_READING_URL = "https://square.link/u/oYibDkgK"
WEBSITE_URL = "https://www.renovaaetherandstone.com"
TELEGRAM_GROUP_URL = "https://t.me/+3ClNaQ3t5KJjZTJl"
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/LTIVL6u2QFl3zEzX2ARKNE"


def get_main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📜 Book a Reading", callback_data="menu_readings"),
        InlineKeyboardButton("🔮 About Jarrod & Practice", callback_data="menu_about"),
        InlineKeyboardButton("📖 Telegram Insights Group", url=TELEGRAM_GROUP_URL),
        InlineKeyboardButton("💬 WhatsApp Insights Community", url=WHATSAPP_GROUP_URL),
        InlineKeyboardButton("📞 Contact / PayID", callback_data="menu_contact"),
        InlineKeyboardButton("🌐 Open Interactive Site", web_app=WebAppInfo(url=WEBSITE_URL)),
    )
    return markup


def renova_welcome(message):
    welcome_text = (
        "✨ **Welcome to Renova Aether & Stone** ✨\n\n"
        "A grounded space for the intuitive work Jarrod has been finding his way back to.\n\n"
        "Clairaudient listening, tarot and oracle cards, geo-mediumship, empathy, and thoughtful reflection — with a little mystery and both feet near the ground.\n\n"
        "Choose an option below, and let’s see what is already speaking."
    )
    renova_bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu_markup(), parse_mode="Markdown")


renova_bot.message_handler(commands=["start", "menu"])(renova_welcome)


@renova_bot.callback_query_handler(func=lambda call: True)
def handle_menu_callbacks(call):
    if call.data == "menu_readings":
        text = (
            "✨ **CHOOSE YOUR READING FORMAT** ✨\n\n"
            "📜 **3-Question Text Reading ($25 AUD)**\n"
            "Share three questions and receive a focused written reading.\n\n"
            "🎙️ **15-Minute Voice Note Reading ($50 AUD)**\n"
            "A more spacious spoken reading delivered in Jarrod’s clear and considered voice."
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("💳 Pay $25 & Book Text Reading", url=SQUARE_TEXT_READING_URL),
            InlineKeyboardButton("💳 Pay $50 & Book Voice Reading", url=SQUARE_VOICE_READING_URL),
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main"),
        )
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "menu_about":
        text = (
            "🔮 **ABOUT JARROD & RENOVA AETHER & STONE**\n\n"
            "A reading practice rooted in attention.\n\n"
            "Jarrod works at the meeting point of intuitive listening and practical reflection. Through tarot, clairaudient insight, and the energetic character of a place, each reading makes room for the patterns that want to be noticed — without rushing toward certainty."
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📜 View Readings & Pricing", callback_data="menu_readings"),
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main"),
        )
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "menu_contact":
        text = "💬 **CONTACT & DIRECT PAYMENT**\n\n• **PayID:** `+61479129590`\n• **Website:** https://www.renovaaetherandstone.com"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📖 Join Telegram Insights Group", url=TELEGRAM_GROUP_URL),
            InlineKeyboardButton("💬 Join WhatsApp Community", url=WHATSAPP_GROUP_URL),
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main"),
        )
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "menu_main":
        text = "✨ **Welcome to Renova Aether & Stone** ✨\n\nA grounded space for intuitive listening, tarot, geographic energy and thoughtful reflection.\n\nChoose an option below, and let’s see what is already speaking."
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, text, reply_markup=get_main_menu_markup(), parse_mode="Markdown")


@nero_bot.message_handler(commands=["start"])
def nero_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🧪 Test Webview", web_app=WebAppInfo(url=WEBSITE_URL)))
    nero_bot.send_message(message.chat.id, "🧪 **Nero Sandbox Active**", reply_markup=markup, parse_mode="Markdown")


if clair_bot:
    @clair_bot.message_handler(commands=["start", "menu"])
    def clair_welcome(message):
        if CLAIR_ADMIN_ID and message.from_user.id == CLAIR_ADMIN_ID:
            text = (
                "🌙 **Welcome back, Jarrod.**\n\n"
                "What whispers do we have today?\n\n"
                "The listening room is open, the quiet threads are gathered, and I’m ready to help you tend to whatever has arrived."
            )
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("📜 New Reading Requests", callback_data="clair_requests"),
                InlineKeyboardButton("🔮 Continue a Conversation", callback_data="clair_conversations"),
                InlineKeyboardButton("🕯 Reading Status", callback_data="clair_status"),
                InlineKeyboardButton("🌙 Test the Flow", callback_data="clair_test"),
            )
        else:
            text = (
                "🌙 **Welcome to Clair.**\n\n"
                "I’m the private reading companion for Renova Aether & Stone. I’ll help prepare your questions for Jarrod.\n\n"
                "Take your time. You do not need to phrase anything perfectly."
            )
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton("🌐 Visit Renova Aether & Stone", url=WEBSITE_URL))
        clair_bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

    @clair_bot.callback_query_handler(func=lambda call: True)
    def clair_admin_callbacks(call):
        if not CLAIR_ADMIN_ID or call.from_user.id != CLAIR_ADMIN_ID:
            clair_bot.answer_callback_query(call.id, "This quiet room is reserved for Jarrod.")
            return
        if call.data == "clair_requests":
            response = "📜 **The listening room is waiting.**\n\nQuestion collection is the next thread to weave in."
        elif call.data == "clair_conversations":
            response = "🔮 **The threads are gathered.**\n\nConversation replies will be added here next."
        elif call.data == "clair_status":
            response = "🕯 **The candle is steady.**\n\nNo reading-status records are connected yet."
        else:
            response = "🌙 **The veil is thin.**\n\nCustomer question flow testing will be added next."
        clair_bot.answer_callback_query(call.id)
        clair_bot.send_message(call.message.chat.id, response, parse_mode="Markdown")


if __name__ == "__main__":
    threads = [
        threading.Thread(target=lambda: renova_bot.infinity_polling(), daemon=True),
        threading.Thread(target=lambda: nero_bot.infinity_polling(), daemon=True),
    ]
    if clair_bot:
        threads.append(threading.Thread(target=lambda: clair_bot.infinity_polling(), daemon=True))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
