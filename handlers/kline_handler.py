from core.market_data.cache import cache


class KlineHandler:

    async def __call__(self, data):

        k = data["k"]

        symbol = data["s"]

        timeframe = k["i"]

        candle = {
            "open_time": k["t"],
            "close_time": k["T"],
            "symbol": symbol,
            "timeframe": timeframe,
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"]),
            "closed": k["x"],
        }

        cache.update_candle(
            symbol,
            timeframe,
            candle,
        )
