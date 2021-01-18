import datetime
import json

from backend.settings import BASE_DIR
from trades.fetchTrades.coinbase._get_coinbase_trades import getLog


def get_coinbase_trades(from_block, limit):
    if from_block == 1:
        with open(BASE_DIR + '/trades/fetchTrades/coinbase/_old_trades.json') as old_trades_file:
            trades = json.load(old_trades_file)
    else:
        trades = getLog(from_block, 'latest', limit // 2)

    result = []
    for trade in trades:
        timestamp = datetime.datetime.fromisoformat(trade['timeStamp']).timestamp()
        result.append({
            'hash': trade['transactionHash'],
            'block': trade['blockNumber'],
            'timestamp': timestamp,
            'amount': trade['coinbaseTokenAmount'],
            'price': trade['value'],
            'price_type': 'deus',
            'other': {
                'event': trade['event'],
                'market': trade['market'],
                'userAddress': trade['userAddress'],
                'deus_amount': trade['deusAmount'],
            }
        })

    return result
