import os
import json
import asyncio
from aiohttp import web
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8697311693:AAH4wkFkNR2F8EBSETarhpsPy2_wHAmCHtg"
WEBAPP_URL = "https://renova-bots-production-8d3b.up.railway.app/nero-app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton(text="🔮 Open Tarot Reader", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text(
        "Welcome to Renova! Tap the button below to draw a card:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.message.web_app_data.data)
    if data.get("action") == "tarot_selected":
        card = data.get("card")
        user = update.effective_user.first_name
        await update.message.reply_text(
            f"🔮 **Renova Reading for {user}** 🔮\n\n"
            f"You pulled: **{card}**!\n\n"
            "✨ *Spiritual Guidance:* Alignment and clarity are heading your way."
        )

async def handle_nero_app(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Renova Psychic Readings</title>
      <script src="https://telegram.org/js/telegram-web-app.js"></script>
      <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background: #0f0c1b; color: #e2d9f3; }
        h2 { color: #d4af37; }
        .card { border: 1px solid #d4af37; padding: 18px; border-radius: 14px; background: #130f24; margin: 15px 0; cursor: pointer; font-size: 18px; font-weight: bold; }
      </style>
    </head>
    <body>
      <h2>🔮 Renova Readings</h2>
      <p>Tap a card to reveal your guidance</p>
      <div class="card" onclick="selectCard('The Sun 🌞 (Joy & Clarity)')">🌞 The Sun</div>
      <div class="card" onclick="selectCard('The Moon 🌙 (Intuition & Secrets)')">🌙 The Moon</div>
      <div class="card" onclick="selectCard('The Star 🌟 (Hope & Inspiration)')">🌟 The Star</div>
      <script>
        const tg = window.Telegram.WebApp;
        tg.expand();
        function selectCard(card) {
          tg.sendData(JSON.stringify({ action: 'tarot_selected', card: card }));
          tg.close();
        }
      </script>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

async def main():
    app = web.Application()
    app.router.add_get('/nero-app', handle_nero_app)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    await web.TCPSite(runner, '0.0.0.0', port).start()

    tg_app = ApplicationBuilder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
