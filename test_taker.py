import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from market_data.models import Coin
from indicators.taker_analysis import TakerAnalysis

coins = Coin.objects.filter(is_active=True)

for coin in coins:

    print(f"\n{'='*20}")
    print(coin.symbol)
    print(f"{'='*20}")

    result = TakerAnalysis.analyze(coin)

    for timeframe, data in result.items():

        print(f"\n========== {timeframe} ==========\n")

        for key, value in data.items():
            print(f"{key:22}: {value}")