import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

RENOVA_TOKEN = os.getenv("RENOVA_BOT_TOKEN")
NERO_TOKEN = os.getenv("NERO_BOT_TOKEN")
CLAIR_TOKEN = os.getenv("CLAIR_BOT_TOKEN")
CLAIR_ADMIN_ID = int(os.getenv("CLAIR_ADMIN_ID", "8664218481"))
CLAIR_ADMIN_USERNAME = "renovaaetherstone"
WEBSITE_URL = "https://www.renovaaetherandstone.com"
TEXT_URL = "https://square.link/u/yaq743A5"
VOICE_URL = "https://square.link/u/oYibDkgK"
TELEGRAM_GROUP_URL = "https://t.me/+3ClNaQ3t5KJjZTJl"
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/LTIVL6u2QFl3zEzX2ARKNE"
SESSIONS = {}

renova_bot = telebot.TeleBot(RENOVA_TOKEN)
nero_bot = telebot.TeleBot(NERO_TOKEN)
clair_bot = telebot.TeleBot(CLAIR_TOKEN) if CLAIR_TOKEN else None

def customer_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add(KeyboardButton("🔮 3-Question Text Reading"), KeyboardButton("🎙️ 15-Minute Voice Note"))
    m.add(KeyboardButton("🌐 Renova Website"), KeyboardButton("❓ Help"))
    return m

def admin_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add(KeyboardButton("📜 New Reading Requests"), KeyboardButton("🕯 Reading Status"))
    m.add(KeyboardButton("🌙 Test Customer Flow"), KeyboardButton("💬 Main Menu"))
    return m

def renova_menu():
    m = InlineKeyboardMarkup(row_width=1)
    m.add(InlineKeyboardButton("📜 Book a Reading", callback_data="renova_readings"), InlineKeyboardButton("🔮 About Jarrod & Practice", callback_data="renova_about"), InlineKeyboardButton("📖 Telegram Insights Group", url=TELEGRAM_GROUP_URL), InlineKeyboardButton("💬 WhatsApp Insights Community", url=WHATSAPP_GROUP_URL), InlineKeyboardButton("📞 Contact / PayID", callback_data="renova_contact"), InlineKeyboardButton("🌐 Open Interactive Site", web_app=WebAppInfo(url=WEBSITE_URL)))
    return m

@renova_bot.message_handler(commands=["start", "menu"])
def renova_start(message):
    renova_bot.send_message(message.chat.id, "✨ **Welcome to Renova Aether & Stone** ✨\n\nA grounded space for intuitive listening, tarot, geographic energy and thoughtful reflection.", reply_markup=renova_menu(), parse_mode="Markdown")

@renova_bot.callback_query_handler(func=lambda call: call.data.startswith("renova_"))
def renova_callbacks(call):
    if call.data == "renova_readings":
        text = "✨ **CHOOSE YOUR READING FORMAT** ✨\n\n📜 **3-Question Text Reading — $25 AUD**\nA focused written reading for three questions.\n\n🎙️ **15-Minute Voice Note Reading — $50 AUD**\nA spacious spoken reading delivered by Jarrod."
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("💳 Pay $25 & Book Text Reading", url=TEXT_URL), InlineKeyboardButton("💳 Pay $50 & Book Voice Reading", url=VOICE_URL), InlineKeyboardButton("🔙 Back to Main Menu", callback_data="renova_main"))
    elif call.data == "renova_about":
        text = "🔮 **ABOUT JARROD & RENOVA AETHER & STONE**\n\nA reading practice rooted in intuitive listening, tarot, geographic energy and grounded reflection."
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📜 View Readings & Pricing", callback_data="renova_readings"), InlineKeyboardButton("🔙 Back to Main Menu", callback_data="renova_main"))
    elif call.data == "renova_contact":
        text = "💬 **CONTACT & DIRECT PAYMENT**\n\nPayID: `+61479129590`"
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📖 Telegram Insights Group", url=TELEGRAM_GROUP_URL), InlineKeyboardButton("💬 WhatsApp Community", url=WHATSAPP_GROUP_URL), InlineKeyboardButton("🔙 Back to Main Menu", callback_data="renova_main"))
    else:
        text = "✨ **Welcome to Renova Aether & Stone** ✨\n\nChoose an option below, and let’s see what is already speaking."
        m = renova_menu()
    renova_bot.answer_callback_query(call.id)
    renova_bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=m, parse_mode="Markdown")

@nero_bot.message_handler(commands=["start"])
def nero_start(message):
    m = InlineKeyboardMarkup(); m.add(InlineKeyboardButton("🧪 Test Webview", web_app=WebAppInfo(url=WEBSITE_URL)))
    nero_bot.send_message(message.chat.id, "🧪 **Nero Sandbox Active**", reply_markup=m, parse_mode="Markdown")

