from core.market_data.cache import cache
from core.smc.smc_engine import smc_engine
from core.ai.indicator_engine import IndicatorEngine
from core.ai.decision_engine import DecisionEngine


class KlineHandler:
    print("KLINE HANDLER CALLED")

    async def __call__(self, data):

        k = data["k"]

        symbol = data["s"]
        timeframe = k["i"]

        candle = {
            "open_time": k["t"],
            "close_time": k["T"],
            "symbol": symbol,
            "timeframe": timeframe,
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"]),
            "closed": k["x"],
        }

        is_closed = cache.update_candle(symbol, timeframe, candle)
        print(len(cache.klines[symbol][timeframe]))

        if not is_closed:
            return

        # ===============================
        # Candle CLOSED -> Run full pipeline
        # ===============================

        # 1. SMC Engine (BOS, CHOCH, OB, FVG... + confluence score andar hi calculate hota hai)
        smc_engine.update(symbol, timeframe)
        print("SMC DONE")

        # 2. Prepare OHLCV arrays for indicators
        candles = list(cache.klines[symbol][timeframe])

        if len(candles) < 50:
            # Indicators ko meaningful result ke liye minimum candles chahiye
            print(
                f"[{symbol}][{timeframe}] Waiting for more candles... ({len(candles)}/50)"
            )
            return

        opens = [c["open"] for c in candles]
        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        closes = [c["close"] for c in candles]
        volumes = [c["volume"] for c in candles]

        # 3. Indicator Engine
        indicator_result = IndicatorEngine.run(
            symbol, opens, highs, lows, closes, volumes
        )
        print("RUNNING INDICATORS")

        # 4. Decision Engine
        decision = DecisionEngine.decide(
            symbol,
            timeframe,
            indicator_result["indicators"],
            oi_data=None,  # baad me real OI data yahan pass karna
            funding_data=None,  # baad me real funding data yahan pass karna
        )
        print(decision)
        # 5. PRINT SIGNAL
        print(
            f"[SIGNAL] {symbol} {timeframe} -> "
            f"{decision['signal']} "
            f"(confidence: {decision['confidence']}%) "
            f"| Bullish: {decision['bullish_points']} "
            f"| Bearish: {decision['bearish_points']} "
            f"| SMC: {decision['smc_score']}"
        )
