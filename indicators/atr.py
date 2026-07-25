import numpy as np
import pandas as pd

ATR_PERIOD = 14


# ==========================================================
# ATR
# ==========================================================


def calculate_atr(highs, lows, closes, period=ATR_PERIOD):

    high = pd.Series(highs, dtype="float64")
    low = pd.Series(lows, dtype="float64")
    close = pd.Series(closes, dtype="float64")

    previous_close = close.shift(1)

    tr = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = tr.ewm(
        alpha=1 / period,
        adjust=False,
    ).mean()

    return atr


# ==========================================================
# ATR MOVING AVERAGE
# ==========================================================


def atr_ma(atr):

    return atr.rolling(20).mean()


# ==========================================================
# ATR SLOPE
# ==========================================================


def atr_slope(atr):

    return round(
        float(atr.iloc[-1] - atr.iloc[-5]),
        4,
    )


# ==========================================================
# ATR PERCENT
# ==========================================================


def atr_percent(
    atr_value,
    price,
):

    return round(
        (atr_value / price) * 100,
        2,
    )


# ==========================================================
# VOLATILITY LEVEL
# ==========================================================


def volatility_level(
    atr_value,
    atr_average,
):

    if atr_value > atr_average * 2:
        return "EXTREME"

    if atr_value > atr_average * 1.5:
        return "HIGH"

    if atr_value > atr_average:
        return "MEDIUM"

    if atr_value > atr_average * 0.6:
        return "LOW"

    return "VERY_LOW"


# ==========================================================
# ATR EXPANSION
# ==========================================================


def atr_expansion(atr):

    latest = atr.iloc[-1]
    previous = atr.iloc[-5]

    return latest > previous


# ==========================================================
# ATR COMPRESSION
# ==========================================================


def atr_compression(atr):

    latest = atr.iloc[-1]
    previous = atr.iloc[-5]

    return latest < previous


# ==========================================================
# BREAKOUT READY
# ==========================================================


def breakout_ready(
    atr_value,
    atr_average,
    expansion,
):

    return expansion and atr_value > atr_average


# ==========================================================
# TREND FRIENDLY
# ==========================================================


def trend_friendly(
    atr_value,
    atr_average,
):

    return atr_value > atr_average * 1.20


# ==========================================================
# CHOPPY MARKET
# ==========================================================


def choppy_market(
    atr_value,
    atr_average,
):

    return atr_value < atr_average * 0.70


# ==========================================================
# VOLATILITY REGIME
# ==========================================================


def volatility_regime(
    atr_value,
    atr_average,
):

    ratio = atr_value / atr_average

    if ratio >= 2:

        return "EXPLOSIVE"

    if ratio >= 1.5:

        return "EXPANDING"

    if ratio >= 1:

        return "NORMAL"

    if ratio >= 0.7:

        return "CONTRACTING"

    return "DEAD"


# ==========================================================
# MOMENTUM SCORE
# ==========================================================


def momentum_score(
    atr_value,
    atr_average,
    expansion,
):

    score = 50

    ratio = atr_value / atr_average

    score += min(ratio * 20, 30)

    if expansion:
        score += 10

    else:
        score -= 10

    score = max(
        0,
        min(
            round(score),
            100,
        ),
    )

    return score


# ==========================================================
# STOP LOSS ENGINE
# ==========================================================


def stop_loss_levels(atr_value):

    return {
        "1x": round(atr_value, 2),
        "1_5x": round(atr_value * 1.5, 2),
        "2x": round(atr_value * 2, 2),
        "3x": round(atr_value * 3, 2),
    }


# ==========================================================
# TAKE PROFIT ENGINE
# ==========================================================


def take_profit_levels(atr_value):

    return {
        "2x": round(atr_value * 2, 2),
        "3x": round(atr_value * 3, 2),
        "4x": round(atr_value * 4, 2),
        "5x": round(atr_value * 5, 2),
    }


# ==========================================================
# CONTINUATION PROBABILITY
# ==========================================================


def continuation_probability(
    atr_value,
    atr_average,
    expansion,
    momentum,
):

    probability = 50

    ratio = atr_value / atr_average

    probability += min(ratio * 20, 25)

    if expansion:
        probability += 10

    probability += (momentum - 50) * 0.30

    probability = max(
        0,
        min(
            round(probability),
            100,
        ),
    )

    return probability


# ==========================================================
# TREND QUALITY
# ==========================================================


def trend_quality(
    atr_value,
    atr_average,
):

    ratio = atr_value / atr_average

    quality = min(
        ratio * 50,
        100,
    )

    return round(quality, 2)


# ==========================================================
# AI SCORE
# ==========================================================


def ai_score(
    breakout,
    trend,
    choppy,
    expansion,
    continuation,
):

    score = 50

    if breakout:
        score += 10

    if trend:
        score += 10

    if expansion:
        score += 10

    if choppy:
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
# MAIN ANALYZER
# ==========================================================


def analyze_atr(highs, lows, closes):

    if len(closes) < 100:
        raise ValueError("At least 100 candles are required.")

    atr = calculate_atr(
        highs,
        lows,
        closes,
    )

    latest_atr = float(atr.iloc[-1])

    average = float(atr_ma(atr).iloc[-1])

    slope = atr_slope(atr)

    expansion = atr_expansion(atr)

    compression = atr_compression(atr)

    price = float(closes[-1])

    percent = atr_percent(
        latest_atr,
        price,
    )

    volatility = volatility_level(
        latest_atr,
        average,
    )

    breakout = breakout_ready(
        latest_atr,
        average,
        expansion,
    )

    trend = trend_friendly(
        latest_atr,
        average,
    )

    choppy = choppy_market(
        latest_atr,
        average,
    )

    regime = volatility_regime(
        latest_atr,
        average,
    )

    momentum = momentum_score(
        latest_atr,
        average,
        expansion,
    )

    continuation = continuation_probability(
        latest_atr,
        average,
        expansion,
        momentum,
    )

    quality = trend_quality(
        latest_atr,
        average,
    )

    sl = stop_loss_levels(
        latest_atr,
    )

    tp = take_profit_levels(
        latest_atr,
    )

    score = ai_score(
        breakout,
        trend,
        choppy,
        expansion,
        continuation,
    )

    return {
        "atr": round(latest_atr, 4),
        "atr_ma": round(average, 4),
        "atr_percent": percent,
        "atr_slope": slope,
        "volatility": volatility,
        "volatility_regime": regime,
        "expansion": expansion,
        "compression": compression,
        "breakout_ready": breakout,
        "trend_friendly": trend,
        "choppy_market": choppy,
        "momentum_score": momentum,
        "continuation_probability": continuation,
        "trend_quality": quality,
        "stop_loss": sl,
        "take_profit": tp,
        "ai_score": score,
    }
