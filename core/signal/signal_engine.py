from core.market_data.cache import cache
from core.ai.indicator_engine import IndicatorEngine


class SignalEngine:

    def generate(self, symbol, timeframe):

        symbol = symbol.upper()

        # ----------------------------
        # Candle Check
        # ----------------------------

        if symbol not in cache.klines:
            return None

        if timeframe not in cache.klines[symbol]:
            return None

        candles = cache.klines[symbol][timeframe]

        if len(candles) < 250:
            return None

        # ----------------------------
        # OHLCV Arrays
        # ----------------------------

        opens = [c["open"] for c in candles]
        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        closes = [c["close"] for c in candles]
        volumes = [c["volume"] for c in candles]

        # ----------------------------
        # Indicator Engine
        # ----------------------------

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

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "price": closes[-1],
            "indicator_score": result["final_score"],
            "indicators": result["indicators"],
            "decision": result["decision"],
        }


signal_engine = SignalEngine()
