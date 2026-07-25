from django.core.management.base import BaseCommand

from market_data.models import Coin, OpenInterest
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

    help = "Sync Binance Futures Open Interest"

    def handle(self, *args, **kwargs):

        service = BinanceService()

        coins = Coin.objects.filter(is_active=True)

        total = 0

        for coin in coins:

            self.stdout.write(
                self.style.WARNING(f"\n========== {coin.symbol} ==========")
            )

            for timeframe in TIMEFRAMES:

                try:

                    history = service.get_open_interest_history(
                        symbol=coin.symbol,
                        timeframe=timeframe,
                        limit=500
                    )

                    for item in history:

                        OpenInterest.objects.update_or_create(

                            coin=coin,

                            timeframe=timeframe,

                            timestamp=item["timestamp"],

                            defaults={

                                "open_interest": item["sumOpenInterest"],

                                "open_interest_value": item["sumOpenInterestValue"],

                            }

                        )

                        total += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {timeframe} completed"
                        )
                    )

                except Exception as e:

                    self.stdout.write(
                        self.style.ERROR(
                            f"{coin.symbol} {timeframe} -> {e}"
                        )
                    )

        self.stdout.write(

            self.style.SUCCESS(

                f"\n\n🎉 {total} Open Interest records synced."

            )

        )