from indicators.ema import analyze_ema
from indicators.rsi import analyze_rsi
from indicators.macd import analyze_macd
from indicators.adx import analyze_adx
from indicators.atr import analyze_atr
from indicators.bollinger import analyze_bollinger
from indicators.ichimoku import analyze_ichimoku
from indicators.obv import analyze_obv
from indicators.supertrend import analyze_supertrend
from indicators.volume import analyze_volume
from indicators.vwap import analyze_vwap


class IndicatorEngine:

    @staticmethod
    def normalize(score):

        if score is None:
            return 50

        return max(0, min(100, float(score)))

    @staticmethod
    def average(scores):

        if len(scores) == 0:
            return 0

        return round(sum(scores) / len(scores), 2)

    @staticmethod
    def get_score(data):

        if isinstance(data, dict):

            if "ai_score" in data:
                return data["ai_score"]

            if "score" in data:
                return data["score"]

            if "trend_score" in data:
                return data["trend_score"]

        return 50

    @staticmethod
    def run(
        symbol,
        opens,
        highs,
        lows,
        closes,
        volumes,
    ):

        indicators = {}
        scores = []

        # ==========================
        # EMA
        # ==========================

        ema = analyze_ema(closes)

        indicators["ema"] = ema

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(ema)))

        # ==========================
        # RSI
        # ==========================

        rsi = analyze_rsi(closes)

        indicators["rsi"] = rsi

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(rsi)))

        # ==========================
        # MACD
        # ==========================

        macd = analyze_macd(closes)

        indicators["macd"] = macd

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(macd)))

        # ==========================
        # ADX
        # ==========================

        adx = analyze_adx(
            highs,
            lows,
            closes,
        )

        indicators["adx"] = adx

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(adx)))

        # ==========================
        # ATR
        # ==========================

        atr = analyze_atr(
            highs,
            lows,
            closes,
        )

        indicators["atr"] = atr

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(atr)))

        # ==========================
        # Bollinger
        # ==========================

        bollinger = analyze_bollinger(closes)

        indicators["bollinger"] = bollinger

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(bollinger)))

        # ==========================
        # Ichimoku
        # ==========================

        ichimoku = analyze_ichimoku(
            highs,
            lows,
            closes,
        )

        indicators["ichimoku"] = ichimoku

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(ichimoku)))

        # ==========================
        # OBV
        # ==========================

        obv = analyze_obv(
            closes,
            volumes,
        )

        indicators["obv"] = obv

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(obv)))

        # ==========================
        # Volume
        # ==========================

        volume = analyze_volume(
            closes,
            volumes,
        )

        indicators["volume"] = volume

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(volume)))

        # ==========================
        # SuperTrend
        # ==========================

        supertrend = analyze_supertrend(
            highs,
            lows,
            closes,
        )

        indicators["supertrend"] = supertrend

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(supertrend)))

        # ==========================
        # VWAP
        # ==========================

        vwap = analyze_vwap(
            highs,
            lows,
            closes,
            volumes,
        )

        indicators["vwap"] = vwap

        scores.append(IndicatorEngine.normalize(IndicatorEngine.get_score(vwap)))

        # ==========================
        # FINAL SCORE
        # ==========================

        final_score = IndicatorEngine.average(scores)

        # ==========================
        # AI DECISION
        # ==========================

        return {
            "symbol": symbol,
            "final_score": final_score,
            "scores": scores,
            "indicators": indicators,
        }
