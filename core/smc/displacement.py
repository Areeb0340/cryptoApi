from collections import defaultdict

from core.market_data.cache import cache


class Displacement:

    def __init__(self):

        self.moves = defaultdict(lambda: defaultdict(dict))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 20:
            return

        current = candles[-1]

        body = abs(current["close"] - current["open"])

        candle_range = current["high"] - current["low"]

        if candle_range == 0:
            return

        body_percent = body / candle_range

        avg_range = sum(c["high"] - c["low"] for c in candles[-11:-1]) / 10

        expansion = candle_range / avg_range if avg_range else 0

        bullish = current["close"] > current["open"]
        bearish = current["close"] < current["open"]

        score = 0

        if body_percent > 0.70:
            score += 40

        if expansion > 1.5:
            score += 40

        if current["volume"] > candles[-2]["volume"]:
            score += 20

        self.moves[symbol][timeframe] = {
            "direction": ("bullish" if bullish else "bearish" if bearish else None),
            "score": score,
            "body_percent": body_percent,
            "range": candle_range,
            "expansion": expansion,
            "volume": current["volume"],
            "valid": score >= 70,
        }

        if score >= 70:

            print(f"[DISPLACEMENT] {symbol} {timeframe} {score}")


displacement = Displacement()
