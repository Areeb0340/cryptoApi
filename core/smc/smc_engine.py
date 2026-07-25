from core.smc.market_structure import market_structure
from core.smc.bos import bos
from core.smc.choch import choch
from core.smc.equal_high_low import equal_high_low
from core.smc.liquidity_sweep import liquidity_sweep
from core.smc.order_block import order_block
from core.smc.fair_value_gap import fair_value_gap
from core.smc.displacement import displacement
from core.smc.mitigation import mitigation
from core.smc.premium_discount import premium_discount
from core.smc.inducement import inducement
from core.smc.breaker_block import breaker_block
from core.smc.rejection_block import rejection_block
from core.smc.confluence_engine import confluence_engine


class SMCEngine:

    def update(self, symbol, timeframe):

        # ======================================================
        # MARKET STRUCTURE
        # ======================================================

        market_structure.update(symbol, timeframe)

        # ======================================================
        # BOS / CHOCH
        # ======================================================

        bos.update(symbol, timeframe)
        choch.update(symbol, timeframe)

        # ======================================================
        # LIQUIDITY
        # ======================================================

        equal_high_low.update(symbol, timeframe)
        liquidity_sweep.update(symbol, timeframe)

        # ======================================================
        # ORDER BLOCK
        # ======================================================

        order_block.update(symbol, timeframe)
        order_block.check_blocks(symbol, timeframe)

        # ======================================================
        # FVG
        # ======================================================

        fair_value_gap.update(symbol, timeframe)

        # ======================================================
        # DISPLACEMENT
        # ======================================================

        displacement.update(symbol, timeframe)

        # ======================================================
        # MITIGATION
        # ======================================================

        mitigation.update(
            symbol,
            timeframe,
            order_block.blocks[symbol][timeframe],
        )

        # ======================================================
        # PREMIUM / DISCOUNT
        # ======================================================

        premium_discount.update(symbol, timeframe)

        # ======================================================
        # INDUCEMENT
        # ======================================================

        inducement.update(symbol, timeframe)

        # ======================================================
        # BREAKER
        # ======================================================

        breaker_block.update(symbol, timeframe)

        # ======================================================
        # REJECTION
        # ======================================================

        rejection_block.update(symbol, timeframe)

        # ======================================================
        # CONFLUENCE
        # ======================================================

        confluence_engine.update(symbol, timeframe)


smc_engine = SMCEngine()
