from web3 import Web3
from datetime import datetime
import pytz

w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/fe345b94534845028bcd5978e0172508'))
amm_addr = w3.toChecksumAddress('0xd77700fc3c78d1cb3acb1a9eac891ff59bc7946d')
amm_abi = '[ { "inputs": [ { "internalType": "address", "name": "_deusToken", "type": "address" } ], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "previousOwner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "OwnershipTransferred", "type": "event" }, { "inputs": [ { "internalType": "uint256", "name": "_tokenAmount", "type": "uint256" } ], "name": "buy", "outputs": [], "stateMutability": "payable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "etherAmount", "type": "uint256" } ], "name": "calculatePurchaseReturn", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenAmount", "type": "uint256" } ], "name": "calculateSaleReturn", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "cw", "outputs": [ { "internalType": "uint32", "name": "", "type": "uint32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoShare", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoShareScale", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoTargetBalance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "daoWallet", "outputs": [ { "internalType": "address payable", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "deusToken", "outputs": [ { "internalType": "contract DEUSToken", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "firstReserve", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "firstSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_firstReserve", "type": "uint256" }, { "internalType": "uint256", "name": "_firstSupply", "type": "uint256" } ], "name": "init", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "maxDaoShare", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "dest", "type": "address" } ], "name": "payments", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "reserve", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "reserveShiftAmount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "scale", "outputs": [ { "internalType": "uint32", "name": "", "type": "uint32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenAmount", "type": "uint256" }, { "internalType": "uint256", "name": "_etherAmount", "type": "uint256" } ], "name": "sell", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "_maxDaoShare", "type": "uint256" }, { "internalType": "uint256", "name": "_daoTargetBalance", "type": "uint256" } ], "name": "setDaoShare", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address payable", "name": "_daoWallet", "type": "address" } ], "name": "setDaoWallet", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "version", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "withdraw", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address payable", "name": "payee", "type": "address" } ], "name": "withdrawPayments", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "stateMutability": "payable", "type": "receive" } ]'

amm = w3.eth.contract(address=amm_addr, abi=amm_abi)


# deus = w3.eth.contract(address=w3.toChecksumAddress('0x3b62f3820e0b035cc4ad602dece6d796bc325325'), abi='[{ "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [{ "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "spender", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" }], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [{ "indexed": true, "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "indexed": true, "internalType": "bytes32", "name": "previousAdminRole", "type": "bytes32" }, { "indexed": true, "internalType": "bytes32", "name": "newAdminRole", "type": "bytes32" }], "name": "RoleAdminChanged", "type": "event" }, { "anonymous": false, "inputs": [{ "indexed": true, "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "indexed": true, "internalType": "address", "name": "account", "type": "address" }, { "indexed": true, "internalType": "address", "name": "sender", "type": "address" }], "name": "RoleGranted", "type": "event" }, { "anonymous": false, "inputs": [{ "indexed": true, "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "indexed": true, "internalType": "address", "name": "account", "type": "address" }, { "indexed": true, "internalType": "address", "name": "sender", "type": "address" }], "name": "RoleRevoked", "type": "event" }, { "anonymous": false, "inputs": [{ "indexed": true, "internalType": "address", "name": "from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "to", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" }], "name": "Transfer", "type": "event" }, { "inputs": [], "name": "BURNER_ROLE", "outputs": [{ "internalType": "bytes32", "name": "", "type": "bytes32" }], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "CURRENT_POINT_INDEX_SETTER_ROLE", "outputs": [{ "internalType": "bytes32", "name": "", "type": "bytes32" }], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "DEFAULT_ADMIN_ROLE", "outputs": [{ "internalType": "bytes32", "name": "", "type": "bytes32" }], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "MINTER_ROLE", "outputs": [{ "internalType": "bytes32", "name": "", "type": "bytes32" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "owner", "type": "address" }, { "internalType": "address", "name": "spender", "type": "address" }], "name": "allowance", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "spender", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }], "name": "approve", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "account", "type": "address" }], "name": "balanceOf", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "from", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }], "name": "burn", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "currentPointIndex", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "decimals", "outputs": [{ "internalType": "uint8", "name": "", "type": "uint8" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "spender", "type": "address" }, { "internalType": "uint256", "name": "subtractedValue", "type": "uint256" }], "name": "decreaseAllowance", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "bytes32", "name": "role", "type": "bytes32" }], "name": "getRoleAdmin", "outputs": [{ "internalType": "bytes32", "name": "", "type": "bytes32" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "uint256", "name": "index", "type": "uint256" }], "name": "getRoleMember", "outputs": [{ "internalType": "address", "name": "", "type": "address" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "bytes32", "name": "role", "type": "bytes32" }], "name": "getRoleMemberCount", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" }], "name": "grantRole", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" }], "name": "hasRole", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "spender", "type": "address" }, { "internalType": "uint256", "name": "addedValue", "type": "uint256" }], "name": "increaseAllowance", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }], "name": "mint", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "name", "outputs": [{ "internalType": "string", "name": "", "type": "string" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" }], "name": "renounceRole", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" }], "name": "revokeRole", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "uint256", "name": "_currentPointIndex", "type": "uint256" }], "name": "setCurrentPointIndex", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "symbol", "outputs": [{ "internalType": "string", "name": "", "type": "string" }], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "totalSupply", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }], "name": "transfer", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }], "name": "transferFrom", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "nonpayable", "type": "function" }]')

