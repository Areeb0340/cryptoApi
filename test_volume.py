import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from market_data.models import Candle
from indicators.volume import analyze_volume


TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
    "30m",
    "1h",
    "4h",
    "1d",
]


print("\n========== BTC VOLUME ANALYSIS ==========\n")

for timeframe in TIMEFRAMES:

    candles = Candle.objects.filter(
        coin__symbol="BTC/USDT:USDT",
        timeframe=timeframe
    ).order_by("timestamp")

    volumes = [float(c.volume) for c in candles]
    closes = [float(c.close) for c in candles]

    result = analyze_volume(volumes, closes)

    print(f"\n========== {timeframe} ==========")

    print("Current Volume        :", result["current_volume"])
    print("Volume SMA (20)       :", result["volume_sma"])
    print("Volume EMA (20)       :", result["volume_ema"])
    print("Relative Volume       :", result["relative_volume"])

    print("High Volume           :", result["high_volume"])
    print("Low Volume            :", result["low_volume"])

    print("Increasing            :", result["increasing"])
    print("Decreasing            :", result["decreasing"])

    print("Volume Spike          :", result["volume_spike"])
    print("Unusual Volume        :", result["unusual_volume"])
    print("Dry Volume            :", result["dry_volume"])

    print("Strength              :", result["strength"])

    print("Buying Pressure       :", result["buying_pressure"])
    print("Selling Pressure      :", result["selling_pressure"])

    print("Breakout Confirmation :", result["breakout_confirmation"])
    print("Fake Breakout         :", result["fake_breakout"])
    print("Trend Confirmation    :", result["trend_confirmation"])

    print("AI Score              :", result["score"])