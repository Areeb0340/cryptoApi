from core.market_data.cache import cache


class TradeHandler:

    async def __call__(self, data):

        symbol = data["s"]

        trade = {
            "event_time": data["E"],
            "trade_id": data["t"],
            "symbol": symbol,
            "price": float(data["p"]),
            "qty": float(data["q"]),
            "trade_time": data["T"],
            "buyer_is_maker": data["m"],
        }

        cache.update_trade(symbol, trade)
