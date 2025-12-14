import pandas as pd
from indicators import rsi, macd

def scan_market():
    # نمونه دیتای قیمت (فعلاً شبیه‌سازی شده)
    data = {
        "فولاد": [24000,24500,25000,24800,25200,25500],
        "شپنا": [3900,3950,4020,3980,4050,4100],
        "پکویر": [680,690,700,705,710,720],
        "خودرو": [1700,1750,1800,1780,1820,1850]
    }

    results = []

    for symbol, prices in data.items():
        s = pd.Series(prices)

        r = rsi(s).iloc[-1]
        macd_line, signal_line = macd(s)

        if r < 30 and macd_line.iloc[-1] > signal_line.iloc[-1]:
            signal = "BUY"
            risk = "Medium"
        elif r > 70:
            signal = "SELL"
            risk = "High"
        else:
            signal = "HOLD"
            risk = "Low"

        results.append({
            "Symbol": symbol,
            "RSI": round(r, 1),
            "Signal": signal,
            "Risk": risk,
            "Style": "Adaptive"
        })

    return pd.DataFrame(results)
