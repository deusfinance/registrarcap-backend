import json
import math

from prices.get_transactions import update_transactions


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
        to_timestamp = math.inf

    update_transactions()

    transactions = []
    with open('{}/transactions.json'.format(contract_address), 'r') as transactions_file:
        for transaction in json.load(transactions_file):
            transactions.append({
                'timestamp': int(transaction['timeStamp']),
                'value': int(transaction['value']),
            })
        transactions.sort(key=lambda o: o['timestamp'])

    transactions = list(filter(lambda tx: from_timestamp <= tx['timestamp'] <= to_timestamp, transactions))

    candlesticks = []

    open_time = transactions[0]['timestamp']
    open_price = transactions[0]['value']
    candlestick_timestamp = open_time - open_time % 100

    high_price = -math.inf
    low_price = math.inf
    volume = 0

    for i in range(len(transactions)):
        transaction = transactions[i]

        timestamp = transaction['timestamp']
        value = transaction['value']
        volume += value

        if candlestick_timestamp + interval < timestamp:
            candlesticks.append({
                't': open_time,
                'o': open_price,
                'h': high_price,
                'l': low_price,
                'c': transactions[i - 1]['value'],
                'v': volume
                # 'timestamp': candlestick_timestamp,
                # 'open_time': open_time,
                # 'open_price': open_price,
                # 'high_price': high_price,
                # 'low_price': low_price,
                # 'close_price': transactions[i - 1]['value'],
                # 'volume': volume
            })

            # Next candle
            candlestick_timestamp += interval
            open_time = timestamp
            open_price = value
            high_price = -math.inf
            low_price = math.inf

        high_price = max(high_price, value)
        low_price = min(low_price, value)

    return candlesticks
