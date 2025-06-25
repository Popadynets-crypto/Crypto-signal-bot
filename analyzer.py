
import requests
import pandas as pd

def analyze_symbol(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=50"
        data = requests.get(url).json()
        closes = [float(candle[4]) for candle in data]
        df = pd.DataFrame(closes, columns=["close"])
        rsi = df["close"].pct_change().apply(lambda x: x if x > 0 else 0).rolling(14).mean().iloc[-1] * 100
        return f"Ціна: {closes[-1]:.4f} USDT\nRSI: {rsi:.2f}"
    except Exception as e:
        return f"Помилка: {e}"
