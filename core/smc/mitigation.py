from collections import defaultdict

from core.market_data.cache import cache


class Mitigation:

    def __init__(self):

        self.state = defaultdict(lambda: defaultdict(list))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe, blocks):

        candles = cache.klines[symbol][timeframe]

        if not candles:
            return

        current = candles[-1]

        if not blocks:
            return

        for block in blocks:

            if block["broken"]:
                continue

            if block["type"] == "bullish":
                self.check_bullish(block, current)
            else:
                self.check_bearish(block, current)

    # ==========================================================
    # BULLISH
    # ==========================================================

    def check_bullish(self, block, candle):

        if candle["low"] <= block["high"] and candle["high"] >= block["low"]:

            block["touches"] += 1
            block["mitigated"] = True

        if candle["close"] < block["low"]:
            block["broken"] = True

    # ==========================================================
    # BEARISH
    # ==========================================================

    def check_bearish(self, block, candle):

        if candle["high"] >= block["low"] and candle["low"] <= block["high"]:

            block["touches"] += 1
            block["mitigated"] = True

        if candle["close"] > block["high"]:
            block["broken"] = True


mitigation = Mitigation()
