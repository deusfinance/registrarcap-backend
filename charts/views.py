import datetime
import math

from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from trades.models import Trade, Currency


class GetTimeView(APIView):
    def get(self, request):
        return Response(datetime.datetime.now().timestamp())


class GetConfigView(APIView):
    def get(self, request):
        return Response({
            "exchanges": [{
                "value": 'DEUS Swap',
                "name": 'DEUS Swap',
                "desc": 'DEUS Swap',
            }],
            "symbols_types": [{
                "name": 'crypto',
                "value": 'crypto',
            }],
            "supported_resolutions": ['60', 'D'],

            "supports_marks": False,
            "supports_timescale_marks": False,
            "supports_time": True,

            "supports_search": True,
            "supports_group_request": False,
        })


deus_symbol = {
    "name": "DEUS/ETH",
    "ticker": "1",
    "description": "DEUS/ETH",

    "type": "crypto",

    "session": "24x7",
    "holidays": "",
    "corrections": "",

    "exchange": "DEUS Swap",
    "listed_exchange": "DEUS Swap",

    "timezone": "Etc/UTC",

    # TL,DR
    "minmov": 1,
    "pricescale": 1000000,
    "has_intraday": True,
    "has_weekly_and_monthly": True,
    "volume_precision": 100,

    "data_status": "streaming",

    "supported_resolutions": ['60', 'D'],

    "has_no_volume": False,

}


def item_to_list(item, keys, n=10):
    result = [item]
    for i in range(1, n):
        new_item = item.copy()
        for key in keys:
            value = new_item[key]
            if isinstance(value, int):
                new_item[key] = value + i
            else:
                new_item[key] = "{} {}".format(value, i)
        result.append(new_item)
    return result


symbols = item_to_list(deus_symbol, ['name', 'description', 'ticker'], 100)


class SearchSymbolView(APIView):

    def get(self, request):
        query = request.GET.get('query', '')
        limit = int(request.GET.get('limit', 10))

        qs = Currency.objects.filter(
            Q(
                Q(name__icontains=query) |
                Q(symbol__icontains=query) |
                Q(description__icontains=query)
            )
        )[:limit]

        result = []
        target_currencies = ['deus', 'eth', 'usd', 'btc', 'dea']
        for currency in qs.all():
            for target_currency in target_currencies:
                if currency.symbol == target_currency:
                    continue
                result.append({
                    'symbol': "{}/{}".format(currency.name.upper(), target_currency.upper()),
                    'ticker': "{}/{}".format(currency.symbol, target_currency.lower()),
                    'full_name': "{} to {}".format(currency.name.upper(), target_currency.upper()),
                    'description': currency.description,
                    'exchange': 'DEUS Swap',
                    'type': 'crypto'
                })

        return Response(result[:limit])


class ResolveSymbolView(APIView):

    def get(self, request):
        ticker = request.GET.get('symbol')  # ticker
        currency_symbol, target_currency = ticker.split('/')
        currency = Currency.objects.get(symbol=currency_symbol)

        symbol = {
            "name": "{}/{}".format(currency.name.upper(), target_currency.upper()),
            'ticker': "{}/{}".format(currency.symbol, target_currency.lower()),
            "description": currency.description,

            "type": "crypto",

            "session": "24x7",
            "holidays": "",
            "corrections": "",

            "exchange": "DEUS Swap",
            "listed_exchange": "DEUS Swap",

            "timezone": "Etc/UTC",

            # TL,DR
            "minmov": 1,
            "pricescale": 1000000,
            "has_intraday": True,
            "has_weekly_and_monthly": True,
            "volume_precision": 100,

            "data_status": "streaming",

            "supported_resolutions": ['60', 'D'],

            "has_no_volume": False,
        }

        return Response(symbol)


