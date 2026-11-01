"""ดึงราคา ETF จาก Yahoo แล้วคำนวณ RSI(14), Stochastic(14,3,3), EMA12/26 ราย D/W/M -> etf_data.json
ใช้: python fetch_etf.py [TICKER ...]   (ไม่ใส่ = ชุดมาตรฐาน 12 ตัว + extra_tickers.txt ถ้ามี)"""
import json, os, sys, datetime as dt
import pandas as pd, yfinance as yf

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = ["SPY","QQQ","VTI","VOO","VEA","VWO","IWM","GLD","TLT","SCHD","VNQ","XLK"]
TFS = {"D": None, "W": "W-FRI", "M": "ME"}
TAIL = 160  # แท่งที่เก็บไว้วาดกราฟต่อ TF


def rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn)


def stoch(h, l, c, n=14, k=3, d=3):
    ll, hh = l.rolling(n).min(), h.rolling(n).max()
    fast = 100 * (c - ll) / (hh - ll)
    K = fast.rolling(k).mean()
    return K, K.rolling(d).mean()


def analyse(df):
    c = df["Close"]
    e12, e26 = c.ewm(span=12, adjust=False).mean(), c.ewm(span=26, adjust=False).mean()
    R = rsi(c); K, D = stoch(df["High"], df["Low"], c)
    diff = e12 - e26
    cross = None
    sgn = diff.apply(lambda x: 0 if pd.isna(x) else (1 if x > 0 else -1))
    for i in range(len(sgn) - 1, 25, -1):
        if sgn.iloc[i] != sgn.iloc[i-1]:
            cross = {"type": "golden" if sgn.iloc[i] > 0 else "death", "date": df.index[i].strftime("%Y-%m-%d"), "bars_ago": len(sgn) - 1 - i}
            break
    # stoch cross ล่าสุดภายใน 3 แท่ง
    sx = None
    for i in range(len(K) - 1, max(len(K) - 4, 1), -1):
        if pd.notna(K.iloc[i]) and pd.notna(D.iloc[i]) and pd.notna(K.iloc[i-1]) and pd.notna(D.iloc[i-1]):
            if K.iloc[i-1] <= D.iloc[i-1] and K.iloc[i] > D.iloc[i]: sx = ("up", K.iloc[i]); break
            if K.iloc[i-1] >= D.iloc[i-1] and K.iloc[i] < D.iloc[i]: sx = ("down", K.iloc[i]); break
    r, k, dd = R.iloc[-1], K.iloc[-1], D.iloc[-1]
    s_rsi = None if pd.isna(r) else (1 if r < 30 else -1 if r > 70 else 0)
    s_sto = None if pd.isna(k) else (1 if sx and sx[0] == "up" and sx[1] < 20 else -1 if sx and sx[0] == "down" and sx[1] > 80 else 0)
    s_ema = None if pd.isna(diff.iloc[-1]) else (1 if cross and cross["type"] == "golden" and cross["bars_ago"] <= 5 else -1 if cross and cross["type"] == "death" and cross["bars_ago"] <= 5 else 0)
    trend = None if pd.isna(diff.iloc[-1]) else (1 if diff.iloc[-1] > 0 else -1)
    sig = [s for s in (s_rsi, s_sto, s_ema) if s is not None]
    score = sum(sig) if sig else None
    t = df.tail(TAIL)
    f = lambda s: [None if pd.isna(x) else round(float(x), 3) for x in s.tail(TAIL)]
    return {
        "last_date": df.index[-1].strftime("%Y-%m-%d"), "close": round(float(c.iloc[-1]), 3),
        "rsi": None if pd.isna(r) else round(float(r), 1),
        "stoch_k": None if pd.isna(k) else round(float(k), 1), "stoch_d": None if pd.isna(dd) else round(float(dd), 1),
        "ema12": round(float(e12.iloc[-1]), 3), "ema26": round(float(e26.iloc[-1]), 3),
        "trend": trend, "cross": cross,
        "sig": {"rsi": s_rsi, "stoch": s_sto, "ema": s_ema}, "score": score,
        "verdict": None if score is None else ("Buy" if score >= 1 else "Sell" if score <= -1 else "Neutral"),
        "chart": {"d": [x.strftime("%Y-%m-%d") for x in t.index], "c": f(t["Close"]), "e12": f(e12), "e26": f(e26)},
    }


def main():
    tk = [a.upper() for a in sys.argv[1:]] or DEFAULT
    ex = os.path.join(HERE, "extra_tickers.txt")
    if len(sys.argv) == 1 and os.path.exists(ex):
        tk += [x.strip().upper() for x in open(ex).read().replace(",", "\n").split() if x.strip()]
    tk = list(dict.fromkeys(tk))
    out, fail = {}, {}
    for t in tk:
        try:
            df = yf.Ticker(t).history(period="max", interval="1d", auto_adjust=True)
            df = df.dropna(subset=["Close"]).tail(5000)
            if len(df) < 60: raise ValueError("ข้อมูลน้อยกว่า 60 วัน")
            df.index = df.index.tz_localize(None)
            res = {}
            for tf, rule in TFS.items():
                x = df if rule is None else df.resample(rule).agg({"Open":"first","High":"max","Low":"min","Close":"last"}).dropna()
                res[tf] = analyse(x) if len(x) >= 40 else None
            out[t] = res
            print(t, "ok", df.index[-1].date())
        except Exception as e:
            fail[t] = str(e); print(t, "FAIL", e)
    meta = {"source": "Yahoo Finance (yfinance, ราคาปรับปันผล/split)", "fetched_ict": (dt.datetime.utcnow() + dt.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M"),
            "params": "RSI 14 (Wilder) · Stoch 14,3,3 · EMA 12/26 · W=จบวันศุกร์ · M=สิ้นเดือน (แท่งสุดท้ายอาจยังไม่ปิด)", "failed": fail}
    json.dump({"meta": meta, "etfs": out}, open(os.path.join(HERE, "etf_data.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("saved", len(out), "failed", len(fail))

if __name__ == "__main__":
    main()
