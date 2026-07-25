from core.market_data.cache import cache


class DepthHandler:

    async def __call__(self, data):

        symbol = data["s"]

        orderbook = {
            "event_time": data["E"],
            "symbol": symbol,
            "first_update_id": data["U"],
            "final_update_id": data["u"],
            "bids": [
                {
                    "price": float(price),
                    "qty": float(qty),
                }
                for price, qty in data["b"]
            ],
            "asks": [
                {
                    "price": float(price),
                    "qty": float(qty),
                }
                for price, qty in data["a"]
            ],
        }

        cache.update_orderbook(
            symbol,
            orderbook,
        )
