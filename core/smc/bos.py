from collections import defaultdict

from core.market_data.cache import cache
from core.smc.market_structure import market_structure


class BOS:

    def __init__(self):

        self.state = defaultdict(
            lambda: defaultdict(
                lambda: {
                    "direction": None,
                    "price": None,
                    "time": None,
                    "strength": 0,
                    "broken_swing": None,
                    "confirmed": False,
                }
            )
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 20:
            return

        structure = market_structure.structure[symbol][timeframe]

        if not structure:
            return

        trend = structure.get("trend")

        if trend == "UPTREND":
            self.detect_bullish_bos(symbol, timeframe)

        elif trend == "DOWNTREND":
            self.detect_bearish_bos(symbol, timeframe)

    # ==========================================================
    # BULLISH BOS
    # ==========================================================

    def detect_bullish_bos(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        structure = market_structure.structure[symbol][timeframe]

        last_high = structure.get("last_high")

        if last_high is None:
            return

        current = candles[-1]

        close = current["close"]

        # candle close above previous swing high

        if close <= last_high:
            return

        # avoid duplicate BOS

        state = self.state[symbol][timeframe]

        if state["direction"] == "BULLISH" and state["price"] == last_high:
            return

        state["direction"] = "BULLISH"

        state["price"] = last_high

        state["time"] = current["close_time"]

        state["broken_swing"] = last_high

        state["confirmed"] = True

        state["strength"] = 0

        print(f"[BOS] {symbol} {timeframe} " f"BULLISH -> {last_high}")

    # ==========================================================
    # BEARISH BOS
    # ==========================================================

    def detect_bearish_bos(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        structure = market_structure.structure[symbol][timeframe]

        last_low = structure.get("last_low")

        if last_low is None:
            return

        current = candles[-1]

        close = current["close"]

        if close >= last_low:
            return

        state = self.state[symbol][timeframe]

        if state["direction"] == "BEARISH" and state["price"] == last_low:
            return

        state["direction"] = "BEARISH"

        state["price"] = last_low

        state["time"] = current["close_time"]

        state["broken_swing"] = last_low

        state["confirmed"] = True

        state["strength"] = 0

        print(f"[BOS] {symbol} {timeframe} " f"BEARISH -> {last_low}")


bos = BOS()
