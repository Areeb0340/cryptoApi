from collections import defaultdict, deque
from threading import Lock


class MarketCache:

    def __init__(self):

        self.lock = Lock()

        self.prices = {}
        self.trades = defaultdict(lambda: deque(maxlen=5000))
        self.orderbooks = {}
        self.book_tickers = {}
        self.klines = defaultdict(lambda: defaultdict(lambda: deque(maxlen=600)))
        self.open_interest = {}
        self.funding_rates = {}
        self.liquidations = defaultdict(lambda: deque(maxlen=1000))

        self.delta_volume = defaultdict(lambda: {"buy": 0.0, "sell": 0.0})
        self.cvd = defaultdict(float)

        self.stats = defaultdict(
            lambda: {
                "last_trade": None,
                "last_depth": None,
                "last_kline": None,
            }
        )

    # ==========================================================
    # TRADE
    # ==========================================================

    def update_trade(self, symbol, trade):

        with self.lock:

            self.prices[symbol] = trade["price"]
            self.trades[symbol].append(trade)

            if trade["buyer_is_maker"]:
                # Seller Aggressor
                self.delta_volume[symbol]["sell"] += trade["qty"]
                self.cvd[symbol] -= trade["qty"]
            else:
                # Buyer Aggressor
                self.delta_volume[symbol]["buy"] += trade["qty"]
                self.cvd[symbol] += trade["qty"]

            self.stats[symbol]["last_trade"] = trade["trade_time"]

    # ==========================================================
    # ORDERBOOK
    # ==========================================================

    def update_orderbook(self, symbol, orderbook):

        with self.lock:

            self.orderbooks[symbol] = orderbook
            self.stats[symbol]["last_depth"] = orderbook["event_time"]

    # ==========================================================
    # CANDLE
    # ==========================================================

    def update_candle(self, symbol, timeframe, candle):

        with self.lock:

            candles = self.klines[symbol][timeframe]

            if len(candles) > 0 and candles[-1]["open_time"] == candle["open_time"]:
                # Update current (still forming) candle
                candles[-1] = candle
            else:
                # New candle started
                candles.append(candle)

            self.stats[symbol]["last_kline"] = candle["close_time"]

            return candle["closed"]

    # ==========================================================
    # BOOK TICKER
    # ==========================================================

    def update_book_ticker(self, symbol, ticker):

        with self.lock:
            self.book_tickers[symbol] = ticker


cache = MarketCache()
