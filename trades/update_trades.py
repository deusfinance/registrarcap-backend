from time import sleep

import requests
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from trades.models import Trade, Currency


class UpdateTrades:
    prices = {
        'eth_to_usd': [],  # fetch from coingecho
        'eth_to_btc': [],  # fetch from coingecho
        'deus_to_eth': [],  # fetch from DB
        'deus_to_dea': []  # fetch Dr-Collector
    }

    def __init__(self, currency: Currency, get_trades):
        self.get_trades = get_trades
        self.currency = currency
        self.limit = 100

    def update(self):
        try:
            last_trade = Trade.objects.filter(currency=self.currency).latest('timestamp')
            from_block = last_trade.block
            from_timestamp = last_trade.timestamp
            print("#{} is latest trade for {}, starting from block: {} and timestamp: {}".format(
                last_trade.id,
                self.currency.symbol,
                from_block,
                from_timestamp
            ))
        except Trade.DoesNotExist:
            from_block = 10894568  # first deus transaction block
            from_timestamp = 1
            print("There is no trade for {}, starting from block: {} and timestamp: {}".format(
                self.currency.name,
                from_block,
                from_timestamp
            ))

        print("Fetching trades...")
        new_trades = self.get_trades(from_block, self.limit)
        new_trades_len = len(new_trades)
        print("There is {} new trades".format(new_trades_len))

        if new_trades_len == 0:
            return

        new_trades = list(filter(lambda t: t['timestamp'] >= from_timestamp, new_trades))

        self.fetch_prices(
            new_trades[0]['timestamp'],
            new_trades[-1]['timestamp'],
            new_trades[0]['price_type']
        )

        for trade in new_trades:
            prices = self.get_prices(
                trade.pop('price'),
                trade.pop('price_type'),
                trade['amount'],
                trade['timestamp'],
            )

            try:
                Trade.objects.create(
                    currency=self.currency,
                    **prices,
                    **trade
                )
            except IntegrityError:
                pass

        if new_trades_len >= self.limit:
            print("There is more than {} trades, running update method again\n".format(self.limit))
            self.update()

    def fetch_prices(self, from_timestamp, to_timestamp, price_type):

        # Add Caching

        if price_type == 'deus':
            print("Generating deus prices")
            qs = Trade.objects.filter(currency__symbol='DEUS', timestamp__range=(from_timestamp, to_timestamp))
            timestamps = qs.values_list('timestamp', flat=True)
            eth_prices = qs.values_list('eth_price', flat=True)
            self.prices['deus_to_eth'] = [[timestamps[i], eth_prices[i]] for i in range(len(timestamps))]

        print("Fetching prices from Coingecko")
        url = 'https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency={}&from={}&to={}'
        i = 0
        timestamp = from_timestamp
        while timestamp <= to_timestamp:
            to = timestamp + 24 * 60 * 60 - 1  # add one day (coingecho limit)

            eth_to_usd = requests.get(url.format('usd', timestamp, to)).json()['prices']
            eth_to_btc = requests.get(url.format('btc', timestamp, to)).json()['prices']

            eth_to_usd = list(map(lambda p: (p[0] // 1000, p[1]), eth_to_usd))
            eth_to_btc = list(map(lambda p: (p[0] // 1000, p[1]), eth_to_btc))

            self.prices['eth_to_usd'] += eth_to_usd
            self.prices['eth_to_btc'] += eth_to_btc

            # temporary
            deus_to_eth_url = 'https://api.coingecko.com/api/v3/coins/deus-finance/market_chart/range?vs_currency={}&from={}&to={}'
            deus_to_eth = requests.get(deus_to_eth_url.format('eth', timestamp, to)).json()['prices']
            deus_to_eth = list(map(lambda p: (p[0] // 1000, p[1]), deus_to_eth))
            self.prices['deus_to_eth'] += deus_to_eth

            timestamp = to
            i += 2

            # coingecho 100 req/min
            if i >= 100:
                print("Coingecho limit reached, sleep for 60 seconds.")
                sleep(60)

        # Deus Dea Prices
        url = "https://dr-collector-api.herokuapp.com/v1/transactions?poolContract=0x92adab6d8dc13dbd9052b291cfc1d07888299d65&from={}&to={}"
        dea_deus_swaps = requests.get(url.format(from_timestamp - 24 * 60 * 60, to_timestamp)).json()
        self.prices['deus_to_dea'] = [(s['timestamp'], 1 / s['price']) for s in dea_deus_swaps]

    def get_prices(self, price, price_type, amount, timestamp):
        if price_type == 'eth':
            eth_price = price

            if self.currency.symbol == 'deus':
                deus_price = 1
            else:
                eth_to_deus = list(map(lambda x: (x[0], 1 / x[1]), self.prices['deus_to_eth']))
                deus_price = self.get_closest_price(timestamp, eth_to_deus)

        elif price_type == 'deus':
            deus_price = price
            eth_price = self.get_closest_price(timestamp, self.prices['deus_to_eth'])
        else:
            raise ValidationError("price type {} is not supported".format(price_type))

        btc_price = self.get_closest_price(timestamp, self.prices['eth_to_btc']) * eth_price
        usd_price = self.get_closest_price(timestamp, self.prices['eth_to_usd']) * eth_price
        dea_price = self.get_closest_price(timestamp, self.prices['deus_to_dea']) * deus_price

        return {
            'deus_price': deus_price,
            'eth_price': eth_price,
            'btc_price': btc_price,
            'usd_price': usd_price,
            'dea_price': dea_price,
        }

    @staticmethod
    def get_closest_price(timestamp, prices):
        closest_price = 0
        timestamp = int(timestamp)
        min_diff = timestamp
        for price in prices:
            price_timestamp = int(price[0])

            if len(str(price_timestamp)) != len(str(timestamp)):
                raise ValidationError("Timestamp length mismatch: {} - {}".format(price_timestamp, timestamp))

            diff = abs(int(price_timestamp) - int(timestamp))
            if diff < min_diff:
                closest_price = price[1]
                min_diff = diff

        # Raise error if closest price timestamp is more 24 hours
        if min_diff >= 24 * 60 * 60:
            print("Prices are not acceptable for timestamp: {}, min-diff: {}".format(
                timestamp,
                min_diff
            ))
            closest_price = 0

        return closest_price
