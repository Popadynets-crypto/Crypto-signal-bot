import requests
import numpy as np

def analyze_symbol(symbol):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100'
    data = requests.get(url).json()
    closes = [float(c[4]) for c in data]
    volumes = [float(c[5]) for c in data]

    rsi = calculate_rsi(closes)[-1]
    avg_volume = np.mean(volumes[:-1])
    current_volume = volumes[-1]

    if rsi < 30 and current_volume > avg_volume * 1.5:
        return f"✅ [{symbol}] сигнал на купівлю:\nЦіна: {closes[-1]}\nRSI: {rsi:.2f}\nОбʼєм: {current_volume:.2f}"
    elif rsi > 70:
        return f"⚠️ [{symbol}] сигнал на продаж:\nЦіна: {closes[-1]}\nRSI: {rsi:.2f}"
    else:
        return None

def calculate_rsi(closes, period=14):
    deltas = np.diff(closes)
    gains = np.maximum(deltas, 0)
    losses = np.maximum(-deltas, 0)
    avg_gain = np.convolve(gains, np.ones(period), 'valid') / period
    avg_loss = np.convolve(losses, np.ones(period), 'valid') / period
    rs = avg_gain / (avg_loss + 1e-6)
    rsi = 100 - (100 / (1 + rs))
    return np.concatenate([[50]* (period-1), rsi])