from collections import defaultdict

from core.market_data.cache import cache


class CHOCH:

    def __init__(self):

        self.state = defaultdict(
            lambda: defaultdict(
                lambda: {
                    "confirmed": False,
                    "direction": None,
                    "price": None,
                    "time": None,
                }
            )
        )

    def update(self, symbol, timeframe):

        structure = cache.market_structure.get(symbol, {}).get(timeframe)

        if not structure:
            return

        swings = structure["structure"]

        if len(swings) < 4:
            return

        last = swings[-1]
        prev = swings[-2]

        state = self.state[symbol][timeframe]

        # Bullish CHOCH
        if prev["label"] == "LL" and last["label"] == "HH":

            state["confirmed"] = True
            state["direction"] = "BULLISH"
            state["price"] = last["price"]
            state["time"] = last["time"]

            print(f"[CHOCH] {symbol} {timeframe} BULLISH")

        # Bearish CHOCH
        elif prev["label"] == "HH" and last["label"] == "LL":

            state["confirmed"] = True
            state["direction"] = "BEARISH"
            state["price"] = last["price"]
            state["time"] = last["time"]

            print(f"[CHOCH] {symbol} {timeframe} BEARISH")


choch = CHOCH()
