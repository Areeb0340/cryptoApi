import numpy as np
import pandas as pd

ADX_PERIOD = 14


# ==========================================================
# CALCULATE ADX
# ==========================================================


def calculate_adx(highs, lows, closes, period=ADX_PERIOD):

    high = pd.Series(highs, dtype="float64")
    low = pd.Series(lows, dtype="float64")
    close = pd.Series(closes, dtype="float64")

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)

    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = tr.ewm(
        alpha=1 / period,
        adjust=False,
    ).mean()

    plus_di = (
        plus_dm.ewm(
            alpha=1 / period,
            adjust=False,
        ).mean()
        / atr
    ) * 100

    minus_di = (
        minus_dm.ewm(
            alpha=1 / period,
            adjust=False,
        ).mean()
        / atr
    ) * 100

    dx = ((plus_di - minus_di).abs() / (plus_di + minus_di)) * 100

    adx = dx.ewm(
        alpha=1 / period,
        adjust=False,
    ).mean()

    return adx, plus_di, minus_di


# ==========================================================
# DI CROSS
# ==========================================================


def detect_di_cross(
    plus_di,
    minus_di,
):

    bullish = (
        plus_di.iloc[-2] <= minus_di.iloc[-2] and plus_di.iloc[-1] > minus_di.iloc[-1]
    )

    bearish = (
        plus_di.iloc[-2] >= minus_di.iloc[-2] and plus_di.iloc[-1] < minus_di.iloc[-1]
    )

    return {
        "bullish_cross": bullish,
        "bearish_cross": bearish,
    }


# ==========================================================
# DI SEPARATION
# ==========================================================


def di_separation(
    plus_di,
    minus_di,
):

    return abs(plus_di.iloc[-1] - minus_di.iloc[-1])


# ==========================================================
# ADX SLOPE
# ==========================================================


def adx_slope(adx):

    return round(
        float(adx.iloc[-1] - adx.iloc[-5]),
        4,
    )


# ==========================================================
# ADX EXPANSION
# ==========================================================


def adx_expansion(adx):

    latest = adx.iloc[-1]

    previous = adx.iloc[-5]

    return latest > previous


# ==========================================================
# ADX COMPRESSION
# ==========================================================


def adx_compression(adx):

    latest = adx.iloc[-1]

    previous = adx.iloc[-5]

    return latest < previous


# ==========================================================
# TREND STRENGTH
# ==========================================================


def trend_strength(adx_value):

    if adx_value >= 50:
        return "EXTREME"

    if adx_value >= 40:
        return "VERY_STRONG"

    if adx_value >= 25:
        return "STRONG"

    if adx_value >= 20:
        return "MODERATE"

    return "WEAK"


# ==========================================================
# TREND EXHAUSTION
# ==========================================================


def trend_exhaustion(
    adx_value,
    slope,
):

    if adx_value > 50 and slope < 0:
        return True

    return False


# ==========================================================
# DIRECTION
# ==========================================================


def direction(
    plus_di,
    minus_di,
):

    latest_plus = plus_di.iloc[-1]

    latest_minus = minus_di.iloc[-1]

    if latest_plus > latest_minus:
        return "BULLISH"

    if latest_minus > latest_plus:
        return "BEARISH"

    return "SIDEWAYS"


# ==========================================================
# MOMENTUM SCORE
# ==========================================================


def momentum_score(
    adx_value,
    slope,
):

    score = 50

    score += min(adx_value, 50) * 0.60

    if slope > 0:
        score += 15

    else:
        score -= 15

    return max(
        0,
        min(
            round(score),
            100,
        ),
    )


# ==========================================================
# DIRECTION CONFIDENCE
# ==========================================================


def direction_confidence(
    plus_di,
    minus_di,
):

    separation = abs(plus_di.iloc[-1] - minus_di.iloc[-1])

    confidence = min(
        100,
        separation * 2,
    )

    return round(confidence, 2)


# ==========================================================
# TREND CONTINUATION
# ==========================================================


def continuation_probability(
    adx_value,
    expansion,
    compression,
    confidence,
):

    probability = adx_value

    probability += confidence * 0.30

    if expansion:
        probability += 10

    if compression:
        probability -= 10

    probability = max(
        0,
        min(
            probability,
            100,
        ),
    )

    return round(probability, 2)


# ==========================================================
# TREND QUALITY
# ==========================================================


def trend_quality(
    adx_value,
    separation,
):

    score = 0

    score += min(adx_value, 50)

    score += min(separation, 50)

    return round(
        score,
        2,
    )


# ==========================================================
# AI SCORE
# ==========================================================


def ai_score(
    direction,
    strength,
    expansion,
    exhaustion,
    continuation,
):

    score = 50

    if direction == "BULLISH":
        score += 10

    elif direction == "BEARISH":
        score += 10

    if strength in [
        "STRONG",
        "VERY_STRONG",
        "EXTREME",
    ]:

        score += 15

    if expansion:
        score += 10

    if exhaustion:
        score -= 20

    score += (continuation - 50) * 0.20

    score = max(
        0,
        min(
            round(score),
            100,
        ),
    )

    return score


# ==========================================================
# TREND STATE
# ==========================================================


def trend_state(
    direction,
    strength,
):

    return f"{direction}_{strength}"


# ==========================================================
# MAIN ANALYZER
# ==========================================================


def analyze_adx(highs, lows, closes):

    if len(closes) < 100:
        raise ValueError("At least 100 candles are required.")

    adx, plus_di, minus_di = calculate_adx(
        highs,
        lows,
        closes,
    )

    latest_adx = float(adx.iloc[-1])

    latest_plus = float(plus_di.iloc[-1])

    latest_minus = float(minus_di.iloc[-1])

    slope = adx_slope(adx)

    expansion = adx_expansion(adx)

    compression = adx_compression(adx)

    strength = trend_strength(latest_adx)

    exhaustion = trend_exhaustion(
        latest_adx,
        slope,
    )

    trend_direction = direction(
        plus_di,
        minus_di,
    )

    separation = di_separation(
        plus_di,
        minus_di,
    )

    cross = detect_di_cross(
        plus_di,
        minus_di,
    )

    momentum = momentum_score(
        latest_adx,
        slope,
    )

    confidence = direction_confidence(
        plus_di,
        minus_di,
    )

    continuation = continuation_probability(
        latest_adx,
        expansion,
        compression,
        confidence,
    )

    quality = trend_quality(
        latest_adx,
        separation,
    )

    score = ai_score(
        trend_direction,
        strength,
        expansion,
        exhaustion,
        continuation,
    )

    state = trend_state(
        trend_direction,
        strength,
    )

    return {
        "adx": round(latest_adx, 2),
        "plus_di": round(latest_plus, 2),
        "minus_di": round(latest_minus, 2),
        "adx_slope": slope,
        "direction": trend_direction,
        "trend_strength": strength,
        "trend_state": state,
        "expansion": expansion,
        "compression": compression,
        "trend_exhaustion": exhaustion,
        "momentum_score": momentum,
        "direction_confidence": confidence,
        "continuation_probability": continuation,
        "trend_quality": quality,
        "di_separation": round(separation, 2),
        "bullish_cross": cross["bullish_cross"],
        "bearish_cross": cross["bearish_cross"],
        "ai_score": score,
    }
