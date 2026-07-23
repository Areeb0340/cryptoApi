from statistics import mean


class OrderBookAnalyzer:

    def __init__(self, book):

        self.book = book

        self.bids = book["bids"]
        self.asks = book["asks"]

        if not self.bids:
            raise ValueError("No bids found.")

        if not self.asks:
            raise ValueError("No asks found.")

    # -------------------------------------------------
    # Basic Prices
    # -------------------------------------------------

    @property
    def best_bid(self):

        return self.bids[0]["price"]

    @property
    def best_ask(self):

        return self.asks[0]["price"]

    @property
    def spread(self):

        return round(

            self.best_ask -
            self.best_bid,

            8

        )

    @property
    def mid_price(self):

        return round(

            (

                self.best_bid +
                self.best_ask

            ) / 2,

            8

        )

    @property
    def spread_percent(self):

        return round(

            (

                self.spread /
                self.mid_price

            ) * 100,

            6

        )

    # -------------------------------------------------
    # Volume
    # -------------------------------------------------

    @property
    def total_bid_volume(self):

        return round(

            sum(

                x["qty"]

                for x in self.bids

            ),

            4

        )

    @property
    def total_ask_volume(self):

        return round(

            sum(

                x["qty"]

                for x in self.asks

            ),

            4

        )

    @property
    def bid_ask_ratio(self):

        ask = self.total_ask_volume

        if ask == 0:

            return 0

        return round(

            self.total_bid_volume /
            ask,

            4

        )

    # -------------------------------------------------
    # Imbalance
    # -------------------------------------------------

    @property
    def order_imbalance(self):

        bid = self.total_bid_volume
        ask = self.total_ask_volume

        total = bid + ask

        if total == 0:

            return 0

        return round(

            (bid - ask) / total,

            4

        )

    @property
    def buy_pressure(self):

        return round(

            (

                self.total_bid_volume /

                (

                    self.total_bid_volume +

                    self.total_ask_volume

                )

            ) * 100,

            2

        )

    @property
    def sell_pressure(self):

        return round(

            (

                self.total_ask_volume /

                (

                    self.total_bid_volume +

                    self.total_ask_volume

                )

            ) * 100,

            2

        )

    # -------------------------------------------------
    # Biggest Orders
    # -------------------------------------------------

    @property
    def largest_bid(self):

        return max(

            self.bids,

            key=lambda x: x["qty"]

        )

    @property
    def largest_ask(self):

        return max(

            self.asks,

            key=lambda x: x["qty"]

        )

    # -------------------------------------------------
    # Average Liquidity
    # -------------------------------------------------

    @property
    def average_bid_size(self):

        return round(

            mean(

                x["qty"]

                for x in self.bids

            ),

            4

        )

    @property
    def average_ask_size(self):

        return round(

            mean(

                x["qty"]

                for x in self.asks

            ),

            4

        )

    # -------------------------------------------------
    # Buy / Sell Walls
    # -------------------------------------------------

    @property
    def buy_wall(self):

        avg = self.average_bid_size

        wall = max(
            self.bids,
            key=lambda x: x["qty"]
        )

        detected = wall["qty"] >= avg * 3

        return {

            "detected": detected,

            "price": wall["price"],

            "qty": wall["qty"],

        }

    @property
    def sell_wall(self):

        avg = self.average_ask_size

        wall = max(
            self.asks,
            key=lambda x: x["qty"]
        )

        detected = wall["qty"] >= avg * 3

        return {

            "detected": detected,

            "price": wall["price"],

            "qty": wall["qty"],

        }

    # -------------------------------------------------
    # Liquidity Score
    # -------------------------------------------------

    @property
    def liquidity_score(self):

        total = (
            self.total_bid_volume +
            self.total_ask_volume
        )

        if total >= 5000:
            return 100

        if total >= 3000:
            return 90

        if total >= 1500:
            return 75

        if total >= 800:
            return 60

        if total >= 400:
            return 45

        return 25

    # -------------------------------------------------
    # Market Depth
    # -------------------------------------------------

    @property
    def market_depth(self):

        score = self.liquidity_score

        if score >= 90:
            return "Very Deep"

        elif score >= 70:
            return "Deep"

        elif score >= 50:
            return "Normal"

        elif score >= 30:
            return "Thin"

        return "Very Thin"

    # -------------------------------------------------
    # Institutional Bias
    # -------------------------------------------------

    @property
    def institutional_bias(self):

        score = 0

        if self.bid_ask_ratio > 1.20:
            score += 25

        elif self.bid_ask_ratio < 0.80:
            score -= 25

        if self.order_imbalance > 0.15:
            score += 25

        elif self.order_imbalance < -0.15:
            score -= 25

        if self.buy_wall["detected"]:
            score += 20

        if self.sell_wall["detected"]:
            score -= 20

        if self.buy_pressure > 55:
            score += 15

        elif self.sell_pressure > 55:
            score -= 15

        if score >= 40:
            return "Strong Bullish"

        elif score >= 15:
            return "Bullish"

        elif score <= -40:
            return "Strong Bearish"

        elif score <= -15:
            return "Bearish"

        return "Neutral"

    # -------------------------------------------------
    # AI Score
    # -------------------------------------------------

    @property
    def ai_score(self):

        score = 50

        if self.bid_ask_ratio > 1:
            score += 10
        else:
            score -= 10

        if self.order_imbalance > 0:
            score += 10
        else:
            score -= 10

        if self.buy_wall["detected"]:
            score += 10

        if self.sell_wall["detected"]:
            score -= 10

        if self.buy_pressure > 55:
            score += 10

        if self.sell_pressure > 55:
            score -= 10

        score += (self.liquidity_score - 50) / 5

        score = max(0, min(100, score))

        return round(score, 2)

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def analyze(self):

        return {

            "best_bid": self.best_bid,

            "best_ask": self.best_ask,

            "spread": self.spread,

            "spread_percent": self.spread_percent,

            "mid_price": self.mid_price,

            "bid_volume": self.total_bid_volume,

            "ask_volume": self.total_ask_volume,

            "bid_ask_ratio": self.bid_ask_ratio,

            "order_imbalance": self.order_imbalance,

            "buy_pressure": self.buy_pressure,

            "sell_pressure": self.sell_pressure,

            "largest_bid": self.largest_bid,

            "largest_ask": self.largest_ask,

            "average_bid_size": self.average_bid_size,

            "average_ask_size": self.average_ask_size,

            "buy_wall": self.buy_wall,

            "sell_wall": self.sell_wall,

            "liquidity_score": self.liquidity_score,

            "market_depth": self.market_depth,

            "institutional_bias": self.institutional_bias,

            "ai_score": self.ai_score,

        }