from django.core.management.base import BaseCommand

from market_data.models import Coin, FundingRate
from services.binance_service import BinanceService


class Command(BaseCommand):

    help = "Sync Binance Futures Funding Rate"

    def handle(self, *args, **kwargs):

        service = BinanceService()

        coins = Coin.objects.filter(is_active=True)

        total = 0

        for coin in coins:

            self.stdout.write(
                self.style.WARNING(f"\n========== {coin.symbol} ==========")
            )

            try:

                history = service.get_funding_rate(
                    symbol=coin.symbol,
                    limit=500
                )

                for item in history:

                    FundingRate.objects.update_or_create(

                        coin=coin,

                        funding_time=item["fundingTime"],

                        defaults={

                            "funding_rate": item["fundingRate"],

                            "mark_price": item["markPrice"],

                        }

                    )

                    total += 1

                self.stdout.write(
                    self.style.SUCCESS("✓ Funding Rate Synced")
                )

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"{coin.symbol} -> {e}"
                    )
                )

        self.stdout.write(

            self.style.SUCCESS(

                f"\n\n🎉 {total} Funding Rate records synced."

            )

        )