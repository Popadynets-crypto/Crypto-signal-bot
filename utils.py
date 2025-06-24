import aiohttp
import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"symbols": ["BTCUSDT", "ETHUSDT", "PEPEUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT"]}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

async def check_all_pairs_and_send_signals(app, symbols):
    from telegram.constants import ParseMode
    async with aiohttp.ClientSession() as session:
        for symbol in symbols:
            try:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
                async with session.get(url) as response:
                    data = await response.json()
                    price = data["price"]
                    msg = f"📊 {symbol} поточна ціна: {price}"
                    for conv in app.chat_data.keys():
                        await app.bot.send_message(chat_id=conv, text=msg, parse_mode=ParseMode.HTML)
            except Exception as e:
                print(f"❌ Помилка: {symbol} — {e}")