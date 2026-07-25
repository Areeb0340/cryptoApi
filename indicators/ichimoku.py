import pandas as pd


TENKAN = 9
KIJUN = 26
SENKOU_B = 52


def calculate_ichimoku(highs, lows, closes):

    high = pd.Series(highs, dtype=float)
    low = pd.Series(lows, dtype=float)
    close = pd.Series(closes, dtype=float)

    tenkan = (
        high.rolling(TENKAN).max() +
        low.rolling(TENKAN).min()
    ) / 2

    kijun = (
        high.rolling(KIJUN).max() +
        low.rolling(KIJUN).min()
    ) / 2

    senkou_a = (
        (tenkan + kijun) / 2
    ).shift(KIJUN)

    senkou_b = (
        (
            high.rolling(SENKOU_B).max() +
            low.rolling(SENKOU_B).min()
        ) / 2
    ).shift(KIJUN)

    chikou = close.shift(-KIJUN)

    return (
        tenkan,
        kijun,
        senkou_a,
        senkou_b,
        chikou,
    )


def analyze_ichimoku(highs, lows, closes):

    closes = pd.Series(closes, dtype=float)

    (
        tenkan,
        kijun,
        senkou_a,
        senkou_b,
        chikou,
    ) = calculate_ichimoku(
        highs,
        lows,
        closes,
    )

    price = float(closes.iloc[-1])

    tenkan_last = float(tenkan.iloc[-1])
    kijun_last = float(kijun.iloc[-1])

    span_a = float(senkou_a.iloc[-27])
    span_b = float(senkou_b.iloc[-27])

    cloud_top = max(span_a, span_b)
    cloud_bottom = min(span_a, span_b)

    bullish_cloud = span_a > span_b
    bearish_cloud = span_a < span_b

    price_above_cloud = price > cloud_top
    price_below_cloud = price < cloud_bottom
    inside_cloud = (
        cloud_bottom <= price <= cloud_top
    )

    bullish_tk_cross = (
        tenkan.iloc[-2] < kijun.iloc[-2]
        and
        tenkan.iloc[-1] > kijun.iloc[-1]
    )

    bearish_tk_cross = (
        tenkan.iloc[-2] > kijun.iloc[-2]
        and
        tenkan.iloc[-1] < kijun.iloc[-1]
    )

    cloud_thickness = abs(span_a - span_b)

    if cloud_thickness > price * 0.03:
        cloud_strength = "Very Strong"

    elif cloud_thickness > price * 0.02:
        cloud_strength = "Strong"

    elif cloud_thickness > price * 0.01:
        cloud_strength = "Moderate"

    else:
        cloud_strength = "Weak"

    future_cloud = (
        "Bullish"
        if bullish_cloud
        else "Bearish"
    )

    if (
        price_above_cloud
        and
        bullish_cloud
        and
        tenkan_last > kijun_last
    ):
        trend = "Strong Bullish"

    elif (
        price_below_cloud
        and
        bearish_cloud
        and
        tenkan_last < kijun_last
    ):
        trend = "Strong Bearish"

    elif inside_cloud:
        trend = "Neutral"

    elif price_above_cloud:
        trend = "Bullish"

    else:
        trend = "Bearish"

    ai_score = 50

    if price_above_cloud:
        ai_score += 15

    if price_below_cloud:
        ai_score -= 15

    if bullish_tk_cross:
        ai_score += 15

    if bearish_tk_cross:
        ai_score -= 15

    if bullish_cloud:
        ai_score += 10

    if bearish_cloud:
        ai_score -= 10

    if tenkan_last > kijun_last:
        ai_score += 10

    else:
        ai_score -= 10

    ai_score = max(0, min(100, ai_score))

    return {

        "price": round(price, 2),

        "tenkan": round(tenkan_last, 2),

        "kijun": round(kijun_last, 2),

        "senkou_a": round(span_a, 2),

        "senkou_b": round(span_b, 2),

        "cloud_top": round(cloud_top, 2),

        "cloud_bottom": round(cloud_bottom, 2),

        "cloud_thickness": round(cloud_thickness, 2),

        "cloud_strength": cloud_strength,

        "future_cloud": future_cloud,

        "bullish_cloud": bullish_cloud,

        "bearish_cloud": bearish_cloud,

        "price_above_cloud": price_above_cloud,

        "price_below_cloud": price_below_cloud,

        "inside_cloud": inside_cloud,

        "bullish_tk_cross": bullish_tk_cross,

        "bearish_tk_cross": bearish_tk_cross,

        "trend": trend,

        "ai_score": ai_score,

    }