if clair_bot:
    @clair_bot.message_handler(commands=["start", "menu"])
    def clair_start(message):
        admin = message.from_user.id == CLAIR_ADMIN_ID or (message.from_user.username or "").lower() == CLAIR_ADMIN_USERNAME
        if admin:
            clair_bot.send_message(message.chat.id, "🌙 **Welcome back, Jarrod.**\n\nWhat whispers do we have today?", reply_markup=admin_menu(), parse_mode="Markdown")
        else:
            clair_bot.send_message(message.chat.id, "🌙 **Welcome to Clair.**\n\nChoose the reading path you would like to begin.", reply_markup=customer_menu(), parse_mode="Markdown")

    @clair_bot.message_handler(func=lambda message: True, content_types=["text"])
    def clair_text(message):
        admin = message.from_user.id == CLAIR_ADMIN_ID or (message.from_user.username or "").lower() == CLAIR_ADMIN_USERNAME
        text = message.text
        if admin and text == "📜 New Reading Requests":
            clair_bot.send_message(message.chat.id, "📜 **The listening room is waiting.**", reply_markup=admin_menu(), parse_mode="Markdown"); return
        if admin and text == "🕯 Reading Status":
            clair_bot.send_message(message.chat.id, "🕯 **The candle is steady.**", reply_markup=admin_menu(), parse_mode="Markdown"); return
        if admin and text == "🌙 Test Customer Flow":
            clair_bot.send_message(message.chat.id, "🌙 **Customer Flow Test**\n\nChoose the reading path:", reply_markup=customer_menu(), parse_mode="Markdown"); return
        if admin and text == "💬 Main Menu": clair_start(message); return
        if text == "🔮 3-Question Text Reading":
            SESSIONS[message.from_user.id] = {"stage": "questions", "questions": [], "service": "3-Question Text Reading"}; clair_bot.send_message(message.chat.id, "Lovely. Please send your first question."); return
        if text == "🎙️ 15-Minute Voice Note":
            SESSIONS[message.from_user.id] = {"stage": "voice", "service": "15-Minute Voice Note Reading"}; clair_bot.send_message(message.chat.id, "Wonderful. Send one main question or say ‘general reading’."); return
        if text == "🌐 Renova Website": clair_bot.send_message(message.chat.id, WEBSITE_URL); return
        if text == "❓ Help": clair_bot.send_message(message.chat.id, "Choose a reading, answer Clair’s prompts, review your request, then tap Send to Jarrod."); return
        session = SESSIONS.get(message.from_user.id)
        if not session: return
        if session["stage"] == "questions":
            session["questions"].append(text); n = len(session["questions"])
            if n < 3: clair_bot.send_message(message.chat.id, f"Thank you — question {n} of 3 received.\n\nPlease send question {n + 1}.")
            else:
                session["stage"] = "review"; q = session["questions"]; m = InlineKeyboardMarkup(row_width=1); m.add(InlineKeyboardButton("✅ Send to Jarrod", callback_data="submit"), InlineKeyboardButton("🔄 Start Again", callback_data="restart")); clair_bot.send_message(message.chat.id, f"🌙 Your questions are gathered.\n\n1. {q[0]}\n\n2. {q[1]}\n\n3. {q[2]}\n\nSend these through to Jarrod?", reply_markup=m)
        elif session["stage"] == "voice":
            session["context"] = text; session["stage"] = "review"; m = InlineKeyboardMarkup(row_width=1); m.add(InlineKeyboardButton("✅ Send to Jarrod", callback_data="submit"), InlineKeyboardButton("🔄 Start Again", callback_data="restart")); clair_bot.send_message(message.chat.id, "🌙 I’ve gathered your request. Send it through to Jarrod?", reply_markup=m)

    @clair_bot.callback_query_handler(func=lambda call: True)
    def clair_callbacks(call):
        if call.data == "restart": SESSIONS.pop(call.from_user.id, None); clair_bot.answer_callback_query(call.id); clair_bot.send_message(call.message.chat.id, "The thread has been cleared. Choose a reading below.", reply_markup=customer_menu()); return
        if call.data == "submit":
            session = SESSIONS.get(call.from_user.id, {}); user = call.from_user; name = " ".join(filter(None, [user.first_name, user.last_name])) or "Unknown client"; username = "@" + user.username if user.username else "No username"
            if session.get("service") == "3-Question Text Reading": content = "\n\n".join(f"Question {i}: {q}" for i, q in enumerate(session.get("questions", []), 1)); heading = "🔮 NEW 3-QUESTION READING REQUEST"
            else: content = session.get("context", "General reading"); heading = "🎙️ NEW VOICE NOTE READING REQUEST"
            clair_bot.send_message(CLAIR_ADMIN_ID, f"{heading}\n\nClient: {name}\nUsername: {username}\nTelegram ID: {user.id}\nService: {session.get('service', 'Reading')}\n\n{content}"); clair_bot.answer_callback_query(call.id); clair_bot.send_message(call.message.chat.id, "Thank you — your request has been sent through to Jarrod. He’ll return to you during standard hours.", reply_markup=customer_menu()); return

    @clair_bot.message_handler(content_types=["voice"])
    def clair_voice(message):
        session = SESSIONS.get(message.from_user.id)
        if session and session.get("stage") == "voice":
            session["voice_file_id"] = message.voice.file_id; session["stage"] = "review"; m = InlineKeyboardMarkup(row_width=1); m.add(InlineKeyboardButton("✅ Send to Jarrod", callback_data="submit"), InlineKeyboardButton("🔄 Start Again", callback_data="restart")); clair_bot.send_message(message.chat.id, "🌙 I’ve received your voice note. Send it through to Jarrod?", reply_markup=m)

if __name__ == "__main__":
    threads = [threading.Thread(target=renova_bot.infinity_polling, daemon=True), threading.Thread(target=nero_bot.infinity_polling, daemon=True)]
    if clair_bot: threads.append(threading.Thread(target=clair_bot.infinity_polling, daemon=True))
    for thread in threads: thread.start()
    for thread in threads: thread.join()
