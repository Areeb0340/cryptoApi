import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from market_data.models import Candle
from indicators.rsi import calculate_rsi

candles = Candle.objects.filter(
    coin__symbol="BTC/USDT:USDT",
    timeframe="1h"
).order_by("timestamp")

closes = [float(candle.close) for candle in candles]

rsi = calculate_rsi(closes)

print("Latest RSI:", round(rsi.iloc[-1], 2))