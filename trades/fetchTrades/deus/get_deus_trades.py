import datetime

from backend.local_settings import INFURA_KEYS
from trades.fetchTrades.deus._deus_trades import DeusTrades


def get_deus_trades(from_block, limit, block_chunk=10000):

    if block_chunk <= 100:
        print("- - reached block chunk 100...")
        return []

    infura_key = INFURA_KEYS[0]
    deus_trades = DeusTrades(infura_key)

    result = []
    to_block = from_block + block_chunk
    while True:
        print("- Get deus trades from block {} to block {}... ".format(from_block, to_block), end=" ")
        try:
            trades = deus_trades.get_history(from_block, to_block, limit)
        except ValueError as e:
            if e.args[0]['code'] == -32005:
                print("Rate limit")
            return result
        except Exception as e:
            print("Error:", type(e), e)
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

        if from_block > deus_trades.w3.eth.blockNumber:
            print(" - - End of eth blocks")
            break

        if len(result) >= limit:
            break

        from_block = to_block
        to_block += block_chunk

    return result
