import numpy as np
import pandas as pd

PERIOD = 20
STD_DEV = 2


# ==========================================================
# CALCULATE BOLLINGER
# ==========================================================


def calculate_bollinger(closes):

    closes = pd.Series(closes, dtype="float64")

    middle = closes.rolling(PERIOD).mean()

    std = closes.rolling(PERIOD).std()

    upper = middle + (STD_DEV * std)

    lower = middle - (STD_DEV * std)

    width = ((upper - lower) / middle) * 100

    return {
        "middle": middle,
        "upper": upper,
        "lower": lower,
        "width": width,
    }


# ==========================================================
# BAND POSITION
# ==========================================================


def band_position(
    price,
    bands,
):

    upper = bands["upper"].iloc[-1]

    middle = bands["middle"].iloc[-1]

    lower = bands["lower"].iloc[-1]

    if price >= upper:
        return "UPPER"

    if price <= lower:
        return "LOWER"

    if price >= middle:
        return "UPPER_HALF"

    return "LOWER_HALF"


# ==========================================================
# BAND WIDTH
# ==========================================================


def band_width(
    bands,
):

    return round(
        float(bands["width"].iloc[-1]),
        2,
    )


# ==========================================================
# BAND SLOPE
# ==========================================================


def band_slope(
    bands,
):

    return round(
        float(bands["width"].iloc[-1] - bands["width"].iloc[-5]),
        4,
    )


# ==========================================================
# BOLLINGER SQUEEZE
# ==========================================================


def squeeze(bands):

    width = bands["width"].iloc[-1]

    return width < 3.0


# ==========================================================
# BAND EXPANSION
# ==========================================================


def expansion(bands):

    current = bands["width"].iloc[-1]

    previous = bands["width"].iloc[-5]

    return current > previous


# ==========================================================
# BAND COMPRESSION
# ==========================================================


def compression(bands):

    current = bands["width"].iloc[-1]

    previous = bands["width"].iloc[-5]

    return current < previous


# ==========================================================
# WALKING THE BAND
# ==========================================================


def walking_band(
    closes,
    bands,
):

    closes = pd.Series(closes)

    upper = bands["upper"]

    lower = bands["lower"]

    bullish = True

    bearish = True

    for i in range(-5, 0):

        if closes.iloc[i] < upper.iloc[i]:
            bullish = False

        if closes.iloc[i] > lower.iloc[i]:
            bearish = False

    return {
        "bullish": bullish,
        "bearish": bearish,
    }


# ==========================================================
# VOLATILITY REGIME
# ==========================================================


def volatility_regime(bands):

    width = bands["width"].iloc[-1]

    if width < 2:
        return "DEAD"

    if width < 4:
        return "LOW"

    if width < 7:
        return "NORMAL"

    if width < 10:
        return "HIGH"

    return "EXTREME"


# ==========================================================
# BREAKOUT READY
# ==========================================================


def breakout_ready(
    bands,
):

    return squeeze(bands) and expansion(bands)


# ==========================================================
# MEAN REVERSION
# ==========================================================


def mean_reversion(
    price,
    bands,
):

    upper = bands["upper"].iloc[-1]

    middle = bands["middle"].iloc[-1]

    lower = bands["lower"].iloc[-1]

    if price > upper:
        return "OVERBOUGHT"

    if price < lower:
        return "OVERSOLD"

    if price > middle:
        return "BULLISH"

    return "BEARISH"


# ==========================================================
# FAKE BREAKOUT
# ==========================================================


def fake_breakout(
    closes,
    bands,
):

    closes = pd.Series(closes)

    upper = bands["upper"]

    lower = bands["lower"]

    if closes.iloc[-2] > upper.iloc[-2] and closes.iloc[-1] < upper.iloc[-1]:

        return "FAKE_BULL_BREAKOUT"

    if closes.iloc[-2] < lower.iloc[-2] and closes.iloc[-1] > lower.iloc[-1]:

        return "FAKE_BEAR_BREAKOUT"

    return None


# ==========================================================
# TREND STRENGTH
# ==========================================================


def trend_strength(
    walk,
    expansion_state,
    squeeze_state,
):

    score = 50

    if walk["bullish"]:
        score += 20

    if walk["bearish"]:
        score += 20

    if expansion_state:
        score += 15

    if squeeze_state:
        score -= 10

    return max(
        0,
        min(
            score,
            100,
        ),
    )


# ==========================================================
# CONTINUATION PROBABILITY
# ==========================================================


def continuation_probability(
    trend_score,
    expansion_state,
):

    probability = trend_score

    if expansion_state:
        probability += 10

    probability = max(
        0,
        min(
            probability,
            100,
        ),
    )

    return round(probability, 2)


# ==========================================================
# AI SCORE
# ==========================================================


def ai_score(
    trend_score,
    continuation,
    fake,
):

    score = trend_score

    score += (continuation - 50) * 0.20

    if fake:

        score -= 20

    return max(
        0,
        min(
            round(score),
            100,
        ),
    )


# ==========================================================
# MAIN ANALYZER
# ==========================================================


def analyze_bollinger(closes):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 100:
        raise ValueError("At least 100 candles are required.")

    price = float(closes.iloc[-1])

    bands = calculate_bollinger(closes)

    position = band_position(
        price,
        bands,
    )

    width = band_width(
        bands,
    )

    slope = band_slope(
        bands,
    )

    squeeze_state = squeeze(
        bands,
    )

    expansion_state = expansion(
        bands,
    )

    compression_state = compression(
        bands,
    )

    walk = walking_band(
        closes,
        bands,
    )

    regime = volatility_regime(
        bands,
    )

    breakout = breakout_ready(
        bands,
    )

    reversion = mean_reversion(
        price,
        bands,
    )

    fake = fake_breakout(
        closes,
        bands,
    )

    trend = trend_strength(
        walk,
        expansion_state,
        squeeze_state,
    )

    continuation = continuation_probability(
        trend,
        expansion_state,
    )

    score = ai_score(
        trend,
        continuation,
        fake,
    )

    return {
        "price": round(price, 4),
        "upper_band": round(
            float(bands["upper"].iloc[-1]),
            4,
        ),
        "middle_band": round(
            float(bands["middle"].iloc[-1]),
            4,
        ),
        "lower_band": round(
            float(bands["lower"].iloc[-1]),
            4,
        ),
        "band_position": position,
        "band_width": width,
        "band_slope": slope,
        "squeeze": squeeze_state,
        "expansion": expansion_state,
        "compression": compression_state,
        "walking_upper_band": walk["bullish"],
        "walking_lower_band": walk["bearish"],
        "volatility_regime": regime,
        "breakout_ready": breakout,
        "mean_reversion": reversion,
        "fake_breakout": fake,
        "trend_strength": trend,
        "continuation_probability": continuation,
        "ai_score": score,
    }
