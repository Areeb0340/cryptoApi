from collections import defaultdict

from core.market_data.cache import cache


class FairValueGap:

    def __init__(self):
        self.gaps = defaultdict(lambda: defaultdict(list))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 3:
            return

        self.detect_bullish(symbol, timeframe)
        self.detect_bearish(symbol, timeframe)
        self.check_filled(symbol, timeframe)

    # ==========================================================
    # BULLISH FVG
    # ==========================================================

    def detect_bullish(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        c1 = candles[-3]
        c2 = candles[-2]
        c3 = candles[-1]

        if c3["low"] > c1["high"]:

            gap = {
                "type": "bullish",
                "top": c3["low"],
                "bottom": c1["high"],
                "created": c3["close_time"],
                "filled": False,
                "partial": False,
                "broken": False,
            }

            gaps = self.gaps[symbol][timeframe]

            if len(gaps) == 0 or gaps[-1]["created"] != gap["created"]:
                gaps.append(gap)
                print(f"[FVG] {symbol} {timeframe} BULLISH")

    # ==========================================================
    # BEARISH FVG
    # ==========================================================

    def detect_bearish(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        c1 = candles[-3]
        c2 = candles[-2]
        c3 = candles[-1]

        if c3["high"] < c1["low"]:

            gap = {
                "type": "bearish",
                "top": c1["low"],
                "bottom": c3["high"],
                "created": c3["close_time"],
                "filled": False,
                "partial": False,
                "broken": False,
            }

            gaps = self.gaps[symbol][timeframe]

            if len(gaps) == 0 or gaps[-1]["created"] != gap["created"]:
                gaps.append(gap)
                print(f"[FVG] {symbol} {timeframe} BEARISH")

    # ==========================================================
    # CHECK FILLED
    # ==========================================================

    def check_filled(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if not candles:
            return

        current = candles[-1]

        for gap in self.gaps[symbol][timeframe]:

            if gap["filled"]:
                continue

            if gap["type"] == "bullish":

                if current["low"] <= gap["top"]:
                    gap["partial"] = True

                if current["low"] <= gap["bottom"]:
                    gap["filled"] = True

            else:

                if current["high"] >= gap["bottom"]:
                    gap["partial"] = True

                if current["high"] >= gap["top"]:
                    gap["filled"] = True


fair_value_gap = FairValueGap()
