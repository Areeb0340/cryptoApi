import numpy as np
import pandas as pd

EMA_PERIOD = 20


# ==========================================================
# CALCULATE OBV
# ==========================================================


def calculate_obv(closes, volumes):

    closes = pd.Series(closes, dtype="float64")
    volumes = pd.Series(volumes, dtype="float64")

    obv = [0.0]

    for i in range(1, len(closes)):

        if closes.iloc[i] > closes.iloc[i - 1]:
            obv.append(obv[-1] + volumes.iloc[i])

        elif closes.iloc[i] < closes.iloc[i - 1]:
            obv.append(obv[-1] - volumes.iloc[i])

        else:
            obv.append(obv[-1])

    obv = pd.Series(obv)

    ema = obv.ewm(
        span=EMA_PERIOD,
        adjust=False,
    ).mean()

    return {
        "obv": obv,
        "ema": ema,
    }


# ==========================================================
# OBV SLOPE
# ==========================================================


def obv_slope(obv):

    return round(
        float(obv.iloc[-1] - obv.iloc[-5]),
        2,
    )


# ==========================================================
# OBV MOMENTUM
# ==========================================================


def obv_momentum(obv):

    if obv.iloc[-1] > obv.iloc[-5]:
        return "BULLISH"

    if obv.iloc[-1] < obv.iloc[-5]:
        return "BEARISH"

    return "NEUTRAL"


# ==========================================================
# VOLUME PRESSURE
# ==========================================================


def volume_pressure(
    obv,
    ema,
):

    if obv.iloc[-1] > ema.iloc[-1]:
        return "BUY"

    if obv.iloc[-1] < ema.iloc[-1]:
        return "SELL"

    return "NEUTRAL"


# ==========================================================
# ACCUMULATION
# ==========================================================


def accumulation(
    obv,
    ema,
):

    return obv.iloc[-1] > ema.iloc[-1] and obv.iloc[-5] > ema.iloc[-5]


# ==========================================================
# DISTRIBUTION
# ==========================================================


def distribution(
    obv,
    ema,
):

    return obv.iloc[-1] < ema.iloc[-1] and obv.iloc[-5] < ema.iloc[-5]


# ==========================================================
# BREAKOUT CONFIRMATION
# ==========================================================


def breakout_confirmation(
    closes,
    obv,
):

    closes = pd.Series(closes)

    price_up = closes.iloc[-1] > closes.iloc[-6]

    obv_up = obv.iloc[-1] > obv.iloc[-6]

    return price_up and obv_up


# ==========================================================
# BREAKDOWN CONFIRMATION
# ==========================================================


def breakdown_confirmation(
    closes,
    obv,
):

    closes = pd.Series(closes)

    price_down = closes.iloc[-1] < closes.iloc[-6]

    obv_down = obv.iloc[-1] < obv.iloc[-6]

    return price_down and obv_down


# ==========================================================
# BULLISH DIVERGENCE
# ==========================================================


def bullish_divergence(
    closes,
    obv,
):

    closes = pd.Series(closes)

    return closes.iloc[-1] < closes.iloc[-6] and obv.iloc[-1] > obv.iloc[-6]


# ==========================================================
# BEARISH DIVERGENCE
# ==========================================================


def bearish_divergence(
    closes,
    obv,
):

    closes = pd.Series(closes)

    return closes.iloc[-1] > closes.iloc[-6] and obv.iloc[-1] < obv.iloc[-6]


# ==========================================================
# HIDDEN BULLISH DIVERGENCE
# ==========================================================


def hidden_bullish_divergence(
    closes,
    obv,
):

    closes = pd.Series(closes)

    return closes.iloc[-1] > closes.iloc[-6] and obv.iloc[-1] < obv.iloc[-6]


# ==========================================================
# HIDDEN BEARISH DIVERGENCE
# ==========================================================


def hidden_bearish_divergence(
    closes,
    obv,
):

    closes = pd.Series(closes)

    return closes.iloc[-1] < closes.iloc[-6] and obv.iloc[-1] > obv.iloc[-6]


# ==========================================================
# TREND STRENGTH
# ==========================================================


def trend_strength(
    accumulation_state,
    distribution_state,
    pressure,
):

    score = 50

    if accumulation_state:
        score += 20

    if distribution_state:
        score -= 20

    if pressure == "BUY":
        score += 10

    elif pressure == "SELL":
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
    trend,
    breakout,
):

    probability = trend

    if breakout:
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
):

    score = trend

    score += (continuation - 50) * 0.20

    if bull_div:
        score += 10

    if bear_div:
        score -= 10

    if hidden_bull:
        score += 8

    if hidden_bear:
        score -= 8

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


def analyze_obv(closes, volumes):

    closes = pd.Series(closes, dtype="float64")
    volumes = pd.Series(volumes, dtype="float64")

    if len(closes) < 100:
        raise ValueError("At least 100 candles are required.")

    data = calculate_obv(
        closes,
        volumes,
    )

    obv = data["obv"]
    ema = data["ema"]

    latest_obv = float(obv.iloc[-1])
    latest_ema = float(ema.iloc[-1])

    slope = obv_slope(obv)

    momentum = obv_momentum(obv)

    pressure = volume_pressure(
        obv,
        ema,
    )

    accumulation_state = accumulation(
        obv,
        ema,
    )

    distribution_state = distribution(
        obv,
        ema,
    )

    breakout = breakout_confirmation(
        closes,
        obv,
    )

    breakdown = breakdown_confirmation(
        closes,
        obv,
    )

    bull_div = bullish_divergence(
        closes,
        obv,
    )

    bear_div = bearish_divergence(
        closes,
        obv,
    )

    hidden_bull = hidden_bullish_divergence(
        closes,
        obv,
    )

    hidden_bear = hidden_bearish_divergence(
        closes,
        obv,
    )

    trend = trend_strength(
        accumulation_state,
        distribution_state,
        pressure,
    )

    continuation = continuation_probability(
        trend,
        breakout,
    )

    score = ai_score(
        trend,
        continuation,
        bull_div,
        bear_div,
        hidden_bull,
        hidden_bear,
    )

    return {
        "obv": round(latest_obv, 2),
        "obv_ema": round(latest_ema, 2),
        "obv_slope": slope,
        "momentum": momentum,
        "volume_pressure": pressure,
        "institutional_accumulation": accumulation_state,
        "institutional_distribution": distribution_state,
        "breakout_confirmation": breakout,
        "breakdown_confirmation": breakdown,
        "bullish_divergence": bull_div,
        "bearish_divergence": bear_div,
        "hidden_bullish_divergence": hidden_bull,
        "hidden_bearish_divergence": hidden_bear,
        "trend_strength": trend,
        "continuation_probability": continuation,
        "ai_score": score,
    }
