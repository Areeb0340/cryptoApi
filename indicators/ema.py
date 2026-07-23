import numpy as np
import pandas as pd

EMA_PERIODS = [20, 50, 100, 200]


# ==========================================================
# EMA
# ==========================================================


def calculate_ema(closes, period):

    closes = pd.Series(closes, dtype="float64")

    return closes.ewm(span=period, adjust=False).mean()


# ==========================================================
# EMA Ribbon
# ==========================================================


def ema_ribbon(closes):

    ribbon = {}

    for period in EMA_PERIODS:

        ribbon[f"ema{period}"] = calculate_ema(closes, period)

    return ribbon


# ==========================================================
# Ribbon Alignment
# ==========================================================


def ribbon_alignment(ribbon):

    e20 = ribbon["ema20"].iloc[-1]
    e50 = ribbon["ema50"].iloc[-1]
    e100 = ribbon["ema100"].iloc[-1]
    e200 = ribbon["ema200"].iloc[-1]

    bullish = e20 > e50 > e100 > e200

    bearish = e20 < e50 < e100 < e200

    if bullish:
        trend = "Strong Bullish"

    elif bearish:
        trend = "Strong Bearish"

    else:
        trend = "Sideways"

    return {
        "bullish": bullish,
        "bearish": bearish,
        "trend": trend,
    }


# ==========================================================
# EMA Cross
# ==========================================================


def detect_cross(ribbon):

    ema50 = ribbon["ema50"]
    ema200 = ribbon["ema200"]

    golden = ema50.iloc[-2] <= ema200.iloc[-2] and ema50.iloc[-1] > ema200.iloc[-1]

    death = ema50.iloc[-2] >= ema200.iloc[-2] and ema50.iloc[-1] < ema200.iloc[-1]

    return {
        "golden_cross": golden,
        "death_cross": death,
    }


# ==========================================================
# EMA Slopes
# ==========================================================


def ema_slopes(ribbon):

    result = {}

    for period in EMA_PERIODS:

        ema = ribbon[f"ema{period}"]

        result[f"ema{period}_slope"] = ema.iloc[-1] - ema.iloc[-5]

    return result


# ==========================================================
# Price Position
# ==========================================================


def price_position(price, ribbon):

    return {
        "above20": price > ribbon["ema20"].iloc[-1],
        "above50": price > ribbon["ema50"].iloc[-1],
        "above100": price > ribbon["ema100"].iloc[-1],
        "above200": price > ribbon["ema200"].iloc[-1],
    }


# ==========================================================
# EMA Distance
# ==========================================================


def ema_distance(price, ribbon):

    result = {}

    for period in EMA_PERIODS:

        ema = ribbon[f"ema{period}"].iloc[-1]

        distance = ((price - ema) / ema) * 100

        result[f"distance_{period}"] = round(distance, 2)

    return result


# ==========================================================
# EMA Ribbon Width
# ==========================================================


def ribbon_width(ribbon):

    ema20 = ribbon["ema20"].iloc[-1]
    ema200 = ribbon["ema200"].iloc[-1]

    width = abs(ema20 - ema200)

    percentage = (width / ema200) * 100

    return round(percentage, 2)


# ==========================================================
# Ribbon Compression
# ==========================================================


def ribbon_compression(ribbon):

    width = ribbon_width(ribbon)

    return width < 0.80


# ==========================================================
# Ribbon Expansion
# ==========================================================


def ribbon_expansion(ribbon):

    width = ribbon_width(ribbon)

    return width > 2.50


# ==========================================================
# EMA Separation Strength
# ==========================================================


def separation_strength(ribbon):

    ema20 = ribbon["ema20"].iloc[-1]
    ema50 = ribbon["ema50"].iloc[-1]
    ema100 = ribbon["ema100"].iloc[-1]
    ema200 = ribbon["ema200"].iloc[-1]

    s1 = abs(ema20 - ema50)
    s2 = abs(ema50 - ema100)
    s3 = abs(ema100 - ema200)

    return round(s1 + s2 + s3, 4)


# ==========================================================
# EMA Momentum
# ==========================================================


def momentum_score(slopes):

    score = 50

    for value in slopes.values():

        if value > 0:
            score += 5

        elif value < 0:
            score -= 5

    score = max(0, min(score, 100))

    return score


# ==========================================================
# Trend Strength
# ==========================================================


def trend_strength(
    alignment,
    compression,
    expansion,
    momentum,
):

    score = momentum

    if alignment["bullish"]:
        score += 15

    if alignment["bearish"]:
        score -= 15

    if expansion:
        score += 10

    if compression:
        score -= 10

    score = max(0, min(score, 100))

    return score


# ==========================================================
# Dynamic Support / Resistance
# ==========================================================


