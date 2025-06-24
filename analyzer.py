import os
import pandas as pd
import ta
import random

def analyze_symbol(symbol):
    # Тимчасова логіка — для тесту
    signals = ["Buy", "Sell", "No signal"]
    return random.choice(signals)
from binance.client import Client

def analyze_coin(symbol, interval='1h', limit=100):
    try:
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        if not api_key or not api_secret:
            raise ValueError("Binance API ключі не задані у середовищі")

        client = Client(api_key, api_secret)
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])

        df["close"] = pd.to_numeric(df["close"])

        # Обчислення RSI
        rsi_indicator = ta.momentum.RSIIndicator(close=df["close"], window=14)
        df["rsi"] = rsi_indicator.rsi()

        last_rsi = df["rsi"].iloc[-1]
        signal = ""
        if last_rsi < 30:
            signal = "BUY"
        elif last_rsi > 70:
            signal = "SELL"
        else:
            signal = "HOLD"

        return {
            "symbol": symbol,
            "signal": signal,
            "rsi": round(last_rsi, 2)
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "signal": "ERROR",
            "error": str(e)
        }
