from statistics import mean

from core.market_data.cache import cache


class MomentumFeature:

    def calculate(self, symbol):

        trades = list(cache.trades[symbol])

        if len(trades) < 2:
            return None

        first_price = trades[0]["price"]
        last_price = trades[-1]["price"]

        price_change = last_price - first_price

        if first_price == 0:
            price_change_percent = 0
        else:
            price_change_percent = (price_change / first_price) * 100

        total_volume = sum(t["qty"] for t in trades)

        average_trade_size = mean(t["qty"] for t in trades)

        buy_volume = cache.delta_volume[symbol]["buy"]
        sell_volume = cache.delta_volume[symbol]["sell"]

        total_delta = buy_volume + sell_volume

        if total_delta == 0:
            buy_ratio = 0
            sell_ratio = 0
        else:
            buy_ratio = (buy_volume / total_delta) * 100
            sell_ratio = (sell_volume / total_delta) * 100

        trade_speed = len(trades)

        cvd = cache.cvd[symbol]

        momentum_score = (
            (price_change_percent * 2) + (buy_ratio - sell_ratio) + (cvd * 0.1)
        )

        if momentum_score > 20:
            direction = "STRONG_BULLISH"

        elif momentum_score > 5:
            direction = "BULLISH"

        elif momentum_score < -20:
            direction = "STRONG_BEARISH"

        elif momentum_score < -5:
            direction = "BEARISH"

        else:
            direction = "SIDEWAYS"

        return {
            "price_change": round(price_change, 8),
            "price_change_percent": round(
                price_change_percent,
                4,
            ),
            "trade_speed": trade_speed,
            "total_volume": round(
                total_volume,
                4,
            ),
            "average_trade_size": round(
                average_trade_size,
                4,
            ),
            "buy_volume": round(
                buy_volume,
                4,
            ),
            "sell_volume": round(
                sell_volume,
                4,
            ),
            "buy_ratio": round(
                buy_ratio,
                2,
            ),
            "sell_ratio": round(
                sell_ratio,
                2,
            ),
            "cvd": round(
                cvd,
                4,
            ),
            "momentum_score": round(
                momentum_score,
                2,
            ),
            "direction": direction,
        }


momentum_feature = MomentumFeature()
