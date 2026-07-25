from collections import defaultdict

from core.market_data.cache import cache
from core.smc.market_structure import market_structure


class PremiumDiscount:

    def __init__(self):

        self.zones = defaultdict(lambda: defaultdict(dict))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        structure = market_structure.structure[symbol][timeframe]

        if not structure:
            return

        high = structure.get("last_high")
        low = structure.get("last_low")

        if high is None or low is None:
            return

        candles = cache.klines[symbol][timeframe]

        if not candles:
            return

        current = candles[-1]["close"]

        equilibrium = (high + low) / 2

        if current > equilibrium:

            zone = "PREMIUM"

        elif current < equilibrium:

            zone = "DISCOUNT"

        else:

            zone = "EQUILIBRIUM"

        self.zones[symbol][timeframe] = {
            "high": high,
            "low": low,
            "equilibrium": equilibrium,
            "price": current,
            "zone": zone,
        }

        print(f"[PD] {symbol} {timeframe} {zone}")


premium_discount = PremiumDiscount()
