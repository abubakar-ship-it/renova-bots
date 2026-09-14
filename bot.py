import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

RENOVA_TOKEN = os.getenv("RENOVA_BOT_TOKEN")
NERO_TOKEN = os.getenv("NERO_BOT_TOKEN")
CLAIR_TOKEN = os.getenv("CLAIR_BOT_TOKEN")
CLAIR_ADMIN_ID = int(os.getenv("CLAIR_ADMIN_ID", "0"))
CLAIR_ADMIN_USERNAME = "renovaaetherstone"

renova_bot = telebot.TeleBot(RENOVA_TOKEN)
nero_bot = telebot.TeleBot(NERO_TOKEN)
clair_bot = telebot.TeleBot(CLAIR_TOKEN) if CLAIR_TOKEN else None

SQUARE_TEXT_READING_URL = "https://square.link/u/yaq743A5"
SQUARE_VOICE_READING_URL = "https://square.link/u/oYibDkgK"
WEBSITE_URL = "https://www.renovaaetherandstone.com"
TELEGRAM_GROUP_URL = "https://t.me/+3ClNaQ3t5KJjZTJl"
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/LTIVL6u2QFl3zEzX2ARKNE"
CLAIR_SESSIONS = {}

def get_main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("📜 Book a Reading", callback_data="menu_readings"), InlineKeyboardButton("🔮 About Jarrod & Practice", callback_data="menu_about"), InlineKeyboardButton("📖 Telegram Insights Group", url=TELEGRAM_GROUP_URL), InlineKeyboardButton("💬 WhatsApp Insights Community", url=WHATSAPP_GROUP_URL), InlineKeyboardButton("📞 Contact / PayID", callback_data="menu_contact"), InlineKeyboardButton("🌐 Open Interactive Site", web_app=WebAppInfo(url=WEBSITE_URL)))
    return markup

def renova_welcome(message):
    text = "✨ **Welcome to Renova Aether & Stone** ✨\n\nA grounded space for intuitive listening, tarot, geographic energy and thoughtful reflection.\n\nChoose an option below, and let’s see what is already speaking."
    renova_bot.send_message(message.chat.id, text, reply_markup=get_main_menu_markup(), parse_mode="Markdown")
renova_bot.message_handler(commands=["start", "menu"])(renova_welcome)

@renova_bot.callback_query_handler(func=lambda call: True)
def handle_menu_callbacks(call):
    if call.data == "menu_readings":
        text = "✨ **CHOOSE YOUR READING FORMAT** ✨\n\n📜 **3-Question Text Reading ($25 AUD)**\nShare three questions and receive a focused written reading.\n\n🎙️ **15-Minute Voice Note Reading ($50 AUD)**\nA more spacious spoken reading delivered in Jarrod’s clear and considered voice."
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("💳 Pay $25 & Book Text Reading", url=SQUARE_TEXT_READING_URL), InlineKeyboardButton("💳 Pay $50 & Book Voice Reading", url=SQUARE_VOICE_READING_URL), InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main"))
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "menu_about":
        text = "🔮 **ABOUT JARROD & RENOVA AETHER & STONE**\n\nA reading practice rooted in attention.\n\nJarrod works at the meeting point of intuitive listening and practical reflection. Through tarot, clairaudient insight, and the energetic character of a place, each reading makes room for the patterns that want to be noticed."
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("📜 View Readings & Pricing", callback_data="menu_readings"), InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main"))
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "menu_contact":
        text = "💬 **CONTACT & DIRECT PAYMENT**\n\n• **PayID:** `+61479129590`\n• **Website:** https://www.renovaaetherandstone.com"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("📖 Join Telegram Insights Group", url=TELEGRAM_GROUP_URL), InlineKeyboardButton("💬 Join WhatsApp Community", url=WHATSAPP_GROUP_URL), InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_main"))
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "menu_main":
        renova_bot.edit_message_text(call.message.chat.id, call.message.message_id, "✨ **Welcome to Renova Aether & Stone** ✨\n\nA grounded space for intuitive listening, tarot, geographic energy and thoughtful reflection.", reply_markup=get_main_menu_markup(), parse_mode="Markdown")

@nero_bot.message_handler(commands=["start"])
def nero_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🧪 Test Webview", web_app=WebAppInfo(url=WEBSITE_URL)))
    nero_bot.send_message(message.chat.id, "🧪 **Nero Sandbox Active**", reply_markup=markup, parse_mode="Markdown")

