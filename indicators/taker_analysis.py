import pandas as pd

from market_data.models import Candle

# ==========================================================
# CONSTANTS
# ==========================================================

DELTA_EMA = 20
IMBALANCE_THRESHOLD = 2.0
AGGRESSIVE_THRESHOLD = 10


# ==========================================================
# DELTA EMA
# ==========================================================


def delta_ema(delta):

    return delta.ewm(
        span=DELTA_EMA,
        adjust=False,
    ).mean()


# ==========================================================
# DELTA MOMENTUM
# ==========================================================


def delta_momentum(delta):

    current = delta.iloc[-1]

    previous = delta.iloc[-5]

    if current > previous:
        return "BULLISH"

    if current < previous:
        return "BEARISH"

    return "NEUTRAL"


# ==========================================================
# DELTA ACCELERATION
# ==========================================================


def delta_acceleration(delta):

    slope = delta.iloc[-1] - delta.iloc[-5]

    if slope > 0:
        return "INCREASING"

    if slope < 0:
        return "DECREASING"

    return "FLAT"


# ==========================================================
# BUY / SELL PRESSURE
# ==========================================================


def pressure(
    buy_percent,
    sell_percent,
):

    if buy_percent > sell_percent:
        return "BUY"

    if sell_percent > buy_percent:
        return "SELL"

    return "NEUTRAL"


# ==========================================================
# DELTA TREND
# ==========================================================


def delta_trend(delta):

    if delta.tail(5).is_monotonic_increasing:
        return "INCREASING"

    if delta.tail(5).is_monotonic_decreasing:
        return "DECREASING"

    return "SIDEWAYS"


# ==========================================================
# AGGRESSIVE BUYERS
# ==========================================================


def aggressive_buyers(
    buy_percent,
    avg_buy_percent,
):

    return buy_percent > (avg_buy_percent + AGGRESSIVE_THRESHOLD)


# ==========================================================
# AGGRESSIVE SELLERS
# ==========================================================


def aggressive_sellers(
    sell_percent,
    avg_buy_percent,
):

    average_sell = 100 - avg_buy_percent

    return sell_percent > (average_sell + AGGRESSIVE_THRESHOLD)


# ==========================================================
# BUY IMBALANCE
# ==========================================================


def buy_imbalance(
    delta,
    avg_delta,
):

    return delta > (avg_delta * IMBALANCE_THRESHOLD)


# ==========================================================
# SELL IMBALANCE
# ==========================================================


def sell_imbalance(
    delta,
    avg_delta,
):

    return delta < (avg_delta * -IMBALANCE_THRESHOLD)


# ==========================================================
# SMART MONEY BUYING
# ==========================================================


def smart_money_buying(
    aggressive,
    imbalance,
    trend,
):

    return aggressive and imbalance and trend == "INCREASING"


# ==========================================================
# SMART MONEY SELLING
# ==========================================================


def smart_money_selling(
    aggressive,
    imbalance,
    trend,
):

    return aggressive and imbalance and trend == "DECREASING"


# ==========================================================
# ABSORPTION DETECTION
# ==========================================================


def absorption(
    buy_percent,
    sell_percent,
    delta,
):

    return (buy_percent > 60 and delta < 0) or (sell_percent > 60 and delta > 0)


# ==========================================================
# EXHAUSTION DETECTION
# ==========================================================


def exhaustion(
    momentum,
    acceleration,
):

    return (momentum == "BULLISH" and acceleration == "DECREASING") or (
        momentum == "BEARISH" and acceleration == "INCREASING"
    )


# ==========================================================
# DELTA DIVERGENCE
# ==========================================================


def delta_divergence(
    closes,
    delta,
):

    closes = pd.Series(closes, dtype="float64")

    if len(closes) < 10:

        return "NONE"

    if closes.iloc[-1] > closes.iloc[-6] and delta.iloc[-1] < delta.iloc[-6]:

        return "BEARISH"

    if closes.iloc[-1] < closes.iloc[-6] and delta.iloc[-1] > delta.iloc[-6]:

        return "BULLISH"

    return "NONE"


# ==========================================================
# CONTINUATION PROBABILITY
# ==========================================================


def continuation_probability(
    smart_buy,
    smart_sell,
    pressure,
):

    probability = 50

    if smart_buy:

        probability += 25

    if smart_sell:

        probability -= 25

    if pressure == "BUY":

        probability += 10

    elif pressure == "SELL":

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
    continuation,
    absorption_state,
    exhaustion_state,
    divergence,
):

    score = continuation

    if absorption_state:

        score += 10

    if exhaustion_state:

        score -= 10

    if divergence == "BULLISH":

        score += 10

    elif divergence == "BEARISH":

        score -= 10

    return max(
        0,
        min(
            round(score),
            100,
        ),
    )


