import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from utils import check_all_pairs_and_send_signals, load_config, save_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()

def get_keyboard():
    buttons = [[InlineKeyboardButton(symbol, callback_data=symbol)] for symbol in config['symbols']]
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text(
    "👋 Привіт! Це крипто-бот.\nНатисни кнопку, щоб отримати сигнал для обраної монети:",
    reply_markup=get_keyboard()
)

async def signal(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Аналізую всі пари...")
    results = check_all_pairs_and_send_signals(config["symbols"])
    if results:
        await update.message.reply_text(results)
    else:
        await update.message.reply_text("⚠️ Сигналів не виявлено.")

async def button_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    symbol = query.data
    await query.edit_message_text(text=f"⏳ Аналізую {symbol}...")
    result = check_all_pairs_and_send_signals([symbol])
    if result:
        await query.message.reply_text(result)
    else:
        await query.message.reply_text("⚠️ Сигналів не виявлено.")

def main():
    application = Application.builder().token(config["token"]).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("signal", signal))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
