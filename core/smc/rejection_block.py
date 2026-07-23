from collections import defaultdict

from core.market_data.cache import cache


class RejectionBlock:

    def __init__(self):

        self.blocks = defaultdict(lambda: defaultdict(dict))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 3:
            return

        candle = candles[-1]

        body = abs(candle["close"] - candle["open"])

        upper_wick = candle["high"] - max(candle["open"], candle["close"])

        lower_wick = min(candle["open"], candle["close"]) - candle["low"]

        candle_range = candle["high"] - candle["low"]

        if candle_range == 0:
            return

        upper_ratio = upper_wick / candle_range
        lower_ratio = lower_wick / candle_range

        state = self.blocks[symbol][timeframe]

        # Bearish rejection

        if upper_ratio >= 0.60:

            state.update(
                {
                    "type": "bearish",
                    "strength": round(upper_ratio * 100, 2),
                    "time": candle["close_time"],
                    "price": candle["high"],
                }
            )

            print(f"[REJECTION] " f"{symbol} " f"{timeframe} " f"BEARISH")

        # Bullish rejection

        elif lower_ratio >= 0.60:

            state.update(
                {
                    "type": "bullish",
                    "strength": round(lower_ratio * 100, 2),
                    "time": candle["close_time"],
                    "price": candle["low"],
                }
            )

            print(f"[REJECTION] " f"{symbol} " f"{timeframe} " f"BULLISH")


rejection_block = RejectionBlock()
