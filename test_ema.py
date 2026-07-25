import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from market_data.models import Candle
from indicators.ema import analyze_ema

candles = Candle.objects.filter(
    coin__symbol="BTC/USDT:USDT",
    timeframe="1h"
).order_by("timestamp")

closes = [float(candle.close) for candle in candles]

result = analyze_ema(closes)

print("\n========== EMA ANALYSIS ==========\n")

print("EMA 20 :", round(result["ema20"], 2))
print("EMA 50 :", round(result["ema50"], 2))
print("EMA 100:", round(result["ema100"], 2))
print("EMA 200:", round(result["ema200"], 2))

print("\nBullish Alignment :", result["bullish_alignment"])
print("Bearish Alignment :", result["bearish_alignment"])
print("Golden Cross      :", result["golden_cross"])
print("Death Cross       :", result["death_cross"])