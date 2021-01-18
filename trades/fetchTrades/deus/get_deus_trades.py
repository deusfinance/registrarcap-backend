import datetime

from trades.fetchTrades.deus._GetHistory import getLog


def get_deus_trades(from_block, limit):
    result = []
    page = 1
    while True:
        print("- Get deus trades from block {}. (page: {})".format(from_block, page), end=" ")
        out = getLog(from_block, 'latest', page, limit)
        trades = out['trs']
        is_last_page = out['isLastPage']
        for trade in trades:
            timestamp = datetime.datetime.fromisoformat(trade['timeStamp']).timestamp()
            result.append({
                'hash': trade['transactionHash'],
                'block': trade['blockNumber'],
                'timestamp': timestamp,
                'amount': trade['deusAmount'],
                'price': trade['value'],
                'price_type': 'eth',
                'other': {
                    'event': trade['event'],
                    'market': trade['market'],
                    'userAddress': trade['userAddress'],
                    'etherAmount': trade['etherAmount'],
                }
            })

        print("{} trades found".format(len(result)))

        if len(result) >= limit:
            break

        page += 1

        if is_last_page:
            break

    return result
