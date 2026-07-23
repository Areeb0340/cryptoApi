from collections import defaultdict

from core.market_data.cache import cache


class EqualHighLow:

    def __init__(self):

        self.equal_highs = defaultdict(lambda: defaultdict(list))
        self.equal_lows = defaultdict(lambda: defaultdict(list))

        # 0.1% tolerance
        self.tolerance = 0.001

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 15:
            return

        self.detect_equal_highs(symbol, timeframe)
        self.detect_equal_lows(symbol, timeframe)

    # ==========================================================
    # EQUAL HIGHS
    # ==========================================================

    def detect_equal_highs(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        current = candles[-2]

        for previous in candles[:-3]:

            diff = abs(current["high"] - previous["high"])

            if diff / previous["high"] <= self.tolerance:

                level = (current["high"] + previous["high"]) / 2

                eq = {
                    "level": level,
                    "first": previous["open_time"],
                    "second": current["open_time"],
                    "swept": False,
                }

                levels = self.equal_highs[symbol][timeframe]

                if len(levels) == 0 or levels[-1]["second"] != eq["second"]:

                    levels.append(eq)

                    print(f"[EQH] {symbol} {timeframe}")

                return

    # ==========================================================
    # EQUAL LOWS
    # ==========================================================

    def detect_equal_lows(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        current = candles[-2]

        for previous in candles[:-3]:

            diff = abs(current["low"] - previous["low"])

            if diff / previous["low"] <= self.tolerance:

                level = (current["low"] + previous["low"]) / 2

                eq = {
                    "level": level,
                    "first": previous["open_time"],
                    "second": current["open_time"],
                    "swept": False,
                }

                levels = self.equal_lows[symbol][timeframe]

                if len(levels) == 0 or levels[-1]["second"] != eq["second"]:

                    levels.append(eq)

                    print(f"[EQL] {symbol} {timeframe}")

                return


equal_high_low = EqualHighLow()
