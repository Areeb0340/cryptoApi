from market_data.models import Coin


class StreamBuilder:

    DEFAULT_TIMEFRAMES = [
        "1m",
        "5m",
        "15m",
        "30m",
        "1h",
        "4h",
        "1d",
    ]

    # Ye streams /public route pe hain
    PUBLIC_TYPES = {"depth", "bookTicker"}

    # Ye streams /market route pe hain
    MARKET_TYPES = {"kline", "trade", "aggTrade", "markPrice"}

    def __init__(self, timeframes=None):
        self.timeframes = timeframes or self.DEFAULT_TIMEFRAMES

    def symbols(self):
        return list(
            Coin.objects.filter(is_active=True).values_list("symbol", flat=True)
        )

    def _clean_symbol(self, symbol):
        return symbol.replace("/", "").replace(":USDT", "").lower()

    # ---------------------------------
    # Kline Streams -> MARKET
    # ---------------------------------
    def kline_streams(self):
        streams = []
        for symbol in self.symbols():
            symbol = self._clean_symbol(symbol)
            for tf in self.timeframes:
                streams.append(f"{symbol}@kline_{tf}")
        return streams

    # ---------------------------------
    # Depth Streams -> PUBLIC
    # ---------------------------------
    def depth_streams(self):
        streams = []
        for symbol in self.symbols():
            symbol = self._clean_symbol(symbol)
            streams.append(f"{symbol}@depth20@100ms")
        return streams

    # ---------------------------------
    # Trade Streams -> MARKET
    # ---------------------------------
    def trade_streams(self):
        streams = []
        for symbol in self.symbols():
            symbol = self._clean_symbol(symbol)
            streams.append(f"{symbol}@trade")
        return streams

    # ---------------------------------
    # BookTicker Streams -> PUBLIC
    # ---------------------------------
    def bookticker_streams(self):
        streams = []
        for symbol in self.symbols():
            symbol = self._clean_symbol(symbol)
            streams.append(f"{symbol}@bookTicker")
        return streams

    # ---------------------------------
    # Category-wise grouping
    # ---------------------------------
    def public_streams(self):
        return self.depth_streams() + self.bookticker_streams()

    def market_streams(self):
        return self.kline_streams() + self.trade_streams()

    # ---------------------------------
    # All Streams (for reference/logging only)
    # ---------------------------------
    def all_streams(self):
        return self.public_streams() + self.market_streams()
