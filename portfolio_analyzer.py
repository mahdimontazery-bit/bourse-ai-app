import base64
import io
import pandas as pd

def analyze_portfolio(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))

    out = []

    for _, row in df.iterrows():
        buy = row["BuyPrice"]
        current = buy * 1.15  # فعلاً شبیه‌سازی
        profit_pct = ((current - buy) / buy) * 100

        if profit_pct > 20:
            decision = "SELL"
            sell_pct = 40
        elif profit_pct > 10:
            decision = "HOLD"
            sell_pct = 0
        else:
            decision = "HOLD"
            sell_pct = 0

        out.append({
            "Symbol": row["Symbol"],
            "Profit %": round(profit_pct, 1),
            "Decision": decision,
            "Sell %": sell_pct
        })

    return pd.DataFrame(out)
