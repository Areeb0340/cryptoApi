from core.smc.confluence_engine import confluence_engine


class DecisionEngine:

    @staticmethod
    def decide(symbol, timeframe, indicators):

        reasons = []

        bullish = 0
        bearish = 0

        # =====================================================
        # EMA
        # =====================================================

        ema = indicators.get("ema", {})

        if ema.get("trend") == "BULLISH":
            bullish += 1
            reasons.append("EMA Bullish")

        elif ema.get("trend") == "BEARISH":
            bearish += 1
            reasons.append("EMA Bearish")

        # =====================================================
        # RSI
        # =====================================================

        rsi = indicators.get("rsi", {})

        if rsi.get("signal") == "BUY":
            bullish += 1
            reasons.append("RSI Buy")

        elif rsi.get("signal") == "SELL":
            bearish += 1
            reasons.append("RSI Sell")

        # =====================================================
        # MACD
        # =====================================================

        macd = indicators.get("macd", {})

        if macd.get("trend") == "BULLISH":
            bullish += 1
            reasons.append("MACD Bullish")

        elif macd.get("trend") == "BEARISH":
            bearish += 1
            reasons.append("MACD Bearish")

        # =====================================================
        # ADX
        # =====================================================

        adx = indicators.get("adx", {})

        if adx.get("trend") == "STRONG_BULLISH":
            bullish += 1
            reasons.append("ADX Strong Bullish")

        elif adx.get("trend") == "STRONG_BEARISH":
            bearish += 1
            reasons.append("ADX Strong Bearish")

        # =====================================================
        # SUPERTREND
        # =====================================================

        supertrend = indicators.get("supertrend", {})

        if supertrend.get("trend") == "BULLISH":
            bullish += 1
            reasons.append("Supertrend Bullish")

        elif supertrend.get("trend") == "BEARISH":
            bearish += 1
            reasons.append("Supertrend Bearish")

        # =====================================================
        # VOLUME
        # =====================================================

        volume = indicators.get("volume", {})

        if volume.get("signal") == "BUY":
            bullish += 1
            reasons.append("Volume Buy")

        elif volume.get("signal") == "SELL":
            bearish += 1
            reasons.append("Volume Sell")

        # =====================================================
        # VWAP
        # =====================================================

        vwap = indicators.get("vwap", {})

        if vwap.get("trend") == "BULLISH":
            bullish += 1
            reasons.append("VWAP Bullish")

        elif vwap.get("trend") == "BEARISH":
            bearish += 1
            reasons.append("VWAP Bearish")

        # =====================================================
        # SMC CONFLUENCE
        # =====================================================

        smc = confluence_engine.score[symbol][timeframe]

        smc_score = smc.get("score", 0)

        smc_reasons = smc.get("reasons", [])

        if smc_score >= 80:

            bullish += 4
            reasons.append(f"Strong Bullish SMC ({smc_score})")

        elif smc_score >= 60:

            bullish += 2
            reasons.append(f"Bullish SMC ({smc_score})")

        elif smc_score >= 40:

            reasons.append(f"Neutral SMC ({smc_score})")

        elif smc_score >= 20:

            bearish += 2
            reasons.append(f"Bearish SMC ({smc_score})")

        else:

            bearish += 4
            reasons.append(f"Strong Bearish SMC ({smc_score})")

        reasons.extend(smc_reasons)

        # =====================================================
        # FINAL SIGNAL
        # =====================================================

        total = bullish + bearish

        if total == 0:

            confidence = 0

        else:

            confidence = round(
                max(bullish, bearish) / total * 100,
                2,
            )

        if bullish >= bearish + 3:

            signal = "LONG"

        elif bearish >= bullish + 3:

            signal = "SHORT"

        else:

            signal = "NO TRADE"

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "signal": signal,
            "confidence": confidence,
            "bullish_points": bullish,
            "bearish_points": bearish,
            "smc_score": smc_score,
            "reasons": reasons,
        }
