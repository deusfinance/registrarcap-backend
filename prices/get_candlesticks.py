import math

from django.db.models.aggregates import Max

from prices.models import Candlestick, Trade


def get_candlesticks(contract_address, interval: int = 1, from_timestamp=None, to_timestamp=None):
    """
    :param to_timestamp:
    :param from_timestamp:
    :param contract_address: Ex 0x3b...
    :param interval: candles interval in minutes (it's 1 minute by default)
    :return: []
    """

    interval = int(interval) * 60

    try:
        from_timestamp = int(from_timestamp)
    except:
        from_timestamp = 0

    try:
        to_timestamp = int(to_timestamp)
    except:
        to_timestamp = Candlestick.objects.aggregate(to_timestamp=Max('timestamp'))['to_timestamp'] * 100

    trades = Trade.objects.filter(timestamp__range=(from_timestamp, to_timestamp)).all()

    candlesticks = []

    open_time = trades[0].timestamp
    open_price = trades[0].price

    candlestick_timestamp = open_time - open_time % 100

    high_price = -math.inf
    low_price = math.inf
    volume = 0

    for i in range(len(trades)):
        trade = trades[i]

        timestamp = trade.timestamp
        price = trade.price
        volume += price

        if candlestick_timestamp + interval < timestamp:
            close_price = trades[i - 1].price
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

        high_price = max(high_price, price)
        low_price = min(low_price, price)

    return candlesticks


def get_candlesticks_from_db(contract_address, interval: int = 1, from_timestamp=None, to_timestamp=None):
    interval = int(interval) * 60

    try:
        from_timestamp = int(from_timestamp)
    except:
        from_timestamp = 0

    try:
        to_timestamp = int(to_timestamp)
    except:
        to_timestamp = Candlestick.objects.aggregate(to_timestamp=Max('timestamp'))['to_timestamp'] * 100

    qs = Candlestick.objects.filter(timestamp__range=(from_timestamp, to_timestamp)).all().order_by('timestamp')

    candlesticks = []

    timestamp = qs[0].timestamp - qs[0].timestamp % 100

    open_price = qs[0].open_price
    high_price = qs[0].high_price
    low_price = qs[0].low_price

    next_timestamp = timestamp + interval
    prev_candlestick = None

    for candlestick in qs:
        if candlestick.timestamp < next_timestamp:
            high_price = max(high_price, candlestick.high_price)
            low_price = min(low_price, candlestick.low_price)
        else:
            timestamp = next_timestamp
            next_timestamp += interval

            close_price = prev_candlestick.close_price
            volume = prev_candlestick.volume

            candlesticks.append(
                {
                    't': timestamp,
                    'o': open_price,
                    'h': high_price,
                    'l': low_price,
                    'c': close_price,
                    'v': volume
                }
            )

            open_price = candlestick.open_price
            high_price = candlestick.high_price
            low_price = candlestick.low_price

        prev_candlestick = candlestick

    return candlesticks
