from core.market_data.cache import cache


class BookTickerHandler:

    async def __call__(self, data):

        symbol = data["s"]

        ticker = {
            "update_id": data["u"],
            "symbol": symbol,
            "best_bid": float(data["b"]),
            "best_bid_qty": float(data["B"]),
            "best_ask": float(data["a"]),
            "best_ask_qty": float(data["A"]),
        }

        cache.update_bookticker(
            symbol,
            ticker,
        )
