import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils import check_all_pairs_and_send_signals, load_config, save_config
from flask import Flask, request

app_flask = Flask(__name__)

@app_flask.route('/')
def health_check():
    return "Bot is running."

@app_flask.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    if data:
        application.update_queue.put_nowait(data)
    return 'OK'

config = load_config()
symbols = config["symbols"]
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
application = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Бот аналізує ринок...")
    await check_all_pairs_and_send_signals(application, symbols)

application.add_handler(CommandHandler("start", start))

# Запуск бота через webhook
async def run():
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(url=os.environ.get("WEBHOOK_URL"))
    await application.updater.start_polling()
    app_flask.run(host="0.0.0.0", port=10000)

import asyncio
asyncio.run(run())