def dynamic_levels(price, ribbon):

    ema20 = ribbon["ema20"].iloc[-1]
    ema50 = ribbon["ema50"].iloc[-1]
    ema100 = ribbon["ema100"].iloc[-1]
    ema200 = ribbon["ema200"].iloc[-1]

    support = None
    resistance = None

    if price > ema20:
        support = ema20
    elif price > ema50:
        support = ema50
    elif price > ema100:
        support = ema100
    else:
        support = ema200

    if price < ema20:
        resistance = ema20
    elif price < ema50:
        resistance = ema50
    elif price < ema100:
        resistance = ema100
    else:
        resistance = ema200

    return {
        "support": round(float(support), 4),
        "resistance": round(float(resistance), 4),
    }


# ==========================================================
# Pullback Detection
# ==========================================================


def pullback(price, ribbon, alignment):

    ema20 = ribbon["ema20"].iloc[-1]
    ema50 = ribbon["ema50"].iloc[-1]

    bullish_pullback = alignment["bullish"] and price <= ema20 and price >= ema50

    bearish_pullback = alignment["bearish"] and price >= ema20 and price <= ema50

    return {
        "bullish_pullback": bullish_pullback,
        "bearish_pullback": bearish_pullback,
    }


# ==========================================================
# Fake Breakout
# ==========================================================


def fake_breakout(price, ribbon):

    ema20 = ribbon["ema20"].iloc[-1]

    distance = abs((price - ema20) / ema20) * 100

    return distance < 0.15


# ==========================================================
# Mean Reversion
# ==========================================================


def mean_reversion(price, ribbon):

    ema200 = ribbon["ema200"].iloc[-1]

    distance = ((price - ema200) / ema200) * 100

    if distance > 8:
        return "OVERBOUGHT"

    if distance < -8:
        return "OVERSOLD"

    return "NORMAL"


# ==========================================================
# Trend Continuation Probability
# ==========================================================


def continuation_probability(
    trend_strength,
    momentum,
    expansion,
    compression,
):

    probability = trend_strength

    probability += (momentum - 50) * 0.30

    if expansion:
        probability += 10

    if compression:
        probability -= 15

    probability = max(0, min(100, probability))

    return round(probability, 2)


# ==========================================================
# MAIN ANALYZER
# ==========================================================


def analyze_ema(closes):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 250:
        raise ValueError("At least 250 candles are required.")

    price = closes.iloc[-1]

    ribbon = ema_ribbon(closes)

    alignment = ribbon_alignment(ribbon)

    cross = detect_cross(ribbon)

    slopes = ema_slopes(ribbon)

    position = price_position(price, ribbon)

    distance = ema_distance(price, ribbon)

    compression = ribbon_compression(ribbon)

    expansion = ribbon_expansion(ribbon)

    separation = separation_strength(ribbon)

    momentum = momentum_score(slopes)

    strength = trend_strength(
        alignment,
        compression,
        expansion,
        momentum,
    )

    levels = dynamic_levels(price, ribbon)

    pb = pullback(
        price,
        ribbon,
        alignment,
    )

    fake = fake_breakout(
        price,
        ribbon,
    )

    mean = mean_reversion(
        price,
        ribbon,
    )

    continuation = continuation_probability(
        strength,
        momentum,
        expansion,
        compression,
    )

    # ======================================================
    # AI SCORE
    # ======================================================

    ai_score = 50

    if alignment["bullish"]:
        ai_score += 20

    elif alignment["bearish"]:
        ai_score -= 20

    if cross["golden_cross"]:

        ai_score += 15

    elif cross["death_cross"]:
        ai_score -= 15

    if expansion:
        ai_score += 10

    elif compression:
        ai_score -= 10

    if continuation > 70:
        ai_score += 10

    elif continuation < 30:
        ai_score -= 10

    if fake:
        ai_score -= 10

        ai_score = max(0, min(100, ai_score))

    # ======================================================
    # OUTPUT
    # ======================================================

    return {
        "price": round(float(price), 4),
        "ema20": round(float(ribbon["ema20"].iloc[-1]), 4),
        "ema50": round(float(ribbon["ema50"].iloc[-1]), 4),
        "ema100": round(float(ribbon["ema100"].iloc[-1]), 4),
        "ema200": round(float(ribbon["ema200"].iloc[-1]), 4),
        "trend": alignment["trend"],
        "bullish_alignment": alignment["bullish"],
        "bearish_alignment": alignment["bearish"],
        "golden_cross": cross["golden_cross"],
        "death_cross": cross["death_cross"],
        "compression": compression,
        "expansion": expansion,
        "separation_strength": separation,
        "momentum_score": momentum,
        "trend_strength": strength,
        "continuation_probability": continuation,
        "support": levels["support"],
        "resistance": levels["resistance"],
        "bullish_pullback": pb["bullish_pullback"],
        "bearish_pullback": pb["bearish_pullback"],
        "fake_breakout": fake,
        "mean_reversion": mean,
        "distances": distance,
        "slopes": slopes,
        "price_position": position,
        "ai_score": ai_score,
        "trend_score": ai_score,
    }
