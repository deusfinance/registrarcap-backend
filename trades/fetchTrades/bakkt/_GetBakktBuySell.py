from web3 import Web3
from datetime import datetime
import pytz


class BakktTrades:

    def __init__(self, infura_key):

        self.w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/{}'.format(infura_key)))

    def eventListener(self, contract, event, fromBlock, toBlock, limit, market):

        event_filter = contract.events[event].createFilter(fromBlock=fromBlock, toBlock=toBlock)
        events = event_filter.get_all_entries()
        if limit != 'all':
            events = events[:limit]
        out = []
        for event in events:
            info = {}

            # print(event)
            try:
                timeStamp = self.w3.eth.getBlock(event['blockNumber'])['timestamp']
                timeStamp = datetime.fromtimestamp(timeStamp).astimezone(pytz.utc)
            except Exception as e:
                print(e)
                timeStamp = 'Not Found'
            trans = self.w3.eth.getTransaction(event['transactionHash'])

            info['coinbaseTokenAmount'] = event['args']['coinbaseTokenAmount'] / 10 ** 18
            info['deusAmount'] = event['args']['deusAmount'] / 10 ** 18
            # info['feeAmount'] = event['args']['feeAmount'] / 10 ** 18
            info['value'] = info['deusAmount'] / info['coinbaseTokenAmount']
            info['timeStamp'] = str(timeStamp)
            info['transactionHash'] = event['transactionHash'].hex()
            info['userAddress'] = event['args']['user']
            info['event'] = event['event']
            info['market'] = 'bakkt ' + market
            info['blockNumber'] = event['blockNumber']

            # print(trans)

            out.append(info)

        return out

    def getLog(self, fromBlock, toBlock, limit):

        bakkt_amm_addr = '0x55FE6eD0617B9dca98141656B3356423bBfA9458'
        bakkt_amm_abi = '[ { "inputs": [ { "internalType": "address", "name": "_deusToken", "type": "address" }, { "internalType": "address", "name": "_coinbaseToken", "type": "address" } ], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "user", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "coinbaseTokenAmount", "type": "uint256" }, { "indexed": false, "internalType": "uint256", "name": "deusAmount", "type": "uint256" }, { "indexed": false, "internalType": "uint256", "name": "feeAmount", "type": "uint256" } ], "name": "Buy", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "previousOwner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "OwnershipTransferred", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "user", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "deusAmount", "type": "uint256" }, { "indexed": false, "internalType": "uint256", "name": "coinbaseTokenAmount", "type": "uint256" }, { "indexed": false, "internalType": "uint256", "name": "feeAmount", "type": "uint256" } ], "name": "Sell", "type": "event" }, { "inputs": [], "name": "IPOFailed", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "coinbaseTokenAmount", "type": "uint256" }, { "internalType": "uint256", "name": "deusAmount", "type": "uint256" } ], "name": "buy", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "user", "type": "address" }, { "internalType": "uint256", "name": "_coinbaseAmount", "type": "uint256" }, { "internalType": "uint256", "name": "_deusAmount", "type": "uint256" } ], "name": "buyFor", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "deusAmount", "type": "uint256" } ], "name": "calculatePurchaseReturn", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" }, { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "coinbaseAmount", "type": "uint256" } ], "name": "calculateSaleReturn", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" }, { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "coinbaseToken", "outputs": [ { "internalType": "contract CoinbaseToken", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "cw", "outputs": [ { "internalType": "uint32", "name": "", "type": "uint32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoShare", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoShareScale", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoWallet", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "deusToken", "outputs": [ { "internalType": "contract DEUSToken", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "firstReserve", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "firstSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_firstReserve", "type": "uint256" }, { "internalType": "uint256", "name": "_firstSupply", "type": "uint256" } ], "name": "init", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "reserve", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "reserveShiftAmount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "scale", "outputs": [ { "internalType": "uint32", "name": "", "type": "uint32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "coinbaseTokenAmount", "type": "uint256" }, { "internalType": "uint256", "name": "deusAmount", "type": "uint256" } ], "name": "sell", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "user", "type": "address" }, { "internalType": "uint256", "name": "coinbaseAmount", "type": "uint256" }, { "internalType": "uint256", "name": "_deusAmount", "type": "uint256" } ], "name": "sellFor", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_daoShare", "type": "uint256" } ], "name": "setDaoShare", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_daoWallet", "type": "address" } ], "name": "setDaoWallet", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bool", "name": "_IPOFailed", "type": "bool" } ], "name": "setIPOFailed", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "version", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "address", "name": "to", "type": "address" } ], "name": "withdrawDEUS", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "stateMutability": "payable", "type": "receive" } ]'
        log = []

        bakkt_amm = self.w3.eth.contract(address=bakkt_amm_addr, abi=bakkt_amm_abi)

        log += self.eventListener(bakkt_amm, 'Buy', fromBlock, toBlock, limit, 'AMM')
        log += self.eventListener(bakkt_amm, 'Sell', fromBlock, toBlock, limit, 'AMM')

        return log

    # log = getLog(1, 'latest', 'all')
    # print(len(log))
    # print(log)

    # with open('spsLog.json', 'w') as outFile:
    #     json.dump(log, outFile)
