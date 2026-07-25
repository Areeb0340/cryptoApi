from django.core.management.base import BaseCommand

import requests
import time

from market_data.models import Coin, TopTraderPositionRatio
from services.binance_service import BinanceService


TIMEFRAMES = [
    "5m",
    "15m",
    "30m",
    "1h",
    "4h",
    "1d",
]


class Command(BaseCommand):

    help = "Sync Binance Top Trader Position Ratio"

    def handle(self, *args, **kwargs):

        service = BinanceService()

        coins = Coin.objects.filter(is_active=True)

        total = 0

        for coin in coins:

            self.stdout.write(
                self.style.WARNING(
                    f"\n========== {coin.symbol} =========="
                )
            )

            for timeframe in TIMEFRAMES:

                try:

                    data = service.get_top_position_ratio(
                        symbol=coin.symbol,
                        timeframe=timeframe,
                        limit=500
                    )

                    for item in data:

                        TopTraderPositionRatio.objects.update_or_create(

                            coin=coin,

                            timeframe=timeframe,

                            timestamp=item["timestamp"],

                            defaults={

                                "long_short_ratio": item["longShortRatio"],

                                "long_account": item["longAccount"],

                                "short_account": item["shortAccount"],

                            }

                        )

                        total += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {timeframe} completed"
                        )
                    )

                    time.sleep(0.20)

                except requests.exceptions.RequestException as e:

                    self.stdout.write(
                        self.style.ERROR(
                            f"{coin.symbol} {timeframe} -> {e}"
                        )
                    )

                except Exception as e:

                    self.stdout.write(
                        self.style.ERROR(str(e))
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Finished! {total} Top Position Ratio records synced."
            )
        )