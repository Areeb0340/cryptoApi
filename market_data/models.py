from django.db import models


class Coin(models.Model):
    symbol = models.CharField(max_length=30, unique=True)
    base_asset = models.CharField(max_length=20)
    quote_asset = models.CharField(max_length=20)
    exchange = models.CharField(max_length=20, default="binance")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


class Candle(models.Model):

    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="candles"
    )

    timeframe = models.CharField(max_length=10)

    open = models.DecimalField(max_digits=20, decimal_places=8)
    high = models.DecimalField(max_digits=20, decimal_places=8)
    low = models.DecimalField(max_digits=20, decimal_places=8)
    close = models.DecimalField(max_digits=20, decimal_places=8)

    volume = models.DecimalField(max_digits=30, decimal_places=8)

    quote_volume = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        default=0
    )

    trades = models.IntegerField(default=0)

    taker_buy_base_volume = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        default=0
    )

    taker_buy_quote_volume = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        default=0
    )

    timestamp = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("coin", "timeframe", "timestamp")

    def __str__(self):
        return f"{self.coin.symbol} - {self.timeframe}"


class OpenInterest(models.Model):

    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="open_interest"
    )

    timeframe = models.CharField(max_length=10)

    open_interest = models.DecimalField(
        max_digits=30,
        decimal_places=8
    )

    open_interest_value = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        default=0
    )

    timestamp = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("coin", "timeframe", "timestamp")

    def __str__(self):
        return f"{self.coin.symbol} - {self.timeframe}"
    
class FundingRate(models.Model):

    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="funding_rates"
    )

    funding_rate = models.DecimalField(
        max_digits=20,
        decimal_places=10
    )

    mark_price = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        default=0
    )

    funding_time = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("coin", "funding_time")

    def __str__(self):
        return f"{self.coin.symbol} - {self.funding_rate}"
    
class MarkPrice(models.Model):

    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="mark_prices"
    )

    mark_price = models.DecimalField(
        max_digits=30,
        decimal_places=8
    )

    index_price = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        default=0
    )

    estimated_settle_price = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        default=0
    )

    funding_rate = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        default=0
    )

    next_funding_time = models.BigIntegerField(default=0)

    timestamp = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("coin", "timestamp")

    def __str__(self):
        return f"{self.coin.symbol} - {self.mark_price}"
    
class LongShortRatio(models.Model):

    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="long_short_ratios"
    )

    timeframe = models.CharField(max_length=10)

    long_short_ratio = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    long_account = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0
    )

    short_account = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0
    )

    timestamp = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "coin",
            "timeframe",
            "timestamp"
        )

    def __str__(self):
        return f"{self.coin.symbol} - {self.timeframe}"
    
class TopTraderRatio(models.Model):

    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="top_trader_ratios"
    )

    timeframe = models.CharField(max_length=10)

    long_short_ratio = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    long_account = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0
    )

    short_account = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0
    )

    timestamp = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "coin",
            "timeframe",
            "timestamp"
        )

    def __str__(self):
        return f"{self.coin.symbol} - {self.timeframe}"
    
class TopTraderPositionRatio(models.Model):

    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
        related_name="top_position_ratios"
    )

    timeframe = models.CharField(max_length=10)

    long_short_ratio = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    long_account = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0
    )

    short_account = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0
    )

    timestamp = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "coin",
            "timeframe",
            "timestamp"
        )

    def __str__(self):
        return f"{self.coin.symbol} - {self.timeframe}"