def get_transactions(fromBlock, toBlock, limit):
    deus_buy_filter = w3.eth.filter({
        'fromBlock': fromBlock,
        'toBlock': toBlock,
        'address': w3.toChecksumAddress('0x3b62f3820e0b035cc4ad602dece6d796bc325325'),
        'topics': [
            '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
            '0x0000000000000000000000000000000000000000000000000000000000000000'
        ]
    })

    buy_trs = deus_buy_filter.get_all_entries()[:limit]

    deus_sell_filter = w3.eth.filter({
        'fromBlock': fromBlock,
        'toBlock': toBlock,
        'address': w3.toChecksumAddress('0x3b62f3820e0b035cc4ad602dece6d796bc325325'),
        'topics': [
            '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
            None,
            '0x0000000000000000000000000000000000000000000000000000000000000000'
        ]
    })

    sell_trs = deus_sell_filter.get_all_entries()[:limit]

    return buy_trs + sell_trs


def export_old_tr_data(old_trs):
    buy = str(amm.get_function_by_name('buy'))
    sell = str(amm.get_function_by_name('sell'))
    new_trs = []
    out = []
    for log in old_trs:
        info = {}
        tr = w3.eth.getTransaction(log['transactionHash'])
        try:
            inputData = amm.decode_function_input(tr['input'])
        except Exception as e:
            new_trs.append(log)
            continue
        if str(inputData[0]) == buy:
            info['deusAmount'] = int(log['data'], 16) / 10 ** 18
            info['etherAmount'] = int(tr['value']) / 10 ** 18
            info['value'] = info['etherAmount'] / info['deusAmount']
            info['event'] = 'buy'
        elif str(inputData[0]) == sell:
            try:
                tr_rcpt = w3.eth.getTransactionReceipt(log['transactionHash'])
                info['etherAmount'] = int(tr_rcpt['logs'][0]['data'], 16) / 10 ** 18
                info['deusAmount'] = int(inputData[1]['tokenAmount']) / 10 ** 18
                info['value'] = info['etherAmount'] / info['deusAmount']
                info['event'] = 'sell'
            except:
                continue
                pass
                # print(log['transactionHash'].hex())
        else:
            continue
        timeStamp = w3.eth.getBlock(int(tr['blockNumber']))['timestamp']
        timeStamp = datetime.fromtimestamp(timeStamp).astimezone(pytz.utc)
        info['timeStamp'] = str(timeStamp)
        info['transactionHash'] = log['transactionHash'].hex()
        info['userAddress'] = tr['from']
        info['market'] = 'DeusAMM'
        info['blockNumber'] = tr['blockNumber']
        out.append(info)
    return out, new_trs


def export_new_tr_data(new_trs):
    out = []
    for log in new_trs:
        info = {}
        tr = w3.eth.getTransaction(log['transactionHash'])
        if log['topics'][2].hex() == '0x0000000000000000000000000000000000000000000000000000000000000000':
            # sell
            tr_rcpt = w3.eth.getTransactionReceipt(log['transactionHash'])
            approval_log = [lg for lg in tr_rcpt['logs'] if
                            lg['address'] == '0x056CbC3D1926B50b493Dc2B92d3CcB2B79f65BcA']
            info['etherAmount'] = int(approval_log[0]['data'], 16) / 10 ** 18
            info['deusAmount'] = int(log['data'], 16) / 10 ** 18
            info['value'] = info['etherAmount'] / info['deusAmount']
            info['event'] = 'sell'

        elif log['topics'][1].hex() == '0x0000000000000000000000000000000000000000000000000000000000000000' \
                and tr['value'] != 0:
            # buy
            info['deusAmount'] = int(log['data'], 16) / 10 ** 18
            info['etherAmount'] = int(tr['value']) / 10 ** 18
            info['value'] = info['etherAmount'] / info['deusAmount']
            info['event'] = 'buy'
        else:
            # print('Unknown Tranaction')
            # print(log['transactionHash'].hex())
            continue
        timeStamp = w3.eth.getBlock(int(tr['blockNumber']))['timestamp']
        timeStamp = datetime.fromtimestamp(timeStamp).astimezone(pytz.utc)
        info['timeStamp'] = str(timeStamp)
        info['transactionHash'] = log['transactionHash'].hex()
        info['userAddress'] = tr['from']
        info['market'] = 'DeusAMM'
        info['blockNumber'] = tr['blockNumber']
        out.append(info)
    return out


def get_history(fromBlock, toBlock, limit):
    trs = get_transactions(fromBlock, toBlock, limit)
    old_method_trs, new_trs_log = export_old_tr_data(trs)
    new_method_trs = [] if new_trs_log == [] else export_new_tr_data(new_trs_log)
    return old_method_trs + new_method_trs


if __name__ == '__main__':
    fromBlock = 11493518
    toBlock = 11503518
    limit = 100

    # fromBlock = 11584723
    # toBlock = "latest"

    trs = get_history(fromBlock, toBlock, limit)
    print(trs)

    # with open('spsLog.txt', 'w') as outFile:
    #     for tr in trs:
    #         # print(tr['event'])
    #         # print(tr['transactionHash'])
    #         outFile.write(tr['event'] + '\n')
    #         outFile.write(tr['transactionHash'] + '\n')
