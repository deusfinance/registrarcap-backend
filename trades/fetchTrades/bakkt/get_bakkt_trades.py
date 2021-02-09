import datetime
from backend.local_settings import INFURA_KEYS
from trades.fetchTrades.bakkt._GetBakktBuySell import BakktTrades


def get_bakkt_trades(from_block, limit, block_chunk=10000):
    infura_key = INFURA_KEYS[0]
    bakkt_trades = BakktTrades(infura_key)

    from_block = max(from_block, 11647801)

    result = []
    to_block = from_block + block_chunk
    while True:
        print("- Get bakkt trades from block {} to block {}... ".format(from_block, to_block), end=" ")
        try:
            trades = bakkt_trades.getLog(from_block, to_block, limit)
        except ValueError as e:
            if e.args[0]['code'] == -32005:
                print("Rate limit")
            return result
        except Exception as e:
            print("Error:", type(e), e)
            return result + get_bakkt_trades(from_block, limit - len(result), block_chunk // 2)

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
                    'deusAmount': trade['deusAmount'],
                }
            })

        print("{} trades found".format(len(trades)))

        if from_block > bakkt_trades.w3.eth.blockNumber:
            print(" - - End of eth blocks")
            break

        if len(result) >= limit:
            break

        from_block = to_block
        to_block += block_chunk

    return result
