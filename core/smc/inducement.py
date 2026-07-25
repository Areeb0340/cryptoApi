from collections import defaultdict

from core.market_data.cache import cache
from core.smc.market_structure import market_structure


class Inducement:

    def __init__(self):

        self.state = defaultdict(lambda: defaultdict(dict))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 10:
            return

        structure = market_structure.structure[symbol][timeframe]

        if not structure:
            return

        current = candles[-1]

        high = structure.get("last_high")
        low = structure.get("last_low")

        if high is None or low is None:
            return

        trend = structure.get("trend")

        state = self.state[symbol][timeframe]

        # Bullish inducement

        if trend == "UPTREND":

            if current["low"] < low and current["close"] > low:

                state.update(
                    {
                        "type": "bullish",
                        "level": low,
                        "price": current["close"],
                        "time": current["close_time"],
                        "valid": True,
                    }
                )

                print(f"[INDUCEMENT] {symbol} {timeframe} BULLISH")

        # Bearish inducement

        elif trend == "DOWNTREND":

            if current["high"] > high and current["close"] < high:

                state.update(
                    {
                        "type": "bearish",
                        "level": high,
                        "price": current["close"],
                        "time": current["close_time"],
                        "valid": True,
                    }
                )

                print(f"[INDUCEMENT] {symbol} {timeframe} BEARISH")


inducement = Inducement()
