from collections import defaultdict

from core.market_data.cache import cache
from core.smc.fair_value_gap import fair_value_gap


class OrderBlock:

    def __init__(self):
        self.blocks = defaultdict(lambda: defaultdict(list))

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, symbol, timeframe):

        # Lazy import (Circular Import Fix)
        from core.smc.bos import bos

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 8:
            return

        bos_state = bos.state[symbol][timeframe]

        if not bos_state.get("confirmed"):
            return

        direction = bos_state.get("direction")

        if direction == "BULLISH":
            self.detect_bullish(symbol, timeframe)

        elif direction == "BEARISH":
            self.detect_bearish(symbol, timeframe)

        # FVG update
        fair_value_gap.update(symbol, timeframe)

    # ==================================================
    # BULLISH ORDER BLOCK
    # ==================================================

    def detect_bullish(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        for candle in reversed(candles[:-1]):

            if candle["close"] < candle["open"]:

                block = {
                    "type": "bullish",
                    "high": candle["high"],
                    "low": candle["low"],
                    "open": candle["open"],
                    "close": candle["close"],
                    "time": candle["open_time"],
                    "mitigated": False,
                    "broken": False,
                    "touches": 0,
                    "strength": 0,
                }

                self.blocks[symbol][timeframe].append(block)

                print(f"[OB] {symbol} {timeframe} BULLISH")

                break

    # ==================================================
    # BEARISH ORDER BLOCK
    # ==================================================

    def detect_bearish(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        for candle in reversed(candles[:-1]):

            if candle["close"] > candle["open"]:

                block = {
                    "type": "bearish",
                    "high": candle["high"],
                    "low": candle["low"],
                    "open": candle["open"],
                    "close": candle["close"],
                    "time": candle["open_time"],
                    "mitigated": False,
                    "broken": False,
                    "touches": 0,
                    "strength": 0,
                }

                self.blocks[symbol][timeframe].append(block)

                print(f"[OB] {symbol} {timeframe} BEARISH")

                break

    # ==================================================
    # CHECK MITIGATION / BREAK
    # ==================================================

    def check_blocks(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if not candles:
            return

        current = candles[-1]

        for block in self.blocks[symbol][timeframe]:

            if block["broken"]:
                continue

            if block["type"] == "bullish":

                if current["low"] <= block["high"] and current["high"] >= block["low"]:
                    block["touches"] += 1
                    block["mitigated"] = True

                if current["close"] < block["low"]:
                    block["broken"] = True

            else:

                if current["high"] >= block["low"] and current["low"] <= block["high"]:
                    block["touches"] += 1
                    block["mitigated"] = True

                if current["close"] > block["high"]:
                    block["broken"] = True


order_block = OrderBlock()
