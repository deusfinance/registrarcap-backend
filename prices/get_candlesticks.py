import json
import math
from pprint import pprint

from prices.get_transactions import update_transactions


def get_candlesticks(contract_address, interval: int = 60):
    """
    :param contract_address: Ex 0x3b...
    :param interval: candles interval in seconds (it's 60 seconds = 1 minute by default)
    :return: []
    """

    update_transactions()

    transactions = []
    with open('{}/transactions.json'.format(contract_address), 'r') as transactions_file:
        for transaction in json.load(transactions_file):
            transactions.append({
                'timestamp': int(transaction['timeStamp']),
                'value': int(transaction['value']),
            })
        transactions.sort(key=lambda o: o['timestamp'])

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
                'timestamp': candlestick_timestamp,
                'open_time': open_time,
                'open_price': open_price,
                'high_price': high_price,
                'low_price': low_price,
                'close_price': transactions[i - 1]['value'],
                'volume': volume
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


pprint(get_candlesticks('0x3b62f3820e0b035cc4ad602dece6d796bc325325', 60 * 60 * 24))
