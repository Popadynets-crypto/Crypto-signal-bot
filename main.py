from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes import config import analyzer import asyncio

Клавіатура з монетами

def get_keyboard(): buttons = [[InlineKeyboardButton(symbol, callback_data=symbol)] for symbol in config.symbols] return InlineKeyboardMarkup(buttons)

Команда /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "Привіт! Я бот для аналізу монет. Обери монету:", reply_markup=get_keyboard() )

Кнопка аналізу

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() symbol = query.data result = analyzer.analyze_symbol(symbol) await query.edit_message_text(text=f"Результат для {symbol}: {result}")

Команда /getid

async def get_id(update: Update, context): chat_id = update.effective_chat.id await update.message.reply_text(f"Твій chat_id: {chat_id}")

Автоматичний аналіз кожні N хвилин

async def auto_analyze(app): while True: for symbol in config.symbols: try: result = analyzer.analyze_symbol(symbol) if isinstance(result, dict) and result.get("signal") in ["buy", "sell"]: message = f"🔔 {symbol.upper()}: {result['signal'].upper()} сигнал!\n{result.get('details', '')}" await app.bot.send_message(chat_id=config.ALERT_CHAT_ID, text=message) except Exception as e: print(f"Помилка при аналізі {symbol}: {e}") await asyncio.sleep(config.ANALYSIS_INTERVAL_MINUTES * 60)

def main(): app = ApplicationBuilder().token(config.BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getid", get_id))
app.add_handler(CallbackQueryHandler(signal))

asyncio.create_task(auto_analyze(app))  # запуск автоаналізу

app.run_polling()

if name == "main": main()

