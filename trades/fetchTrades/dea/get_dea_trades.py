import requests
from trades.models import Trade


def get_dea_trades(from_block, limit):
    last_trade = Trade.objects.filter(currency__symbol='dea').order_by('-timestamp').first()
    if last_trade:
        from_timestamp = last_trade.timestamp - 1
    else:
        from_timestamp = 0
    url = "https://dr-collector-api.herokuapp.com/v1/transactions?poolContract=0x92adab6d8dc13dbd9052b291cfc1d07888299d65&from={}&to={}"
    trades = requests.get(url.format(from_timestamp, 99999999999)).json()['results'][:limit * 2]

    result = []
    for trade in trades:
        result.append({
            'hash': None,
            'block': trade['blockNumber'],
            'timestamp': trade['timestamp'],
            'amount': trade['volume'],
            'price': trade['price'],
            'price_type': 'deus',
            'other': {
                'logIndex': trade['logIndex'],
            }
        })

    print("- {} trades found".format(len(trades)))
    return result
