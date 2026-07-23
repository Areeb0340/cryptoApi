from core.market_data.cache import cache


class OrderBookFeatures:

    def __init__(self):
        self.data = {}

    def update(self, symbol):

        orderbook = cache.orderbooks.get(symbol)

        if not orderbook:
            return

        bids = orderbook["bids"]
        asks = orderbook["asks"]

        if not bids or not asks:
            return

        best_bid = float(bids[0][0])
        best_ask = float(asks[0][0])

        spread = best_ask - best_bid
        mid_price = (best_bid + best_ask) / 2

        spread_percent = (spread / mid_price) * 100 if mid_price else 0

        bid_volume = sum(float(b[1]) for b in bids)
        ask_volume = sum(float(a[1]) for a in asks)

        total_volume = bid_volume + ask_volume

        if total_volume == 0:
            imbalance = 0
        else:
            imbalance = (bid_volume - ask_volume) / total_volume

        if ask_volume == 0:
            bid_ask_ratio = 0
        else:
            bid_ask_ratio = bid_volume / ask_volume

        if imbalance > 0.20:
            pressure = "BUY"

        elif imbalance < -0.20:
            pressure = "SELL"

        else:
            pressure = "NEUTRAL"

        self.data[symbol] = {
            "best_bid": best_bid,
            "best_ask": best_ask,
            "mid_price": mid_price,
            "spread": spread,
            "spread_percent": spread_percent,
            "bid_volume": bid_volume,
            "ask_volume": ask_volume,
            "bid_ask_ratio": bid_ask_ratio,
            "imbalance": imbalance,
            "pressure": pressure,
        }

        print(symbol, self.data[symbol])


orderbook_features = OrderBookFeatures()
