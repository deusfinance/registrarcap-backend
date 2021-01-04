from django.db import models
from rest_framework.fields import JSONField


class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)  # ETH
    contract = models.CharField(max_length=255)


class MarketMaker(models.Model):
    contract = models.CharField(max_length=255)
    token_id = models.CharField(max_length=255)


class Transaction:
    BUY = 'b'
    SELL = 's'
    OTHER = 'o'

    TRANSACTION_TYPES = (
        (BUY, 'buy'),
        (SELL, 'sell'),
        (OTHER, 'other'),
    )

    type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)

    timestamp = models.CharField(max_length=12)
    date = models.DateTimeField()

    # we need these
    hash = models.CharField(max_length=255)

    ether_value = models.DecimalField(max_digits=38, decimal_places=18)
    internal_ether_value = models.DecimalField(max_digits=38, decimal_places=18)
    token_value = models.DecimalField(max_digits=38, decimal_places=18)

    from_contract = models.CharField(max_length=255)
    to_contract = models.CharField(max_length=255)
    from_token = models.CharField(max_length=255)
    to_token = models.CharField(max_length=255)

    token_address = models.CharField(max_length=255)
    token_decimals = models.IntegerField()
    token_name = models.CharField(max_length=255)
    token_symbol = models.CharField(max_length=255)

    # end

    status = models.CharField(max_length=1)
    block_hash = models.CharField(max_length=255)
    block_number = models.BigIntegerField()
    nonce = models.IntegerField()
    transaction_index = models.IntegerField()

    total_supply = models.DecimalField(max_digits=38, decimal_places=18)

    last_updated = models.FloatField()

    holders_count = models.IntegerField()

    coin_gecko = models.CharField(max_length=255)

    result = JSONField()
    token_info = JSONField()
    operations = JSONField()

    input = models.CharField(max_length=255)


class Trade(models.Model):
    hash = models.CharField(max_length=255, null=True, unique=True)
    timestamp = models.IntegerField()
    price = models.DecimalField(max_digits=38, decimal_places=18)
    block = models.IntegerField()

    class Meta:
        ordering = ('timestamp', 'block')


class Candlestick(models.Model):
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='candlesticks')

    timestamp = models.IntegerField()

    open_price = models.DecimalField(max_digits=38, decimal_places=18)
    high_price = models.DecimalField(max_digits=38, decimal_places=18)
    low_price = models.DecimalField(max_digits=38, decimal_places=18)
    close_price = models.DecimalField(max_digits=38, decimal_places=18)

    volume = models.DecimalField(max_digits=38, decimal_places=18)
