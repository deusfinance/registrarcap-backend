from pprint import pprint

from web3 import Web3
from datetime import datetime
from requests import get
import json
import pytz

w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/fe345b94534845028bcd5978e0172508'))
amm_addr = w3.toChecksumAddress('0xd77700fc3c78d1cb3acb1a9eac891ff59bc7946d')
amm_abi = '[ { "inputs": [ { "internalType": "address", "name": "_deusToken", "type": "address" } ], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "previousOwner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "OwnershipTransferred", "type": "event" }, { "inputs": [ { "internalType": "uint256", "name": "_tokenAmount", "type": "uint256" } ], "name": "buy", "outputs": [], "stateMutability": "payable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "etherAmount", "type": "uint256" } ], "name": "calculatePurchaseReturn", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenAmount", "type": "uint256" } ], "name": "calculateSaleReturn", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "cw", "outputs": [ { "internalType": "uint32", "name": "", "type": "uint32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoShare", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoShareScale", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoTargetBalance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoWallet", "outputs": [ { "internalType": "address payable", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "deusToken", "outputs": [ { "internalType": "contract DEUSToken", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "firstReserve", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "firstSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_firstReserve", "type": "uint256" }, { "internalType": "uint256", "name": "_firstSupply", "type": "uint256" } ], "name": "init", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "maxDaoShare", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "dest", "type": "address" } ], "name": "payments", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "reserve", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "reserveShiftAmount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "scale", "outputs": [ { "internalType": "uint32", "name": "", "type": "uint32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenAmount", "type": "uint256" }, { "internalType": "uint256", "name": "_etherAmount", "type": "uint256" } ], "name": "sell", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_maxDaoShare", "type": "uint256" }, { "internalType": "uint256", "name": "_daoTargetBalance", "type": "uint256" } ], "name": "setDaoShare", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address payable", "name": "_daoWallet", "type": "address" } ], "name": "setDaoWallet", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "version", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "withdraw", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address payable", "name": "payee", "type": "address" } ], "name": "withdrawPayments", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "stateMutability": "payable", "type": "receive" } ]'

sps_addr = '0xc2fb644cd18325c58889cf8bb0573e4a8774bcd2'
sps_abi = '[ { "inputs": [ { "internalType": "uint256", "name": "_endBlock", "type": "uint256" }, { "internalType": "address", "name": "_deusToken", "type": "address" }, { "internalType": "address", "name": "_pair", "type": "address" } ], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "previousOwner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "OwnershipTransferred", "type": "event" }, { "inputs": [], "name": "buy", "outputs": [], "stateMutability": "payable", "type": "function" }, { "inputs": [], "name": "deusToken", "outputs": [ { "internalType": "contract DEUSToken", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "endBlock", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "pair", "outputs": [ { "internalType": "contract IUniswapV2Pair", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "price", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_endBlock", "type": "uint256" } ], "name": "setEndBlock", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address payable", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "withdraw", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]'


def getLog(fromBlock, toBlock, page, offset):
    amm = w3.eth.contract(address=amm_addr, abi=amm_abi)

    get_trs_url = f'https://api.etherscan.io/api?module=account&action=txlist&address=0xD77700fC3C78d1Cb3aCb1a9eAC891ff59bC7946D&startblock={fromBlock}&endblock={toBlock}&sort=asc&apikey=9Z15YVP4D56SE3W6813MKG31X46V2IN6I8&page={page}&offset={offset}'

    trs = get(get_trs_url).json()['result']
    # print(trs)

    get_internal_trs_url = f'https://api.etherscan.io/api?module=account&action=txlistinternal&startblock={fromBlock}&endblock={toBlock}&page={page}&offset={offset}&sort=asc&apikey=9Z15YVP4D56SE3W6813MKG31X46V2IN6I8&address=0xD77700fC3C78d1Cb3aCb1a9eAC891ff59bC7946D'
    internal_trs = get(get_internal_trs_url).json()['result']

    buy = str(amm.get_function_by_name('buy'))
    sell = str(amm.get_function_by_name('sell'))

    out = {
        'isLastPage': True if len(trs) < offset else False,
        'trs': []
    }

    for tr in trs:
        try:
            info = {}
            inputData = amm.decode_function_input(tr['input'])
            if tr['isError'] == '1':
                continue
            if str(inputData[0]) == buy:
                # print('buy')
                # print(tr)
                fromHex = '0x000000000000000000000000' + tr['from'][2:]
                get_token_trsfr_data_url = f"https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock={tr['blockNumber']}&toBlock={tr['blockNumber']}&address=0x3b62f3820e0b035cc4ad602dece6d796bc325325&topic0=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef&topic0_1_opr=and&topic1=0x0000000000000000000000000000000000000000000000000000000000000000&topic1_2_opr=and&topic2={fromHex}&apikey=9Z15YVP4D56SE3W6813MKG31X46V2IN6I8"
                tk_tr_data = get(get_token_trsfr_data_url).json()['result']
                # print(tk_tr_data)
                info['deusAmount'] = int(tk_tr_data[0]['data'], 16) / 10 ** 18
                info['etherAmount'] = int(tr['value']) / 10 ** 18
                info['value'] = info['etherAmount'] / info['deusAmount']
                info['event'] = 'buy'
            elif str(inputData[0]) == sell:
                # print('sell')
                get_internal_trs_url = f'https://api.etherscan.io/api?module=account&action=txlistinternal&apikey=9Z15YVP4D56SE3W6813MKG31X46V2IN6I8&txhash={tr["hash"]}'

                # internal_trs = get(get_internal_trs_url).json()['result']
                # info['etherAmount'] = int(internal_trs[0]['value']) / 10 ** 18

                internal_tr = [trx for trx in internal_trs if tr['hash'] == trx['hash']]
                info['etherAmount'] = int(internal_tr[0]['value']) / 10 ** 18

                info['deusAmount'] = int(inputData[1]['tokenAmount']) / 10 ** 18
                info['value'] = info['etherAmount'] / info['deusAmount']
                info['event'] = 'sell'
            else:
                continue
            timeStamp = w3.eth.getBlock(int(tr['blockNumber']))['timestamp']
            timeStamp = datetime.fromtimestamp(timeStamp).astimezone(pytz.utc)
            info['timeStamp'] = str(timeStamp)
            info['transactionHash'] = tr['hash']
            info['userAddress'] = tr['from']
            info['market'] = 'DeusAMM'
            info['blockNumber'] = tr['blockNumber']
            out['trs'].append(info)

        except Exception as e:
            # print(e)
            pass
    return out


if __name__ == '__main__':
    log = getLog(10936349, 'latest', 1, 10)
    pprint(log)
