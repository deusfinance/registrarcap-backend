import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100, unique=True)  # ETH
    description = models.CharField(max_length=255)  # ETH

    def __str__(self):
        return "{} ({}) ({})".format(self.name, self.symbol, self.id)


class Trade(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='trades')

    hash = models.CharField(max_length=255, null=True, unique=True)
    block = models.IntegerField()
    timestamp = models.IntegerField()

    amount = models.DecimalField(max_digits=38, decimal_places=18)
    eth_price = models.DecimalField(max_digits=38, decimal_places=18)
    usd_price = models.DecimalField(max_digits=38, decimal_places=18)
    btc_price = models.DecimalField(max_digits=38, decimal_places=18)
    deus_price = models.DecimalField(max_digits=38, decimal_places=18)
    dea_price = models.DecimalField(max_digits=38, decimal_places=18)

    other = JSONField(default=dict)

    class Meta:
        ordering = ('timestamp', 'block')

    def __str__(self):
        return "{}, {}: Amount: {}, Eth Price:{} ({})".format(
            self.currency.symbol,
            datetime.datetime.fromtimestamp(self.timestamp).isoformat(),
            round(self.amount, 2),
            round(self.eth_price, 2),
            self.id)


class Candlestick(models.Model):
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='candlesticks')

    timestamp = models.IntegerField()

    open_price = models.DecimalField(max_digits=38, decimal_places=18)
    high_price = models.DecimalField(max_digits=38, decimal_places=18)
    low_price = models.DecimalField(max_digits=38, decimal_places=18)
    close_price = models.DecimalField(max_digits=38, decimal_places=18)

    volume = models.DecimalField(max_digits=38, decimal_places=18)
