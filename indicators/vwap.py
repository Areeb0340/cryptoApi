import pandas as pd


def calculate_vwap(highs, lows, closes, volumes):

    df = pd.DataFrame(
        {
            "high": pd.Series(highs, dtype=float),
            "low": pd.Series(lows, dtype=float),
            "close": pd.Series(closes, dtype=float),
            "volume": pd.Series(volumes, dtype=float),
        }
    )

    # Typical Price
    df["tp"] = (df["high"] + df["low"] + df["close"]) / 3

    # TP × Volume
    df["tpv"] = df["tp"] * df["volume"]

    # Running VWAP
    df["cum_tpv"] = df["tpv"].cumsum()
    df["cum_volume"] = df["volume"].cumsum()

    df["vwap"] = df["cum_tpv"] / df["cum_volume"]

    return df["vwap"]


def analyze_vwap(highs, lows, closes, volumes):
    if len(closes) < 50:
        raise ValueError("At least 50 candles are required.")

    closes = pd.Series(closes, dtype=float)

    vwap = calculate_vwap(highs, lows, closes, volumes)

    latest_price = float(closes.iloc[-1])
    latest_vwap = float(vwap.iloc[-1])

    distance = ((latest_price - latest_vwap) / latest_vwap) * 100

    distance = round(distance, 2)

    price_above = latest_price > latest_vwap
    price_below = latest_price < latest_vwap

    cross_up = closes.iloc[-2] < vwap.iloc[-2] and closes.iloc[-1] > vwap.iloc[-1]

    cross_down = closes.iloc[-2] > vwap.iloc[-2] and closes.iloc[-1] < vwap.iloc[-1]

    slope = float(vwap.iloc[-1] - vwap.iloc[-2])

    if slope > 0:
        vwap_trend = "Rising"

    elif slope < 0:
        vwap_trend = "Falling"

    else:
        vwap_trend = "Flat"

    if abs(distance) < 0.30:
        zone = "At VWAP"

    elif distance > 0:
        zone = "Premium"

    else:
        zone = "Discount"

    if abs(distance) < 0.25:

        distance_zone = "NEAR"

    elif abs(distance) < 1:

        distance_zone = "NORMAL"

    elif abs(distance) < 3:

        distance_zone = "FAR"

    else:
        distance_zone = "EXTREME"

    institutional_buy_zone = price_above and vwap_trend == "Rising"

    institutional_sell_zone = price_below and vwap_trend == "Falling"

    ai_score = 50

    if institutional_buy_zone:
        ai_score += 20

    if institutional_sell_zone:
        ai_score -= 20

    if cross_up:
        ai_score += 15

    if cross_down:
        ai_score -= 15

    if abs(distance) < 0.50:
        ai_score += 5

    ai_score = max(0, min(100, ai_score))

    if institutional_buy_zone:

        trend = "Bullish"

    elif institutional_sell_zone:

        trend = "Bearish"

    elif price_above:

        trend = "Bullish Bias"

    else:

        trend = "Bearish Bias"

    return {
        "vwap": round(latest_vwap, 2),
        "price": round(latest_price, 2),
        "distance_percent": distance,
        "price_above_vwap": price_above,
        "price_below_vwap": price_below,
        "cross_up": cross_up,
        "cross_down": cross_down,
        "vwap_slope": round(slope, 4),
        "vwap_trend": vwap_trend,
        "zone": zone,
        "institutional_buy_zone": institutional_buy_zone,
        "institutional_sell_zone": institutional_sell_zone,
        "trend": trend,
        "ai_score": ai_score,
    }
