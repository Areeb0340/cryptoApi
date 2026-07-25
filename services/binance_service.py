from urllib import response

import ccxt
import requests


class BinanceService:

    BASE_URL = "https://fapi.binance.com"

    def __init__(self):

        self.exchange = ccxt.binance({
            "options": {
                "defaultType": "future"
            }
        })

    # -----------------------------
    # Futures Markets
    # -----------------------------
    def get_markets(self):

        markets = self.exchange.load_markets()

        futures = {}

        for symbol, market in markets.items():

            if (
                market.get("swap") is True
                and market.get("quote") == "USDT"
                and market.get("active") is True
            ):
                futures[symbol] = market

        return futures

    # -----------------------------
    # Official Binance Futures API
    # -----------------------------
    def get_klines(
        self,
        symbol,
        timeframe="1h",
        limit=500
    ):

        symbol = symbol.replace("/", "").replace(":USDT", "")

        url = f"{self.BASE_URL}/fapi/v1/klines"

        params = {
            "symbol": symbol,
            "interval": timeframe,
            "limit": limit,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
    

        # -----------------------------
    # Open Interest
    # -----------------------------
    def get_open_interest_history(
        self,
        symbol,
        timeframe="5m",
        limit=500
    ):

        symbol = symbol.replace("/", "").replace(":USDT", "")

        url = f"{self.BASE_URL}/futures/data/openInterestHist"

        params = {
            "symbol": symbol,
            "period": timeframe,
            "limit": limit,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
    
        # -----------------------------
    # Funding Rate
    # -----------------------------
    def get_funding_rate(
        self,
        symbol,
        limit=500
    ):

        symbol = symbol.replace("/", "").replace(":USDT", "")

        url = f"{self.BASE_URL}/fapi/v1/fundingRate"

        params = {
            "symbol": symbol,
            "limit": limit,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
# -----------------------------
# Mark Price
# -----------------------------
    def get_mark_price(self):

     url = f"{self.BASE_URL}/fapi/v1/premiumIndex"

     response = requests.get(
        url,
        timeout=30,
     )

     response.raise_for_status()

     return response.json()
    
    # -----------------------------
# Global Long Short Ratio
# -----------------------------
    def get_long_short_ratio(
      self,
    symbol,
    timeframe="5m",
    limit=500
 ):

     symbol = symbol.replace("/", "").replace(":USDT", "")

     url = f"{self.BASE_URL}/futures/data/globalLongShortAccountRatio"

     params = {
        "symbol": symbol,
        "period": timeframe,
        "limit": limit,
    }

     response = requests.get(
        url,
        params=params,
        timeout=30,
    )

     response.raise_for_status()

     return response.json()
    
    # -----------------------------
# Top Trader Long Short Ratio
# -----------------------------
    def get_top_trader_ratio(
     self,
      symbol,
      timeframe="5m",
      limit=500
    ):

     symbol = symbol.replace("/", "").replace(":USDT", "")

     url = f"{self.BASE_URL}/futures/data/topLongShortAccountRatio"

     params = {
        "symbol": symbol,
        "period": timeframe,
         "limit": limit,
     }

     response = requests.get(
        url,
        params=params,
        timeout=30,
     )

     response.raise_for_status()

     return response.json()
    
        # -----------------------------
# Top Trader Position Ratio
# -----------------------------
    def get_top_position_ratio(
     self,
     symbol,
     timeframe="5m",
     limit=500
 ):

     symbol = symbol.replace("/", "").replace(":USDT", "")

     url = f"{self.BASE_URL}/futures/data/topLongShortPositionRatio"

     params = {
        "symbol": symbol,
        "period": timeframe,
        "limit": limit,
     }

     response = requests.get(
        url,
        params=params,
        timeout=30,
    )

     response.raise_for_status()

     return response.json()