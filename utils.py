import requests, json
from strategy import analyze_symbol

def get_usdt_pairs():
    r = requests.get('https://api.binance.com/api/v3/exchangeInfo').json()
    return [s['symbol'] for s in r['symbols'] if s['quoteAsset'] in ['USDT', 'USDC']]

async def check_all_pairs_and_send_signals(bot, chat_id):
    pairs = get_usdt_pairs()
    messages = []
    for symbol in pairs[:50]:
        try:
            signal = analyze_symbol(symbol)
            if signal:
                messages.append(signal)
        except:
            continue
    if not messages:
        await bot.send_message(chat_id, "🔍 Немає актуальних сигналів.")
    else:
        for msg in messages:
            await bot.send_message(chat_id, msg)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def save_config(cfg):
    with open("config.json", "w") as f:
        json.dump(cfg, f)