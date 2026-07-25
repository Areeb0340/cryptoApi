from market_data.models import Coin
from market_data.models import Candle

from core.ai.indicator_engine import IndicatorEngine

TIMEFRAMES = [
    "1h",
    "4h",
    "1d",
]

MIN_CANDLES = 250


class CoinSelector:

    def __init__(self):

        self.results = []

    def load_data(
        self,
        coin,
        timeframe,
    ):

        candles = Candle.objects.filter(
            coin=coin,
            timeframe=timeframe,
        ).order_by("timestamp")

        if candles.count() < MIN_CANDLES:
            return None

        highs = []
        lows = []
        closes = []
        volumes = []
        opens = []

        for candle in candles:

            highs.append(float(candle.high))
            lows.append(float(candle.low))
            closes.append(float(candle.close))
            volumes.append(float(candle.volume))
            opens.append(float(candle.open))

        return {
            "opens": opens,
            "highs": highs,
            "lows": lows,
            "closes": closes,
            "volumes": volumes,
        }

    def scan_coin(
        self,
        coin,
    ):

        timeframe_scores = {}

        for timeframe in TIMEFRAMES:

            data = self.load_data(
                coin,
                timeframe,
            )

            if data is None:
                continue

            analysis = IndicatorEngine.run(
                coin.symbol,
                data["opens"],
                data["highs"],
                data["lows"],
                data["closes"],
                data["volumes"],
            )

            timeframe_scores[timeframe] = analysis

        if len(timeframe_scores) == 0:
            return None

        scores = []

        for tf in timeframe_scores:

            scores.append(timeframe_scores[tf]["final_score"])

        final_score = round(
            sum(scores) / len(scores),
            2,
        )

        if final_score >= 75:

            signal = "LONG"

        elif final_score <= 25:

            signal = "SHORT"

        else:

            signal = "WAIT"

        return {
            "symbol": coin.symbol,
            "coin": coin,
            "signal": signal,
            "score": final_score,
            "timeframes": timeframe_scores,
        }

    def scan_all(self):

        coins = Coin.objects.filter(
            is_active=True,
        )

        results = []

        for coin in coins:

            result = self.scan_coin(
                coin,
            )

            if result:
                results.append(result)

        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        self.results = results

        return results

    def get_top_longs(
        self,
        limit=20,
    ):

        longs = [x for x in self.results if x["signal"] == "LONG"]

        return longs[:limit]

    def get_top_shorts(
        self,
        limit=20,
    ):

        shorts = [x for x in self.results if x["signal"] == "SHORT"]

        return shorts[:limit]
