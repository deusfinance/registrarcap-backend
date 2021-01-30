import datetime

from trades.fetchTrades.deus._GetBuySell import get_history, w3


def get_deus_trades(from_block, limit, block_chunk=10000):
    result = []
    to_block = from_block + block_chunk
    while True:
        print("- Get deus trades from block {} to block {}... ".format(from_block, to_block), end=" ")
        try:
            trades = get_history(from_block, to_block, limit)
        except Exception as e:
            print(e)
            return result + get_deus_trades(from_block, limit - len(result), block_chunk // 2)

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

        print("{} trades found".format(len(trades)))

        if len(result) >= limit or from_block > w3.eth.blockNumber:
            break

        from_block = to_block
        to_block += block_chunk

    return result
