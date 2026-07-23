import time
import requests

from django.core.management.base import BaseCommand, CommandParser

from market_data.models import Coin, Candle
from services.binance_service import BinanceService

TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
    "30m",
    "1h",
    "4h",
    "1d",
]

MAX_RETRIES = 3
RETRY_DELAY = 5


class Command(BaseCommand):

    help = "Download Binance Futures Candles"

    def add_arguments(self, parser: CommandParser):

        parser.add_argument(
            "--start",
            type=int,
            default=0,
            help="Start Coin Index",
        )

        parser.add_argument(
            "--end",
            type=int,
            default=None,
            help="End Coin Index",
        )

        parser.add_argument(
            "--limit",
            type=int,
            default=1000,
            help="Number of candles",
        )

    def handle(self, *args, **options):

        service = BinanceService()
        start = options["start"]
        end = options["end"]
        limit = options["limit"]

        all_coins = Coin.objects.filter(is_active=True).order_by("id")

        total_coins = all_coins.count()

        coins = all_coins[start:end]

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDownloading Coins {start} -> {end if end else total_coins}"
            )
        )

        total_saved = 0
        completed = 0
        failed = []

        for coin in coins:

            self.stdout.write(
                self.style.WARNING(f"\n========== {coin.symbol} ==========")
            )

            coin_success = True

            for timeframe in TIMEFRAMES:

                self.stdout.write(f"Downloading {timeframe}...")

                candles = None

                for attempt in range(1, MAX_RETRIES + 1):

                    try:

                        candles = service.get_klines(
                            symbol=coin.symbol,
                            timeframe=timeframe,
                            limit=limit,
                        )

                        break

                    except requests.exceptions.RequestException as e:

                        self.stdout.write(
                            self.style.WARNING(f"Retry {attempt}/{MAX_RETRIES}: {e}")
                        )

                        if attempt < MAX_RETRIES:
                            time.sleep(RETRY_DELAY)

                    except Exception as e:

                        self.stdout.write(
                            self.style.WARNING(f"Retry {attempt}/{MAX_RETRIES}: {e}")
                        )

                        if attempt < MAX_RETRIES:
                            time.sleep(RETRY_DELAY)

                if candles is None:

                    coin_success = False

                    failed.append(f"{coin.symbol} [{timeframe}]")

                    self.stdout.write(self.style.ERROR(f"✗ Failed {timeframe}"))

                    continue

                try:

                    for candle in candles:

                        Candle.objects.update_or_create(
                            coin=coin,
                            timeframe=timeframe,
                            timestamp=candle[0],
                            defaults={
                                "open": candle[1],
                                "high": candle[2],
                                "low": candle[3],
                                "close": candle[4],
                                "volume": candle[5],
                                "quote_volume": candle[7],
                                "trades": candle[8],
                                "taker_buy_base_volume": candle[9],
                                "taker_buy_quote_volume": candle[10],
                            },
                        )

                        total_saved += 1

                    self.stdout.write(self.style.SUCCESS(f"✓ {timeframe} completed"))

                    time.sleep(0.20)

                except Exception as e:

                    coin_success = False

                    failed.append(f"{coin.symbol} [{timeframe}]")

                    self.stdout.write(self.style.ERROR(str(e)))

            if coin_success:
                completed += 1

        self.stdout.write("\n")
        self.stdout.write("=" * 70)

        self.stdout.write(
            self.style.SUCCESS(f"Coins Completed : {completed}/{len(coins)}")
        )

        self.stdout.write(self.style.SUCCESS(f"Candles Processed : {total_saved}"))

        self.stdout.write(self.style.ERROR(f"Failed Tasks : {len(failed)}"))

        if failed:

            self.stdout.write("\nFailed Tasks:\n")

            for item in failed:
                self.stdout.write(self.style.ERROR(item))

        self.stdout.write("=" * 70)

        self.stdout.write(self.style.SUCCESS("\n🎉 Candle Sync Finished Successfully."))
