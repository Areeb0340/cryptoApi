from core.market_data.cache import cache


class VolatilityFeature:

    def calculate(self, symbol, timeframe="1m"):

        symbol = symbol.upper()

        if symbol not in cache.klines:
            return None

        if timeframe not in cache.klines[symbol]:
            return None

        k = cache.klines[symbol][timeframe]

        high = float(k["h"])
        low = float(k["l"])
        open_price = float(k["o"])
        close = float(k["c"])

        volume = float(k["v"])

        price_range = high - low

        if open_price == 0:
            range_percent = 0
        else:
            range_percent = (price_range / open_price) * 100

        candle_body = abs(close - open_price)

        upper_wick = high - max(open_price, close)

        lower_wick = min(open_price, close) - low

        if candle_body == 0:
            body_ratio = 0
        else:
            body_ratio = candle_body / price_range if price_range else 0

        if range_percent > 2:
            volatility = "EXTREME"

        elif range_percent > 1:
            volatility = "HIGH"

        elif range_percent > 0.4:
            volatility = "MEDIUM"

        else:
            volatility = "LOW"

        return {
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "range": round(price_range, 8),
            "range_percent": round(
                range_percent,
                4,
            ),
            "body": round(
                candle_body,
                8,
            ),
            "upper_wick": round(
                upper_wick,
                8,
            ),
            "lower_wick": round(
                lower_wick,
                8,
            ),
            "body_ratio": round(
                body_ratio,
                4,
            ),
            "volatility": volatility,
        }


volatility_feature = VolatilityFeature()
