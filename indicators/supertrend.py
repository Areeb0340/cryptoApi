import pandas as pd
import numpy as np

ATR_PERIOD = 10
MULTIPLIER = 3.0


def calculate_atr(highs, lows, closes, period=ATR_PERIOD):

    high = pd.Series(highs, dtype=float)
    low = pd.Series(lows, dtype=float)
    close = pd.Series(closes, dtype=float)

    previous_close = close.shift(1)

    tr = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = tr.ewm(alpha=1 / period, adjust=False).mean()

    return atr


def calculate_supertrend(
    highs,
    lows,
    closes,
    period=ATR_PERIOD,
    multiplier=MULTIPLIER,
):

    high = pd.Series(highs, dtype=float)
    low = pd.Series(lows, dtype=float)
    close = pd.Series(closes, dtype=float)

    atr = calculate_atr(
        highs,
        lows,
        closes,
        period,
    )

    hl2 = (high + low) / 2

    upperband = hl2 + multiplier * atr
    lowerband = hl2 - multiplier * atr

    final_upper = upperband.copy()
    final_lower = lowerband.copy()

    trend = pd.Series(index=close.index, dtype=bool)
    supertrend = pd.Series(index=close.index, dtype=float)

    trend.iloc[0] = True

    for i in range(1, len(close)):

        if (
            upperband.iloc[i] < final_upper.iloc[i - 1]
            or close.iloc[i - 1] > final_upper.iloc[i - 1]
        ):
            final_upper.iloc[i] = upperband.iloc[i]
        else:
            final_upper.iloc[i] = final_upper.iloc[i - 1]

        if (
            lowerband.iloc[i] > final_lower.iloc[i - 1]
            or close.iloc[i - 1] < final_lower.iloc[i - 1]
        ):
            final_lower.iloc[i] = lowerband.iloc[i]
        else:
            final_lower.iloc[i] = final_lower.iloc[i - 1]

        if trend.iloc[i - 1]:

            if close.iloc[i] < final_lower.iloc[i]:
                trend.iloc[i] = False
            else:
                trend.iloc[i] = True

        else:

            if close.iloc[i] > final_upper.iloc[i]:
                trend.iloc[i] = True
            else:
                trend.iloc[i] = False

        if trend.iloc[i]:
            supertrend.iloc[i] = final_lower.iloc[i]
        else:
            supertrend.iloc[i] = final_upper.iloc[i]

    return supertrend, trend


def analyze_supertrend(highs, lows, closes):

    st, trend = calculate_supertrend(
        highs,
        lows,
        closes,
    )

    price = float(closes[-1])

    latest_st = float(st.iloc[-1])

    bullish = bool(trend.iloc[-1])
    bearish = not bullish

    buy_signal = (
        trend.iloc[-2] == False
        and trend.iloc[-1] == True
    )

    sell_signal = (
        trend.iloc[-2] == True
        and trend.iloc[-1] == False
    )

    trend_count = 1

    for i in range(len(trend) - 2, -1, -1):

        if trend.iloc[i] == trend.iloc[-1]:
            trend_count += 1
        else:
            break

    distance = abs(
        (price - latest_st)
        / latest_st
        * 100
    )

    if trend_count >= 30:
        strength = "Extreme"

    elif trend_count >= 20:
        strength = "Very Strong"

    elif trend_count >= 10:
        strength = "Strong"

    elif trend_count >= 5:
        strength = "Moderate"

    else:
        strength = "Weak"

    trailing_stop = round(latest_st, 2)

    ai_score = 50

    if bullish:
        ai_score += 20
    else:
        ai_score -= 20

    if buy_signal:
        ai_score += 20

    if sell_signal:
        ai_score -= 20

    if trend_count >= 10:
        ai_score += 10

    if distance > 3:
        ai_score -= 10

    ai_score = max(0, min(100, ai_score))

    return {

        "supertrend": round(latest_st, 2),

        "price": round(price, 2),

        "bullish": bullish,

        "bearish": bearish,

        "buy_signal": buy_signal,

        "sell_signal": sell_signal,

        "trend_count": trend_count,

        "trend_strength": strength,

        "distance_percent": round(distance, 2),

        "trailing_stop": trailing_stop,

        "trend": "Bullish" if bullish else "Bearish",

        "ai_score": ai_score,

    }