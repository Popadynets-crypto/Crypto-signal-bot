from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import config
import analyzer
import asyncio


def get_keyboard():
    buttons = [
        [InlineKeyboardButton(symbol, callback_data=symbol)]
        for symbol in config.symbols
    ]
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот для аналізу монет. Обери монету для аналізу:",
        reply_markup=get_keyboard()
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    symbol = query.data
    result = analyzer.analyze_symbol(symbol)
    await query.edit_message_text(text=f"🔍 Аналіз {symbol}:\n{result}")


async def auto_analysis(app):
    while True:
        for symbol in config.symbols:
            result = analyzer.analyze_symbol(symbol)
            if "Покупка" in result or "Продаж" in result:
                try:
                    await app.bot.send_message(
                        chat_id=config.CHAT_ID,
                        text=f"📊 Сигнал по {symbol}:\n{result}"
                    )
                except Exception as e:
                    print(f"❌ Error sending message: {e}")
        await asyncio.sleep(config.ANALYSIS_INTERVAL_MINUTES * 60)


async def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(signal))

    # Запускаємо автоперевірку монет у фоновому режимі
    app.job_queue.run_once(lambda _: asyncio.create_task(auto_analysis(app)), 1)

    print("✅ Бот запущено")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
