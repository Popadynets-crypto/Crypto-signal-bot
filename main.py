from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, symbols, ANALYSIS_INTERVAL_MINUTES
from analyzer import analyze_symbol
import asyncio

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(symbol, callback_data=symbol)] for symbol in symbols
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть монету для аналізу:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    symbol = query.data
    result = analyze_symbol(symbol)
    await query.edit_message_text(text=f"🔍 Результат аналізу {symbol}:
{result}")

async def auto_analysis(app):
    while True:
        for symbol in symbols:
            result = analyze_symbol(symbol)
            print(f"[AUTO] {symbol}: {result}")
        await asyncio.sleep(ANALYSIS_INTERVAL_MINUTES * 60)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.job_queue.run_once(lambda _: asyncio.create_task(auto_analysis(app)), 1)
    app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
