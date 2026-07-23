from collections import defaultdict

from core.market_data.cache import cache
from core.smc.market_structure import market_structure


class LiquiditySweep:

    def __init__(self):

        self.sweeps = defaultdict(lambda: defaultdict(list))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 5:
            return

        self.detect_buy_side(symbol, timeframe)
        self.detect_sell_side(symbol, timeframe)

    # ==========================================================
    # BUY SIDE LIQUIDITY
    # ==========================================================

    def detect_buy_side(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        current = candles[-1]

        structure = market_structure.structure[symbol][timeframe]

        previous_high = structure.get("last_high")

        if previous_high is None:
            return

        # wick breaks high
        if current["high"] <= previous_high:
            return

        # close back below
        if current["close"] >= previous_high:
            return

        sweep = {
            "type": "BUY_SIDE",
            "level": previous_high,
            "time": current["close_time"],
            "wick": current["high"],
            "close": current["close"],
            "valid": True,
        }

        sweeps = self.sweeps[symbol][timeframe]

        if len(sweeps) == 0 or sweeps[-1]["time"] != sweep["time"]:

            sweeps.append(sweep)

            print(f"[LS] {symbol} {timeframe} BUY SIDE")

    # ==========================================================
    # SELL SIDE LIQUIDITY
    # ==========================================================

    def detect_sell_side(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        current = candles[-1]

        structure = market_structure.structure[symbol][timeframe]

        previous_low = structure.get("last_low")

        if previous_low is None:
            return

        # wick breaks low
        if current["low"] >= previous_low:
            return

        # close back above
        if current["close"] <= previous_low:
            return

        sweep = {
            "type": "SELL_SIDE",
            "level": previous_low,
            "time": current["close_time"],
            "wick": current["low"],
            "close": current["close"],
            "valid": True,
        }

        sweeps = self.sweeps[symbol][timeframe]

        if len(sweeps) == 0 or sweeps[-1]["time"] != sweep["time"]:

            sweeps.append(sweep)

            print(f"[LS] {symbol} {timeframe} SELL SIDE")


liquidity_sweep = LiquiditySweep()
