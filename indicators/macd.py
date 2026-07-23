import numpy as np
import pandas as pd

FAST = 12
SLOW = 26
SIGNAL = 9


# ==========================================================
# CALCULATE MACD
# ==========================================================


def calculate_macd(closes):

    closes = pd.Series(closes, dtype="float64")

    ema_fast = closes.ewm(
        span=FAST,
        adjust=False,
    ).mean()

    ema_slow = closes.ewm(
        span=SLOW,
        adjust=False,
    ).mean()

    macd = ema_fast - ema_slow

    signal = macd.ewm(
        span=SIGNAL,
        adjust=False,
    ).mean()

    histogram = macd - signal

    return {
        "macd": macd,
        "signal": signal,
        "histogram": histogram,
    }


# ==========================================================
# MACD SLOPE
# ==========================================================


def macd_slope(macd):

    return round(
        float(macd.iloc[-1] - macd.iloc[-5]),
        4,
    )


# ==========================================================
# SIGNAL SLOPE
# ==========================================================


def signal_slope(signal):

    return round(
        float(signal.iloc[-1] - signal.iloc[-5]),
        4,
    )


# ==========================================================
# HISTOGRAM SLOPE
# ==========================================================


def histogram_slope(histogram):

    return round(
        float(histogram.iloc[-1] - histogram.iloc[-5]),
        4,
    )


# ==========================================================
# ZERO LINE
# ==========================================================


def zero_line(macd):

    value = macd.iloc[-1]

    if value > 0:
        return "ABOVE"

    if value < 0:
        return "BELOW"

    return "ZERO"


# ==========================================================
# MACD CROSS
# ==========================================================


def macd_cross(macd, signal):

    bullish = macd.iloc[-2] <= signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]

    bearish = macd.iloc[-2] >= signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]

    return {
        "bullish": bullish,
        "bearish": bearish,
    }


# ==========================================================
# ZERO LINE CROSS
# ==========================================================


def zero_cross(macd):

    bullish = macd.iloc[-2] <= 0 and macd.iloc[-1] > 0

    bearish = macd.iloc[-2] >= 0 and macd.iloc[-1] < 0

    return {
        "bullish": bullish,
        "bearish": bearish,
    }


# ==========================================================
# MOMENTUM
# ==========================================================


def momentum(histogram):

    value = histogram.iloc[-1]

    if value > 0:
        return "BULLISH"

    if value < 0:
        return "BEARISH"

    return "NEUTRAL"


# ==========================================================
# MOMENTUM ACCELERATION
# ==========================================================


def momentum_acceleration(histogram):

    current = histogram.iloc[-1]

    previous = histogram.iloc[-5]

    if current > previous:
        return "INCREASING"

    if current < previous:
        return "DECREASING"

    return "FLAT"


# ==========================================================
# TREND STRENGTH
# ==========================================================


def trend_strength(
    macd,
    signal,
):

    distance = abs(macd.iloc[-1] - signal.iloc[-1])

    if distance > 2:

        return "EXTREME"

    if distance > 1:

        return "STRONG"

    if distance > 0.5:

        return "MODERATE"

    return "WEAK"


# ==========================================================
# BULLISH DIVERGENCE
# ==========================================================


def bullish_divergence(closes, macd):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    price_lower_low = closes.iloc[-1] < closes.iloc[-6]

    macd_higher_low = macd.iloc[-1] > macd.iloc[-6]

    return price_lower_low and macd_higher_low


# ==========================================================
# BEARISH DIVERGENCE
# ==========================================================


def bearish_divergence(closes, macd):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    price_higher_high = closes.iloc[-1] > closes.iloc[-6]

    macd_lower_high = macd.iloc[-1] < macd.iloc[-6]

    return price_higher_high and macd_lower_high


# ==========================================================
# HIDDEN BULLISH DIVERGENCE
# ==========================================================


def hidden_bullish_divergence(closes, macd):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    price_higher_low = closes.iloc[-1] > closes.iloc[-6]

    macd_lower_low = macd.iloc[-1] < macd.iloc[-6]

    return price_higher_low and macd_lower_low


# ==========================================================
# HIDDEN BEARISH DIVERGENCE
# ==========================================================


def hidden_bearish_divergence(closes, macd):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:
        return False

    price_lower_high = closes.iloc[-1] < closes.iloc[-6]

    macd_higher_high = macd.iloc[-1] > macd.iloc[-6]

    return price_lower_high and macd_higher_high


# ==========================================================
# CONTINUATION PROBABILITY
# ==========================================================


def continuation_probability(
    trend,
    acceleration,
):

    probability = 50

    if trend == "EXTREME":
        probability += 25

    elif trend == "STRONG":
        probability += 15

    elif trend == "MODERATE":
        probability += 8

    if acceleration == "INCREASING":
        probability += 10

    elif acceleration == "DECREASING":
        probability -= 10

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
    cross,
    zero,
    trend,
    continuation,
    bull_div,
    bear_div,
):

    score = 50

    if cross["bullish"]:
        score += 15

    if cross["bearish"]:
        score -= 15

    if zero["bullish"]:
        score += 10

    if zero["bearish"]:
        score -= 10

    if trend == "EXTREME":
        score += 15

    elif trend == "STRONG":
        score += 10

    elif trend == "MODERATE":
        score += 5

    score += (continuation - 50) * 0.20

    if bull_div:
        score += 10

    if bear_div:
        score -= 10

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


def analyze_macd(closes):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 100:
        raise ValueError("At least 100 candles are required.")

    data = calculate_macd(closes)

    macd = data["macd"]
    signal = data["signal"]
    histogram = data["histogram"]

    latest_macd = float(macd.iloc[-1])
    latest_signal = float(signal.iloc[-1])
    latest_histogram = float(histogram.iloc[-1])

    macdSlope = macd_slope(macd)
    signalSlope = signal_slope(signal)
    histogramSlope = histogram_slope(histogram)

    zero = zero_line(macd)

    cross = macd_cross(macd, signal)

    zeroCross = zero_cross(macd)

    momentumState = momentum(histogram)

    acceleration = momentum_acceleration(histogram)

    trend = trend_strength(macd, signal)

    bullDiv = bullish_divergence(closes, macd)

    bearDiv = bearish_divergence(closes, macd)

    hiddenBull = hidden_bullish_divergence(closes, macd)

    hiddenBear = hidden_bearish_divergence(closes, macd)

    continuation = continuation_probability(
        trend,
        acceleration,
    )

    score = ai_score(
        cross,
        zeroCross,
        trend,
        continuation,
        bullDiv,
        bearDiv,
    )

    return {
        "macd": round(latest_macd, 4),
        "signal": round(latest_signal, 4),
        "histogram": round(latest_histogram, 4),
        "macd_slope": macdSlope,
        "signal_slope": signalSlope,
        "histogram_slope": histogramSlope,
        "zero_line": zero,
        "bullish_cross": cross["bullish"],
        "bearish_cross": cross["bearish"],
        "bullish_zero_cross": zeroCross["bullish"],
        "bearish_zero_cross": zeroCross["bearish"],
        "momentum": momentumState,
        "momentum_acceleration": acceleration,
        "trend_strength": trend,
        "bullish_divergence": bullDiv,
        "bearish_divergence": bearDiv,
        "hidden_bullish_divergence": hiddenBull,
        "hidden_bearish_divergence": hiddenBear,
        "continuation_probability": continuation,
        "ai_score": score,
    }
