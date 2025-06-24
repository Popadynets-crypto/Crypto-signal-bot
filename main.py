from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import config
import analyzer

def get_keyboard():
    buttons = [[InlineKeyboardButton(symbol, callback_data=symbol)] for symbol in config.symbols]
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот для аналізу монет. Обери монету:",
        reply_markup=get_keyboard()
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    symbol = query.data
    result = analyzer.analyze_symbol(symbol)
    await query.edit_message_text(text=f"Результат для {symbol}:\n{result}")

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(signal))
    app.run_polling()

if __name__ == "__main__":
    main()
