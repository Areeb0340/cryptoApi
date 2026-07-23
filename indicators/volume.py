import numpy as np
import pandas as pd

SMA_PERIOD = 20
EMA_PERIOD = 20


# ==========================================================
# BASIC VOLUME
# ==========================================================


def calculate_volume(volumes):

    volume = pd.Series(volumes, dtype="float64")

    sma = volume.rolling(SMA_PERIOD).mean()

    ema = volume.ewm(
        span=EMA_PERIOD,
        adjust=False,
    ).mean()

    return {
        "volume": volume,
        "sma": sma,
        "ema": ema,
    }


# ==========================================================
# RELATIVE VOLUME
# ==========================================================


def relative_volume(
    current,
    average,
):

    if average == 0:
        return 0

    return current / average


# ==========================================================
# VOLUME MOMENTUM
# ==========================================================


def volume_momentum(volume):

    current = volume.iloc[-1]

    previous = volume.iloc[-5]

    if current > previous:
        return "BULLISH"

    if current < previous:
        return "BEARISH"

    return "NEUTRAL"


# ==========================================================
# VOLUME ACCELERATION
# ==========================================================


def volume_acceleration(volume):

    slope = volume.iloc[-1] - volume.iloc[-5]

    if slope > 0:
        return "INCREASING"

    if slope < 0:
        return "DECREASING"

    return "FLAT"


# ==========================================================
# VOLUME SPIKE
# ==========================================================


def volume_spike(rvol):

    return rvol >= 2.0


# ==========================================================
# UNUSUAL VOLUME
# ==========================================================


def unusual_volume(rvol):

    return rvol >= 3.0


# ==========================================================
# DRY VOLUME
# ==========================================================


def dry_volume(rvol):

    return rvol <= 0.5


# ==========================================================
# CLIMAX VOLUME
# ==========================================================


def climax_volume(
    volume,
    sma,
):

    return volume > (sma * 4)


# ==========================================================
# BUYING PRESSURE
# ==========================================================


def buying_pressure(
    closes,
    volume,
    sma,
):

    closes = pd.Series(closes, dtype="float64")

    return closes.iloc[-1] > closes.iloc[-2] and volume > sma


# ==========================================================
# SELLING PRESSURE
# ==========================================================


def selling_pressure(
    closes,
    volume,
    sma,
):

    closes = pd.Series(closes, dtype="float64")

    return closes.iloc[-1] < closes.iloc[-2] and volume > sma


# ==========================================================
# VOLUME STRENGTH
# ==========================================================


def volume_strength(rvol):

    if rvol >= 4:
        return "EXTREME"

    if rvol >= 3:
        return "VERY_STRONG"

    if rvol >= 2:
        return "STRONG"

    if rvol >= 1:
        return "NORMAL"

    if rvol >= 0.5:
        return "LOW"

    return "VERY_LOW"


# ==========================================================
# BREAKOUT CONFIRMATION
# ==========================================================


def breakout_confirmation(
    closes,
    volume,
    sma,
):

    closes = pd.Series(closes, dtype="float64")

    return closes.iloc[-1] > closes.iloc[-2] and volume > sma * 1.5


# ==========================================================
# FAKE BREAKOUT
# ==========================================================


def fake_breakout(
    closes,
    volume,
    sma,
):

    closes = pd.Series(closes, dtype="float64")

    return closes.iloc[-1] > closes.iloc[-2] and volume < sma


# ==========================================================
# TREND CONFIRMATION
# ==========================================================


def trend_confirmation(
    closes,
    volume,
    sma,
):

    closes = pd.Series(closes, dtype="float64")

    move = abs(closes.iloc[-1] - closes.iloc[-2])

    return volume > sma and move > 0


# ==========================================================
# VOLUME EXHAUSTION
# ==========================================================


def volume_exhaustion(
    momentum,
    acceleration,
    climax,
):

    return (climax and momentum == "BULLISH" and acceleration == "DECREASING") or (
        climax and momentum == "BEARISH" and acceleration == "INCREASING"
    )


# ==========================================================
# CONTINUATION PROBABILITY
# ==========================================================


def continuation_probability(
    breakout,
    buying,
    selling,
):

    probability = 50

    if breakout:
        probability += 20

    if buying:
        probability += 15

    if selling:
        probability -= 15

    return max(
        0,
        min(
            round(probability),
            100,
        ),
    )


# ==========================================================
# AI SCORE
# ==========================================================


def ai_score(
    continuation,
    spike,
    unusual,
    exhaustion,
):

    score = continuation

    if spike:
        score += 10

    if unusual:
        score += 10

    if exhaustion:
        score -= 15

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


def analyze_volume(volumes, closes):

    volumes = pd.Series(volumes, dtype="float64")
    closes = pd.Series(closes, dtype="float64")

    if len(volumes) < 100:
        raise ValueError("At least 100 candles are required.")

    data = calculate_volume(volumes)

    volume = data["volume"]
    sma = data["sma"]
    ema = data["ema"]

    latest_volume = float(volume.iloc[-1])
    latest_sma = float(sma.iloc[-1])
    latest_ema = float(ema.iloc[-1])

    rvol = relative_volume(
        latest_volume,
        latest_sma,
    )

    momentum = volume_momentum(volume)

    acceleration = volume_acceleration(volume)

    spike = volume_spike(rvol)

    unusual = unusual_volume(rvol)

    dry = dry_volume(rvol)

    climax = climax_volume(
        latest_volume,
        latest_sma,
    )

    buying = buying_pressure(
        closes,
        latest_volume,
        latest_sma,
    )

    selling = selling_pressure(
        closes,
        latest_volume,
        latest_sma,
    )

    breakout = breakout_confirmation(
        closes,
        latest_volume,
        latest_sma,
    )

    fake = fake_breakout(
        closes,
        latest_volume,
        latest_sma,
    )

    trend = trend_confirmation(
        closes,
        latest_volume,
        latest_sma,
    )

    exhaustion = volume_exhaustion(
        momentum,
        acceleration,
        climax,
    )

    continuation = continuation_probability(
        breakout,
        buying,
        selling,
    )

    score = ai_score(
        continuation,
        spike,
        unusual,
        exhaustion,
    )

    return {
        "current_volume": round(latest_volume, 2),
        "volume_sma": round(latest_sma, 2),
        "volume_ema": round(latest_ema, 2),
        "relative_volume": round(rvol, 2),
        "momentum": momentum,
        "acceleration": acceleration,
        "volume_spike": spike,
        "unusual_volume": unusual,
        "dry_volume": dry,
        "climax_volume": climax,
        "strength": volume_strength(rvol),
        "buying_pressure": buying,
        "selling_pressure": selling,
        "breakout_confirmation": breakout,
        "fake_breakout": fake,
        "trend_confirmation": trend,
        "volume_exhaustion": exhaustion,
        "continuation_probability": continuation,
        "ai_score": score,
    }
