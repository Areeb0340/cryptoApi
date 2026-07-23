import pandas as pd


PERIOD = 14


def calculate_mfi(highs, lows, closes, volumes, period=PERIOD):

    high = pd.Series(highs, dtype=float)
    low = pd.Series(lows, dtype=float)
    close = pd.Series(closes, dtype=float)
    volume = pd.Series(volumes, dtype=float)

    typical_price = (high + low + close) / 3

    money_flow = typical_price * volume

    positive_flow = [0]
    negative_flow = [0]

    for i in range(1, len(typical_price)):

        if typical_price.iloc[i] > typical_price.iloc[i - 1]:
            positive_flow.append(money_flow.iloc[i])
            negative_flow.append(0)

        elif typical_price.iloc[i] < typical_price.iloc[i - 1]:
            positive_flow.append(0)
            negative_flow.append(money_flow.iloc[i])

        else:
            positive_flow.append(0)
            negative_flow.append(0)

    positive_flow = pd.Series(positive_flow)
    negative_flow = pd.Series(negative_flow)

    positive_sum = positive_flow.rolling(period).sum()
    negative_sum = negative_flow.rolling(period).sum()

    money_ratio = positive_sum / negative_sum.replace(0, 0.000001)

    mfi = 100 - (100 / (1 + money_ratio))

    return mfi


def analyze_mfi(highs, lows, closes, volumes):

    closes = pd.Series(closes, dtype=float)

    mfi = calculate_mfi(
        highs,
        lows,
        closes,
        volumes
    )

    latest = float(mfi.iloc[-1])
    previous = float(mfi.iloc[-2])

    slope = latest - previous

    overbought = latest >= 80
    oversold = latest <= 20

    bullish = latest > 50
    bearish = latest < 50

    strengthening = slope > 0
    weakening = slope < 0

    bullish_reversal = (
        previous < 20 and
        latest > 20
    )

    bearish_reversal = (
        previous > 80 and
        latest < 80
    )

    last_price = closes.iloc[-1]
    prev_price = closes.iloc[-6]

    divergence = "None"

    if (
        last_price < prev_price
        and
        latest > float(mfi.iloc[-6])
    ):
        divergence = "Bullish"

    elif (
        last_price > prev_price
        and
        latest < float(mfi.iloc[-6])
    ):
        divergence = "Bearish"

    if latest >= 80:
        zone = "Extreme Buy"

    elif latest >= 65:
        zone = "Strong Buy"

    elif latest >= 50:
        zone = "Bullish"

    elif latest >= 35:
        zone = "Bearish"

    elif latest >= 20:
        zone = "Strong Sell"

    else:
        zone = "Extreme Sell"

    ai_score = 50

    if bullish:
        ai_score += 10

    else:
        ai_score -= 10

    if strengthening:
        ai_score += 10

    else:
        ai_score -= 10

    if bullish_reversal:
        ai_score += 15

    if bearish_reversal:
        ai_score -= 15

    if divergence == "Bullish":
        ai_score += 10

    elif divergence == "Bearish":
        ai_score -= 10

    ai_score = max(0, min(100, ai_score))

    return {

        "mfi": round(latest, 2),

        "mfi_slope": round(slope, 2),

        "bullish": bullish,

        "bearish": bearish,

        "strengthening": strengthening,

        "weakening": weakening,

        "overbought": overbought,

        "oversold": oversold,

        "bullish_reversal": bullish_reversal,

        "bearish_reversal": bearish_reversal,

        "divergence": divergence,

        "zone": zone,

        "ai_score": ai_score,

    }