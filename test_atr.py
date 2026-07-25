import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from market_data.models import Candle
from indicators.atr import analyze_atr


TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
    "30m",
    "1h",
    "4h",
    "1d",
]


print("\n========== BTC ATR ANALYSIS ==========\n")

for timeframe in TIMEFRAMES:

    candles = Candle.objects.filter(
        coin__symbol="BTC/USDT:USDT",
        timeframe=timeframe
    ).order_by("timestamp")

    highs = [float(c.high) for c in candles]
    lows = [float(c.low) for c in candles]
    closes = [float(c.close) for c in candles]

    result = analyze_atr(highs, lows, closes)

    print(f"\n========== {timeframe} ==========")

    print("ATR                :", result["atr"])
    print("ATR SMA            :", result["atr_sma"])

    print("High Volatility    :", result["high_volatility"])
    print("Low Volatility     :", result["low_volatility"])

    print("Increasing ATR     :", result["increasing"])
    print("Decreasing ATR     :", result["decreasing"])

    print("Strength           :", result["strength"])

    print("Trend Friendly     :", result["trend_friendly"])
    print("Breakout Ready     :", result["breakout_ready"])
    print("Choppy Market      :", result["choppy_market"])

    print("SL (1x ATR)        :", result["stop_loss_1x"])
    print("SL (1.5x ATR)      :", result["stop_loss_1_5x"])
    print("SL (2x ATR)        :", result["stop_loss_2x"])

    print("TP (2x ATR)        :", result["take_profit_2x"])
    print("TP (3x ATR)        :", result["take_profit_3x"])

    print("AI Score           :", result["score"])