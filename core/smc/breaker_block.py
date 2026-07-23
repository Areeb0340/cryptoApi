from collections import defaultdict

from core.smc.order_block import order_block


class BreakerBlock:

    def __init__(self):

        self.blocks = defaultdict(lambda: defaultdict(list))

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def update(self, symbol, timeframe):

        blocks = order_block.blocks[symbol][timeframe]

        if not blocks:
            return

        for block in blocks:

            if not block["broken"]:
                continue

            if block.get("breaker"):
                continue

            breaker = {
                "type": ("bearish" if block["type"] == "bullish" else "bullish"),
                "high": block["high"],
                "low": block["low"],
                "created": block["time"],
                "mitigated": False,
                "touches": 0,
            }

            self.blocks[symbol][timeframe].append(breaker)

            block["breaker"] = True

            print(f"[BREAKER] {symbol} {timeframe} " f"{breaker['type'].upper()}")


breaker_block = BreakerBlock()
