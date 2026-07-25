from django.core.management.base import BaseCommand
from django.utils import timezone

from market_data.models import Coin, MarkPrice
from services.binance_service import BinanceService


class Command(BaseCommand):

    help = "Sync Binance Futures Mark Price"

    def handle(self, *args, **kwargs):

        service = BinanceService()

        self.stdout.write(
            self.style.WARNING("Downloading Mark Prices...")
        )

        data = service.get_mark_price()

        total = 0

        for item in data:

            symbol = (
                item["symbol"]
                .replace("USDT", "/USDT:USDT")
            )

            try:

                coin = Coin.objects.get(symbol=symbol)

            except Coin.DoesNotExist:
                continue

            MarkPrice.objects.update_or_create(

                coin=coin,

                timestamp=item["time"],

                defaults={

                    "mark_price": item["markPrice"],

                    "index_price": item["indexPrice"],

                    "estimated_settle_price": item.get(
                        "estimatedSettlePrice",
                        0
                    ),

                    "funding_rate": item["lastFundingRate"],

                    "next_funding_time": item["nextFundingTime"],

                }

            )

            total += 1

        self.stdout.write(

            self.style.SUCCESS(

                f"✅ {total} Mark Prices Synced."

            )

        )