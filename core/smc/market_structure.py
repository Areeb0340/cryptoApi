from core.market_data.cache import cache


class MarketStructure:

    def __init__(self):

        self.left = 3
        self.right = 3

    # ==========================================================
    # MAIN UPDATE
    # ==========================================================

    def update(self, symbol, timeframe):

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 20:
            return

        swings = self.detect_swings(candles)

        if len(swings) < 2:
            return

        structure = self.classify(swings)

        trend = self.detect_trend(structure)

        if not hasattr(cache, "market_structure"):
            cache.market_structure = {}

        cache.market_structure.setdefault(symbol, {})
        cache.market_structure[symbol][timeframe] = {
            "swings": swings,
            "structure": structure,
            "trend": trend,
        }

    # ==========================================================
    # SWING DETECTION
    # ==========================================================

    def detect_swings(self, candles):

        swings = []

        total = len(candles)

        for i in range(self.left, total - self.right):

            current = candles[i]

            high = current["high"]
            low = current["low"]

            swing_high = True
            swing_low = True

            # Left
            for j in range(i - self.left, i):

                if candles[j]["high"] >= high:
                    swing_high = False

                if candles[j]["low"] <= low:
                    swing_low = False

            # Right
            for j in range(i + 1, i + self.right + 1):

                if candles[j]["high"] > high:
                    swing_high = False

                if candles[j]["low"] < low:
                    swing_low = False

            if swing_high:

                swings.append(
                    {
                        "type": "HIGH",
                        "price": high,
                        "index": i,
                        "time": current["close_time"],
                    }
                )

            elif swing_low:

                swings.append(
                    {
                        "type": "LOW",
                        "price": low,
                        "index": i,
                        "time": current["close_time"],
                    }
                )

        return swings

    # ==========================================================
    # HH HL LH LL
    # ==========================================================

    def classify(self, swings):

        result = []

        previous_high = None
        previous_low = None

        for swing in swings:

            item = swing.copy()

            if swing["type"] == "HIGH":

                if previous_high is None:

                    item["label"] = "H"

                elif swing["price"] > previous_high:

                    item["label"] = "HH"

                else:

                    item["label"] = "LH"

                previous_high = swing["price"]

            else:

                if previous_low is None:

                    item["label"] = "L"

                elif swing["price"] > previous_low:

                    item["label"] = "HL"

                else:

                    item["label"] = "LL"

                previous_low = swing["price"]

            result.append(item)

        return result

    # ==========================================================
    # TREND
    # ==========================================================

    def detect_trend(self, structure):

        if len(structure) < 4:
            return "UNKNOWN"

        labels = [x["label"] for x in structure[-6:]]

        bullish = 0
        bearish = 0

        for label in labels:

            if label in ("HH", "HL"):
                bullish += 1

            elif label in ("LH", "LL"):
                bearish += 1

        if bullish > bearish:
            return "BULLISH"

        if bearish > bullish:
            return "BEARISH"

        return "RANGE"


market_structure = MarketStructure()
