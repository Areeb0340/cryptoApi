from collections import defaultdict

from core.smc.market_structure import market_structure
from core.smc.bos import bos
from core.smc.choch import choch
from core.smc.order_block import order_block

from core.smc.liquidity_sweep import liquidity_sweep
from core.smc.equal_high_low import equal_high_low
from core.smc.displacement import displacement
from core.smc.mitigation import mitigation
from core.smc.premium_discount import premium_discount
from core.smc.inducement import inducement
from core.smc.breaker_block import breaker_block
from core.smc.rejection_block import rejection_block


class ConfluenceEngine:

    def __init__(self):

        self.score = defaultdict(lambda: defaultdict(dict))

    # =====================================================
    # PUBLIC
    # =====================================================

    def update(self, symbol, timeframe):

        score = 0
        reasons = []

        # ==========================================
        # BOS
        # ==========================================

        bos_state = bos.state[symbol][timeframe]

        if bos_state.get("confirmed"):

            score += 10
            reasons.append("BOS")

        # ==========================================
        # CHOCH
        # ==========================================

        choch_state = choch.state[symbol][timeframe]

        if choch_state.get("confirmed"):

            score += 15
            reasons.append("CHOCH")

        # ==========================================
        # ORDER BLOCK
        # ==========================================

        if order_block.blocks[symbol][timeframe]:

            score += 15
            reasons.append("ORDER_BLOCK")

            # ==========================================
            # FVG
            # ==========================================

            score += 10
            reasons.append("FVG")

        # ==========================================
        # LIQUIDITY
        # ==========================================

        if liquidity_sweep.state[symbol][timeframe]:

            score += 10
            reasons.append("LIQUIDITY")

        # ==========================================
        # EQH / EQL
        # ==========================================

        if equal_high_low.equal_highs[symbol][timeframe]:

            score += 5
            reasons.append("EQH")

        if equal_high_low.equal_lows[symbol][timeframe]:

            score += 5
            reasons.append("EQL")

        # ==========================================
        # DISPLACEMENT
        # ==========================================

        disp = displacement.moves[symbol][timeframe]

        if disp.get("valid"):

            score += 10
            reasons.append("DISPLACEMENT")

        # ==========================================
        # MITIGATION
        # ==========================================

        score += 5
        reasons.append("MITIGATION")

        # ==========================================
        # PREMIUM / DISCOUNT
        # ==========================================

        pd = premium_discount.zones[symbol][timeframe]

        if pd.get("zone") == "DISCOUNT":

            score += 5
            reasons.append("DISCOUNT")

        if pd.get("zone") == "PREMIUM":

            score += 5
            reasons.append("PREMIUM")

        # ==========================================
        # INDUCEMENT
        # ==========================================

        if inducement.state[symbol][timeframe]:

            score += 5
            reasons.append("INDUCEMENT")

        # ==========================================
        # BREAKER
        # ==========================================

        if breaker_block.blocks[symbol][timeframe]:

            score += 5
            reasons.append("BREAKER")

        # ==========================================
        # REJECTION
        # ==========================================

        if rejection_block.blocks[symbol][timeframe]:

            score += 5
            reasons.append("REJECTION")

        self.score[symbol][timeframe] = {
            "score": score,
            "reasons": reasons,
        }

        print(f"[CONFLUENCE] " f"{symbol} " f"{timeframe} " f"{score}/100")


confluence_engine = ConfluenceEngine()