if clair_bot:
    @clair_bot.message_handler(commands=["start", "menu"])
    def clair_welcome(message):
        is_admin = ((CLAIR_ADMIN_ID and message.from_user.id == CLAIR_ADMIN_ID) or (message.from_user.username or "").lower() == CLAIR_ADMIN_USERNAME)
        if is_admin:
            text = "🌙 **Welcome back, Jarrod.**\n\nWhat whispers do we have today?\n\nThe listening room is open, the quiet threads are gathered, and I’m ready to help you tend to whatever has arrived."
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton("📜 New Reading Requests", callback_data="clair_requests"), InlineKeyboardButton("🔮 Continue a Conversation", callback_data="clair_conversations"), InlineKeyboardButton("🕯 Reading Status", callback_data="clair_status"), InlineKeyboardButton("🌙 Test the Flow", callback_data="clair_test"))
        else:
            text = "🌙 **Welcome to Clair.**\n\nI’m the private reading companion for Renova Aether & Stone. I’ll help prepare your questions for Jarrod.\n\nTake your time. You do not need to phrase anything perfectly."
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton("🔮 3-Question Text Reading", callback_data="clair_text"), InlineKeyboardButton("🎙️ 15-Minute Voice Note", callback_data="clair_voice"), InlineKeyboardButton("🌐 Visit Renova Aether & Stone", url=WEBSITE_URL))
        clair_bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

    @clair_bot.message_handler(func=lambda message: bool(message.text) and not message.text.startswith("/"))
    def clair_customer_message(message):
        session = CLAIR_SESSIONS.get(message.from_user.id)
        if not session: return
        if session["stage"] == "questions":
            session["questions"].append(message.text)
            count = len(session["questions"])
            if count < 3:
                clair_bot.send_message(message.chat.id, f"Thank you — I’ve received question {count} of 3.\n\nPlease send question {count + 1}.")
            else:
                session["stage"] = "review"
                q = session["questions"]
                review = f"🌙 Your three questions are gathered.\n\n1. {q[0]}\n\n2. {q[1]}\n\n3. {q[2]}\n\nWould you like to send these through to Jarrod?"
                markup = InlineKeyboardMarkup(row_width=1)
                markup.add(InlineKeyboardButton("✅ Send to Jarrod", callback_data="clair_submit"), InlineKeyboardButton("🔄 Start Again", callback_data="clair_restart"))
                clair_bot.send_message(message.chat.id, review, reply_markup=markup)
        elif session["stage"] == "voice":
            session["context"] = message.text
            session["stage"] = "review"
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton("✅ Send to Jarrod", callback_data="clair_submit"), InlineKeyboardButton("🔄 Start Again", callback_data="clair_restart"))
            clair_bot.send_message(message.chat.id, "🌙 I’ve gathered your voice-note request.\n\nWould you like me to send it through to Jarrod?", reply_markup=markup)

    @clair_bot.callback_query_handler(func=lambda call: True)
    def clair_admin_callbacks(call):
        if call.data == "clair_text":
            CLAIR_SESSIONS[call.from_user.id] = {"stage": "questions", "questions": [], "service": "3-Question Text Reading"}
            clair_bot.answer_callback_query(call.id)
            clair_bot.send_message(call.message.chat.id, "Lovely. I’ll collect three questions for your text reading.\n\nPlease send your first question.")
            return
        if call.data == "clair_voice":
            CLAIR_SESSIONS[call.from_user.id] = {"stage": "voice", "questions": [], "service": "15-Minute Voice Note Reading"}
            clair_bot.answer_callback_query(call.id)
            clair_bot.send_message(call.message.chat.id, "Wonderful. Send one main question, related thoughts, or simply say ‘general reading’. You may also send a Telegram voice message.")
            return
        if call.data == "clair_restart":
            CLAIR_SESSIONS.pop(call.from_user.id, None)
            clair_bot.answer_callback_query(call.id)
            clair_bot.send_message(call.message.chat.id, "The thread has been cleared. Choose your reading again with /start.")
            return
        if call.data == "clair_submit":
            CLAIR_SESSIONS.get(call.from_user.id, {})["stage"] = "submitted"
            clair_bot.answer_callback_query(call.id)
            clair_bot.send_message(call.message.chat.id, "Thank you — your request has been gathered and is ready for Jarrod. He will return to you during standard hours, usually within 3–4 hours.")
            return
        is_admin = ((CLAIR_ADMIN_ID and call.from_user.id == CLAIR_ADMIN_ID) or (call.from_user.username or "").lower() == CLAIR_ADMIN_USERNAME)
        if not is_admin:
            clair_bot.answer_callback_query(call.id, "This quiet room is reserved for Jarrod.")
            return
        if call.data == "clair_requests": response = "📜 **The listening room is waiting.**"
        elif call.data == "clair_conversations": response = "🔮 **The threads are gathered.**"
        elif call.data == "clair_status": response = "🕯 **The candle is steady.**"
        elif call.data == "clair_test":
            clair_bot.answer_callback_query(call.id)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton("🔮 3-Question Text Reading", callback_data="clair_text"), InlineKeyboardButton("🎙️ 15-Minute Voice Note", callback_data="clair_voice"), InlineKeyboardButton("🔙 Back to Jarrod’s Menu", callback_data="clair_admin_menu"))
            clair_bot.send_message(call.message.chat.id, "🌙 **Customer Flow Test**\n\nChoose the reading path you want to test:", reply_markup=markup, parse_mode="Markdown")
            return
        elif call.data == "clair_admin_menu":
            clair_bot.answer_callback_query(call.id)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton("📜 New Reading Requests", callback_data="clair_requests"), InlineKeyboardButton("🔮 Continue a Conversation", callback_data="clair_conversations"), InlineKeyboardButton("🕯 Reading Status", callback_data="clair_status"), InlineKeyboardButton("🌙 Test the Flow", callback_data="clair_test"))
            clair_bot.send_message(call.message.chat.id, "🌙 **Welcome back, Jarrod.**\n\nThe listening room is open.", reply_markup=markup, parse_mode="Markdown")
            return
        else: response = "🌙 **The veil is thin.**\n\nChoose Test the Flow to preview the customer menu."
        clair_bot.answer_callback_query(call.id)
        clair_bot.send_message(call.message.chat.id, response, parse_mode="Markdown")

if __name__ == "__main__":
    threads = [threading.Thread(target=lambda: renova_bot.infinity_polling(), daemon=True), threading.Thread(target=lambda: nero_bot.infinity_polling(), daemon=True)]
    if clair_bot: threads.append(threading.Thread(target=lambda: clair_bot.infinity_polling(), daemon=True))
    for thread in threads: thread.start()
    for thread in threads: thread.join()
