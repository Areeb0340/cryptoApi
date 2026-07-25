from core.market_data.cache import cache
from core.ai.indicator_engine import IndicatorEngine
from core.ai.decision_engine import DecisionEngine


class SignalEngine:

    def generate(self, symbol, timeframe):

        symbol = symbol.upper()

        if symbol not in cache.klines:
            return None

        if timeframe not in cache.klines[symbol]:
            return None

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 250:
            return None

        opens = [c["open"] for c in candles]
        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        closes = [c["close"] for c in candles]
        volumes = [c["volume"] for c in candles]

        result = IndicatorEngine.run(
            symbol=symbol,
            opens=opens,
            highs=highs,
            lows=lows,
            closes=closes,
            volumes=volumes,
        )

        if result is None:
            return None

        # Decision Engine yahan, SAHI timeframe ke sath
        decision = DecisionEngine.decide(
            symbol,
            timeframe,
            result["indicators"],
        )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "price": closes[-1],
            "indicator_score": result["final_score"],
            "indicators": result["indicators"],
            "decision": decision,
        }


signal_engine = SignalEngine()
