from market_data.models import Candle
from core.market_data.cache import cache

TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
    "30m",
    "1h",
    "4h",
    "1d",
]


class CandleLoader:

    def load(self, symbols=None):

        print("=" * 80)
        print("Loading Candles Into Memory...")
        print("=" * 80)

        total = 0

        # ----------------------------
        # Only selected symbols
        # ----------------------------

        if symbols is None:

            symbols = list(
                Candle.objects.values_list(
                    "coin__symbol",
                    flat=True,
                ).distinct()
            )

        for symbol in symbols:

            for timeframe in TIMEFRAMES:

                candles = Candle.objects.filter(
                    coin__symbol=symbol,
                    timeframe=timeframe,
                ).order_by("-timestamp")[:600]

                candles = list(reversed(candles))

                cache.klines[symbol][timeframe].clear()

                for c in candles:

                    cache.klines[symbol][timeframe].append(
                        {
                            "open_time": c.timestamp,
                            "open": float(c.open),
                            "high": float(c.high),
                            "low": float(c.low),
                            "close": float(c.close),
                            "volume": float(c.volume),
                            "closed": True,
                        }
                    )

                    total += 1

                print(
                    f"{symbol:<15} {timeframe:<4} "
                    f"{len(cache.klines[symbol][timeframe])}"
                )

        print("=" * 80)
        print(f"Loaded {total} candles")
        print("=" * 80)


candle_loader = CandleLoader()
