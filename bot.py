import os
import threading
import telebot

# Read environment variables from Railway
RENOVA_TOKEN = os.getenv(8846130755:AAF0rVmlfB_tWRQThaN0mCCzDj7yE_cFb0Q)
NERO_TOKEN = os.getenv(8697311693:AAG6qoatlCKvc8SKVoGGHd2SFgg0f-GzdCg)

renova_bot = telebot.TeleBot(RENOVA_TOKEN)
nero_bot = telebot.TeleBot(NERO_TOKEN)

# ==========================================
# 🌟 RENOVA CLIENT BOT (@RenovaAetherStone1Bot)
# ==========================================
@renova_bot.message_handler(commands=['start'])
def renova_start(message):
    welcome_text = (
        "✨ Welcome to Renova Aether & Stone!\n\n"
        "Grounded intuitive guidance, tarot analysis, and energy readings with Jarrod.\n\n"
        "Book a reading at: https://renovaaetherandstone.com"
    )
    renova_bot.send_message(message.chat.id, welcome_text)

# ==========================================
# 🧪 NERO TEST BOT (@Nerolabtestbot)
# ==========================================
@nero_bot.message_handler(commands=['start'])
def nero_start(message):
    nero_text = (
        "🧪 Nero Sandbox Active (@Nerolabtestbot)\n\n"
        "Ready to run test suites and evaluate Mini App features."
    )
    nero_bot.send_message(message.chat.id, nero_text)

# ==========================================
# 🚀 RUN BOTH BOTS
# ==========================================
if __name__ == "__main__":
    t1 = threading.Thread(target=lambda: renova_bot.infinity_polling(), daemon=True)
    t1.start()
    nero_bot.infinity_polling()
