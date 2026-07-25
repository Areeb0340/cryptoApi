import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from market_data.models import Candle
from indicators.macd import analyze_macd


TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
    "30m",
    "1h",
    "4h",
    "1d",
]


print("\n========== BTC MACD ANALYSIS ==========\n")

for timeframe in TIMEFRAMES:

    candles = Candle.objects.filter(
        coin__symbol="BTC/USDT:USDT",
        timeframe=timeframe
    ).order_by("timestamp")

    closes = [float(c.close) for c in candles]

    result = analyze_macd(closes)

    print(f"\n========== {timeframe} ==========")

    print("MACD Line        :", round(result["macd"], 4))
    print("Signal Line      :", round(result["signal"], 4))
    print("Histogram        :", round(result["histogram"], 4))

    print("Bullish Cross    :", result["bullish_cross"])
    print("Bearish Cross    :", result["bearish_cross"])

    print("Above Zero       :", result["above_zero"])
    print("Below Zero       :", result["below_zero"])

    print("Bullish Momentum :", result["bullish_momentum"])
    print("Bearish Momentum :", result["bearish_momentum"])

    print("Trend            :", result["trend"])

    print("Momentum Strength:", result["momentum_strength"])

    print("AI Score         :", result["score"])