def get_candlesticks(currency: Currency, interval: int = 1, from_timestamp=None, to_timestamp=None,
                     target_currency='eth'):
    """
    :param currency:
    :param target_currency: eth, btc, usd
    :param to_timestamp:
    :param from_timestamp:
    :param contract_address: Ex 0x3b...
    :param interval: candles interval in minutes (it's 1 minute by default)
    :return: []
    """

    interval = int(interval) * 60

    filters = {
        'currency': currency,
        "{}_price__gt".format(target_currency): 0
    }
    qs = Trade.objects.filter(**filters)

    if from_timestamp:
        try:
            from_timestamp = int(from_timestamp)
        except:
            from_timestamp = None
    else:
        from_timestamp = int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp())

    qs = qs.filter(timestamp__gt=from_timestamp)

    if to_timestamp:
        try:
            to_timestamp = int(to_timestamp)
            qs = qs.filter(timestamp__lt=to_timestamp)
        except:
            pass

    trades = qs.all()

    if trades.count() == 0:
        return []

    candlesticks = []

    open_price = getattr(trades[0], "{}_price".format(target_currency))

    candlestick_timestamp = max(trades[0].timestamp, from_timestamp)
    candlestick_timestamp = candlestick_timestamp - candlestick_timestamp % interval

    now_timestamp = int(datetime.datetime.now().timestamp())
    last_candlestick_timestamp = now_timestamp - now_timestamp % interval

    high_price = -math.inf
    low_price = math.inf
    volume = 0

    trades_count = len(trades)
    trades_in_interval = 0
    for i in range(trades_count):
        trade = trades[i]

        timestamp = trade.timestamp
        price = getattr(trade, "{}_price".format(target_currency))
        volume += trade.amount

        if candlestick_timestamp + interval < timestamp or i == trades_count - 1:
            print(candlestick_timestamp, trades_in_interval)

            if i == 0:
                close_price = open_price
            else:
                close_price = getattr(trades[i - 1], "{}_price".format(target_currency))

            if high_price == -math.inf:
                high_price = open_price

            if low_price == math.inf:
                low_price = open_price

            candlesticks.append({
                't': candlestick_timestamp,
                'o': open_price,
                'h': high_price,
                'l': low_price,
                'c': close_price,
                'v': volume
            })

            # Next candle
            candlestick_timestamp += interval
            open_price = close_price
            high_price = -math.inf
            low_price = math.inf
            trades_in_interval = 0
            volume = 0

        high_price = max(high_price, price)
        low_price = min(low_price, price)
        trades_in_interval += 1

    candlestick_timestamp = candlesticks[-1]['t']
    price = candlesticks[-1]['c']
    volume = candlesticks[-1]['v']
    while candlestick_timestamp < last_candlestick_timestamp:
        candlestick_timestamp += interval

        candlesticks.append({
            't': candlestick_timestamp,
            'o': price,
            'h': price,
            'l': price,
            'c': price,
            'v': volume
        })

    return candlesticks


class GetBarsView(APIView):
    def get(self, request):

        ticker = request.GET.get('symbol')  # ticker
        currency_symbol, target_currency = ticker.split('/')
        currency = get_object_or_404(Currency, symbol=currency_symbol)

        candlesticks = get_candlesticks(
            currency,
            self.get_resolution(),
            request.GET.get('from'),
            request.GET.get('to'),
            target_currency
        )

        result = {
            't': [candle['t'] for candle in candlesticks],
            'c': [candle['c'] for candle in candlesticks],
            'o': [candle['o'] for candle in candlesticks],
            'h': [candle['h'] for candle in candlesticks],
            'l': [candle['l'] for candle in candlesticks],
            'v': [candle['v'] for candle in candlesticks]
        }

        if len(candlesticks):
            result['s'] = 'ok'
        else:
            result['s'] = 'no_data'

        return Response(result)

    def get_resolution(self):
        resolutions_to_minutes = {
            "60": 60,
            "60m": 60,
            "D": 1440,
            "1D": 1440,
        }
        resolution = self.request.GET.get('resolution', "60")
        return resolutions_to_minutes[resolution]
