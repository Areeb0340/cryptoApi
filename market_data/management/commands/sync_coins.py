from django.core.management.base import BaseCommand
from market_data.models import Coin
from services.binance_service import BinanceService


class Command(BaseCommand):
    help = "Sync Binance Futures Coins"

    def handle(self, *args, **kwargs):

        self.stdout.write("Fetching Binance Futures Coins...")

        service = BinanceService()

        markets = service.get_markets()

        total = 0

        for symbol, market in markets.items():

            Coin.objects.update_or_create(
                symbol=symbol,
                defaults={
                    "base_asset": market["base"],
                    "quote_asset": market["quote"],
                    "exchange": "binance",
                    "is_active": True,
                },
            )

            total += 1

        self.stdout.write(
            self.style.SUCCESS(f"✅ {total} coins synced successfully!")
        )