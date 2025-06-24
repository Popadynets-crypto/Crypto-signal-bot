from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils import check_all_pairs_and_send_signals, load_config, save_config
import logging, threading
from flask import Flask

# Flask health-check
app_flask = Flask(__name__)

@app_flask.route('/')
def health():
    return 'OK', 200

def run_web():
    app_flask.run(host='0.0.0.0', port=8000)

web_thread = threading.Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

# Telegram bot
logging.basicConfig(level=logging.INFO)
config = load_config()

async def start(update, context):
    await update.message.reply_text("👋 Привіт! Це крипто-бот. Напиши /signal щоб отримати сигнали.")

async def signal(update, context):
    await update.message.reply_text("⏳ Аналізую ринок...")
    await check_all_pairs_and_send_signals(context.bot, update.effective_chat.id)

async def set_interval(update, context):
    try:
        minutes = int(context.args[0])
        config['scan_interval_minutes'] = minutes
        save_config(config)
        await update.message.reply_text(f"✅ Інтервал встановлено: {minutes} хв.")
    except:
        await update.message.reply_text("❌ Невірний формат. Приклад: /set_interval 60")

app_bot = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("signal", signal))
app_bot.add_handler(CommandHandler("set_interval", set_interval))
app_bot.run_polling()