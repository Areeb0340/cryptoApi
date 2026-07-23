from .cache import cache
from core.features.orderbook import orderbook_features
from core.smc.market_structure import market_structure
from core.smc.bos import bos
from core.smc.smc_engine import smc_engine
from core.signal.signal_engine import signal_engine


class MarketDataEngine:

    # ==========================================================
    # MAIN PROCESSOR
    # ==========================================================

    def process(self, payload):

        stream = payload["stream"].lower()
        data = payload["data"]

        if "@trade" in stream:
            self.process_trade(data)

        elif "@depth" in stream:
            self.process_depth(data)

        elif "@kline" in stream:
            self.process_kline(data)

        elif "@bookticker" in stream:
            self.process_bookticker(data)

    # ==========================================================
    # TRADE
    # ==========================================================

    def process_trade(self, data):

        symbol = data["s"]

        price = float(data["p"])
        qty = float(data["q"])

        # Latest Price
        cache.prices[symbol] = price

        # Store Recent Trades
        cache.trades[symbol].append(
            {
                "price": price,
                "qty": qty,
                "buyer_maker": data["m"],
                "time": data["T"],
            }
        )

        # Delta Volume + CVD
        if data["m"]:
            # Seller Aggressor
            cache.delta_volume[symbol]["sell"] += qty
            cache.cvd[symbol] -= qty
        else:
            # Buyer Aggressor
            cache.delta_volume[symbol]["buy"] += qty
            cache.cvd[symbol] += qty

    # ==========================================================
    # ORDER BOOK
    # ==========================================================

    def process_depth(self, data):

        symbol = data["s"]

        cache.orderbooks[symbol] = {
            "bids": data["b"],
            "asks": data["a"],
            "time": data["T"],
        }

        orderbook_features.update(symbol)

    # ==========================================================
    # KLINES
    # ==========================================================

    def process_kline(self, data):

        k = data["k"]

        symbol = k["s"]
        timeframe = k["i"]

        candle = {
            "open_time": k["t"],
            "close_time": k["T"],
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"]),
            "closed": k["x"],
        }

        candles = cache.klines[symbol][timeframe]

        if candles:

            if candles[-1]["open_time"] == candle["open_time"]:
                candles[-1] = candle
            else:
                candles.append(candle)

        else:
            candles.append(candle)

        # Candle close hone ke baad hi analysis
        if not candle["closed"]:
            return

        # 1) SMC Update
        smc_engine.update(symbol, timeframe)

        # 2) Signal Generate
        signal = signal_engine.generate(
            symbol,
            timeframe,
        )

        # 3) Agar signal hi nahi bana
        if signal is None:
            return

        decision = signal["decision"]

        print("\n" + "=" * 70)
        print("AI SIGNAL GENERATED")
        print("=" * 70)

        print(f"Symbol      : {signal['symbol']}")
        print(f"Timeframe   : {signal['timeframe']}")
        print(f"Price       : {signal['price']}")
        print(f"Score       : {signal['indicator_score']}")

        print()

        print(f"Signal      : {decision['signal']}")
        print(f"Confidence  : {decision['confidence']}%")

        print(f"Bullish     : {decision['bullish_points']}")
        print(f"Bearish     : {decision['bearish_points']}")

        print("\nReasons")

        for reason in decision["reasons"]:
            print(f"- {reason}")

        print("=" * 70)

    # ==========================================================
    # BOOK TICKER
    # ==========================================================

    def process_bookticker(self, data):

        symbol = data["s"]

        cache.book_tickers[symbol] = {
            "bid": float(data["b"]),
            "bid_qty": float(data["B"]),
            "ask": float(data["a"]),
            "ask_qty": float(data["A"]),
            "time": data.get("T"),
        }


market_data_engine = MarketDataEngine()
