import numpy as np
import pandas as pd

RSI_PERIOD = 14
EMA_PERIOD = 14


# ==========================================================
# CALCULATE RSI
# ==========================================================


def calculate_rsi(
    closes,
    period=RSI_PERIOD,
):

    closes = pd.Series(closes, dtype="float64")

    delta = closes.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False,
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False,
    ).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    ema = rsi.ewm(
        span=EMA_PERIOD,
        adjust=False,
    ).mean()

    return {
        "rsi": rsi,
        "ema": ema,
    }


# ==========================================================
# RSI SLOPE
# ==========================================================


def rsi_slope(rsi):

    return round(
        float(rsi.iloc[-1] - rsi.iloc[-5]),
        2,
    )


# ==========================================================
# RSI MOMENTUM
# ==========================================================


def rsi_momentum(rsi):

    value = rsi.iloc[-1]

    if value >= 60:
        return "BULLISH"

    if value <= 40:
        return "BEARISH"

    return "NEUTRAL"


# ==========================================================
# RSI TREND
# ==========================================================


def rsi_trend(
    rsi,
    ema,
):

    if rsi.iloc[-1] > ema.iloc[-1]:
        return "UP"

    if rsi.iloc[-1] < ema.iloc[-1]:
        return "DOWN"

    return "SIDEWAYS"


# ==========================================================
# OVERBOUGHT / OVERSOLD
# ==========================================================


def overbought(rsi):

    return rsi.iloc[-1] >= 70


def oversold(rsi):

    return rsi.iloc[-1] <= 30


# ==========================================================
# BULL / BEAR RANGE
# ==========================================================


def bull_bear_range(rsi):

    value = rsi.iloc[-1]

    if value >= 60:
        return "BULL_RANGE"

    if value <= 40:
        return "BEAR_RANGE"

    return "NEUTRAL_RANGE"


# ==========================================================
# FAILURE SWING
# ==========================================================


def failure_swing(rsi):

    values = rsi.tail(5).tolist()

    bullish = values[0] < 30 and values[-1] > values[-2]

    bearish = values[0] > 70 and values[-1] < values[-2]

    return {
        "bullish": bullish,
        "bearish": bearish,
    }


# ==========================================================
# RSI EXPANSION
# ==========================================================


def rsi_expansion(rsi):

    current = rsi.iloc[-1]

    previous = rsi.iloc[-5]

    return abs(current - previous) > 8


# ==========================================================
# RSI COMPRESSION
# ==========================================================


def rsi_compression(rsi):

    current = rsi.iloc[-1]

    previous = rsi.iloc[-5]

    return abs(current - previous) < 3


# ==========================================================
# BULLISH DIVERGENCE
# ==========================================================


def bullish_divergence(
    closes,
    rsi,
):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    return closes.iloc[-1] < closes.iloc[-6] and rsi.iloc[-1] > rsi.iloc[-6]


# ==========================================================
# BEARISH DIVERGENCE
# ==========================================================


def bearish_divergence(
    closes,
    rsi,
):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    return closes.iloc[-1] > closes.iloc[-6] and rsi.iloc[-1] < rsi.iloc[-6]


# ==========================================================
# HIDDEN BULLISH DIVERGENCE
# ==========================================================


def hidden_bullish_divergence(
    closes,
    rsi,
):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    return closes.iloc[-1] > closes.iloc[-6] and rsi.iloc[-1] < rsi.iloc[-6]


# ==========================================================
# HIDDEN BEARISH DIVERGENCE
# ==========================================================


def hidden_bearish_divergence(
    closes,
    rsi,
):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    return closes.iloc[-1] < closes.iloc[-6] and rsi.iloc[-1] > rsi.iloc[-6]


# ==========================================================
# CONTINUATION PROBABILITY
# ==========================================================


def continuation_probability(
    trend,
    expansion,
):

    probability = 50

    if trend == "UP":
        probability += 20

    elif trend == "DOWN":
        probability -= 20

    if expansion:
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
    trend,
    continuation,
    bull_div,
    bear_div,
    hidden_bull,
    hidden_bear,
    overbought_state,
    oversold_state,
):

    score = 50

    if trend == "UP":
        score += 15

    elif trend == "DOWN":
        score -= 15

    score += (continuation - 50) * 0.20

    if bull_div:
        score += 10

    if bear_div:
        score -= 10

    if hidden_bull:
        score += 8

    if hidden_bear:
        score -= 8

    if oversold_state:
        score += 5

    if overbought_state:
        score -= 5

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


def analyze_rsi(closes):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 100:
        raise ValueError("At least 100 candles are required.")

    data = calculate_rsi(closes)

    rsi = data["rsi"]
    ema = data["ema"]

    latest_rsi = float(rsi.iloc[-1])
    latest_ema = float(ema.iloc[-1])

    slope = rsi_slope(rsi)

    momentum = rsi_momentum(rsi)

    trend = rsi_trend(
        rsi,
        ema,
    )

    overbought_state = overbought(rsi)

    oversold_state = oversold(rsi)

    market_range = bull_bear_range(rsi)

    swing = failure_swing(rsi)

    expansion = rsi_expansion(rsi)

    compression = rsi_compression(rsi)

    bull_div = bullish_divergence(
        closes,
        rsi,
    )

    bear_div = bearish_divergence(
        closes,
        rsi,
    )

    hidden_bull = hidden_bullish_divergence(
        closes,
        rsi,
    )

    hidden_bear = hidden_bearish_divergence(
        closes,
        rsi,
    )

    continuation = continuation_probability(
        trend,
        expansion,
    )

    score = ai_score(
        trend,
        continuation,
        bull_div,
        bear_div,
        hidden_bull,
        hidden_bear,
        overbought_state,
        oversold_state,
    )

    return {
        "rsi": round(latest_rsi, 2),
        "rsi_ema": round(latest_ema, 2),
        "rsi_slope": slope,
        "momentum": momentum,
        "trend": trend,
        "range": market_range,
        "overbought": overbought_state,
        "oversold": oversold_state,
        "bullish_failure_swing": swing["bullish"],
        "bearish_failure_swing": swing["bearish"],
        "expansion": expansion,
        "compression": compression,
        "bullish_divergence": bull_div,
        "bearish_divergence": bear_div,
        "hidden_bullish_divergence": hidden_bull,
        "hidden_bearish_divergence": hidden_bear,
        "continuation_probability": continuation,
        "ai_score": score,
    }
