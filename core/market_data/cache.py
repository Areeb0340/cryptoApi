from collections import defaultdict, deque
from threading import Lock


class MarketCache:

    def __init__(self):

        self.lock = Lock()

        # Latest Trade Price
        self.prices = {}

        # Recent Trades
        self.trades = defaultdict(lambda: deque(maxlen=5000))

        # Latest Orderbook
        self.orderbooks = {}

        # Latest BookTicker
        self.book_tickers = {}

        # Latest Klines
        self.klines = defaultdict(lambda: defaultdict(lambda: deque(maxlen=600)))

        # Open Interest
        self.open_interest = {}

        # Funding Rate
        self.funding_rates = {}

        # Liquidations
        self.liquidations = defaultdict(lambda: deque(maxlen=1000))

        # Aggressive Buy/Sell Volume
        self.delta_volume = defaultdict(
            lambda: {
                "buy": 0.0,
                "sell": 0.0,
            }
        )

        # Cumulative Volume Delta
        self.cvd = defaultdict(float)

        # Symbol Statistics
        self.stats = defaultdict(
            lambda: {
                "last_trade": None,
                "last_depth": None,
                "last_kline": None,
            }
        )


cache = MarketCache()
