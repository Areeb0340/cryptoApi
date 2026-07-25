from statistics import mean

from core.market_data.cache import cache


class VolumeFeature:

    def get(self, symbol):

        symbol = symbol.upper()

        trades = list(cache.trades[symbol])

        if not trades:
            return None

        buy_volume = cache.delta_volume[symbol]["buy"]
        sell_volume = cache.delta_volume[symbol]["sell"]

        total_volume = buy_volume + sell_volume

        if total_volume == 0:
            delta_percent = 0
        else:
            delta_percent = ((buy_volume - sell_volume) / total_volume) * 100

        prices = [trade["price"] for trade in trades]
        quantities = [trade["qty"] for trade in trades]

        return {
            "trade_count": len(trades),
            "buy_volume": round(buy_volume, 4),
            "sell_volume": round(sell_volume, 4),
            "total_volume": round(total_volume, 4),
            "delta_volume": round(
                buy_volume - sell_volume,
                4,
            ),
            "delta_percent": round(
                delta_percent,
                2,
            ),
            "cvd": round(
                cache.cvd[symbol],
                4,
            ),
            "average_trade_size": round(
                mean(quantities),
                6,
            ),
            "largest_trade": round(
                max(quantities),
                6,
            ),
            "average_price": round(
                mean(prices),
                4,
            ),
            "last_price": round(
                prices[-1],
                4,
            ),
        }


volume_feature = VolumeFeature()