class TakerAnalysis:

    @staticmethod
    def analyze(coin):

        result = {}

        for timeframe in TIMEFRAMES:

            candles = Candle.objects.filter(coin=coin, timeframe=timeframe).order_by(
                "-timestamp"
            )[:100]

            if candles.count() < 20:
                continue

            df = pd.DataFrame(
                list(
                    candles.values(
                        "volume",
                        "taker_buy_base_volume",
                    )
                )
            )

            df = df.iloc[::-1].reset_index(drop=True)

            df["volume"] = df["volume"].astype(float)
            df["buy_volume"] = df["taker_buy_base_volume"].astype(float)
            df["sell_volume"] = df["volume"] - df["buy_volume"]

            # -----------------------------
            # Order Flow Calculations
            # -----------------------------

            df["buy_percent"] = (df["buy_volume"] / df["volume"]) * 100

            df["sell_percent"] = (df["sell_volume"] / df["volume"]) * 100

            df["delta"] = df["buy_volume"] - df["sell_volume"]

            df["delta_percent"] = (df["delta"] / df["volume"]) * 100

            df["avg_buy_percent"] = df["buy_percent"].rolling(20).mean()

            df["avg_delta"] = df["delta"].rolling(20).mean()

            df["cvd"] = df["delta"].cumsum()

            df["delta_ema"] = delta_ema(df["delta"])

            # -----------------------------
            # Latest Values
            # -----------------------------

            buy = df["buy_volume"].iloc[-1]
            sell = df["sell_volume"].iloc[-1]
            total = df["volume"].iloc[-1]

            buy_percent = df["buy_percent"].iloc[-1]
            sell_percent = df["sell_percent"].iloc[-1]

            delta = df["delta"].iloc[-1]
            delta_percent = df["delta_percent"].iloc[-1]

            avg_buy_percent = df["avg_buy_percent"].iloc[-1]
            avg_delta = df["avg_delta"].iloc[-1]

            cvd = df["cvd"].iloc[-1]

            momentum = delta_momentum(df["delta"])

            acceleration = delta_acceleration(df["delta"])

            pressure_state = pressure(
                buy_percent,
                sell_percent,
            )

            trend = delta_trend(df["delta"])

            # -----------------------------
            # Delta Trend
            # -----------------------------

            delta_trend = "Neutral"

            if df["delta"].tail(5).is_monotonic_increasing:
                delta_trend = "Increasing"

            elif df["delta"].tail(5).is_monotonic_decreasing:
                delta_trend = "Decreasing"

            # -----------------------------
            # Dynamic Order Flow
            # -----------------------------

            buyers = aggressive_buyers(
                buy_percent,
                avg_buy_percent,
            )

            sellers = aggressive_sellers(
                sell_percent,
                avg_buy_percent,
            )

            buySide = buy_imbalance(
                delta,
                avg_delta,
            )

            sellSide = sell_imbalance(
                delta,
                avg_delta,
            )

            smartBuy = smart_money_buying(
                buyers,
                buySide,
                trend,
            )

            smartSell = smart_money_selling(
                sellers,
                sellSide,
                trend,
            )

            absorptionState = absorption(
                buy_percent,
                sell_percent,
                delta,
            )

            exhaustionState = exhaustion(
                momentum,
                acceleration,
            )

            divergence = delta_divergence(
                df["buy_volume"],
                df["delta"],
            )

            continuation = continuation_probability(
                smartBuy,
                smartSell,
                pressure_state,
            )

            score = ai_score(
                continuation,
                absorptionState,
                exhaustionState,
                divergence,
            )
            # -----------------------------
            # AI Score
            # -----------------------------

            ai_score = 50

            if aggressive_buyers:
                ai_score += 10

            if buy_imbalance:
                ai_score += 20

            if smart_money_buying:
                ai_score += 20

            if aggressive_sellers:
                ai_score -= 10

            if sell_imbalance:
                ai_score -= 20

            if smart_money_selling:
                ai_score -= 20

            ai_score = max(0, min(100, ai_score))

            # -----------------------------
            # Output
            # -----------------------------

            result[timeframe] = {
                "buy_volume": round(buy, 2),
                "sell_volume": round(sell, 2),
                "buy_percent": round(buy_percent, 2),
                "sell_percent": round(sell_percent, 2),
                "avg_buy_percent": round(avg_buy_percent, 2),
                "delta": round(delta, 2),
                "avg_delta": round(avg_delta, 2),
                "delta_percent": round(delta_percent, 2),
                "cvd": round(cvd, 2),
                "delta_trend": delta_trend,
                "aggressive_buyers": aggressive_buyers,
                "aggressive_sellers": aggressive_sellers,
                "buy_imbalance": buy_imbalance,
                "sell_imbalance": sell_imbalance,
                "smart_money_buying": smart_money_buying,
                "smart_money_selling": smart_money_selling,
                "ai_score": ai_score,
            }

        return result
