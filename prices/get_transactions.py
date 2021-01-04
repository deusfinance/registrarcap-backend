from time import sleep
import pandas as pd
import requests
from datetime import datetime, date
import json
import os

from backend.settings import BASE_DIR

pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.max_colwidth', 400)

apikey_ethplorer = 'EK-2Le3Q-DXBEUjQ-bsqj1'
apikey_etherscan = 'Z38JUQ2M61Z7TWK5EDB1NK783RRXPYBWRJ'


def get_transactions(latest_block: int, latest_timestamp: int, limit: int):
    print("Getting transactions from block {} and timestamp {}".format(latest_block, latest_timestamp))
    end_block = int(
        requests.get(
            "https://api.etherscan.io/api",
            params={
                'module': 'proxy',
                'action': 'eth_blockNumber',
                'apikey': apikey_etherscan
            }
        ).json()['result'],
        0
    )

    if latest_block != end_block:
        transactions = requests.get(
            "http://api.etherscan.io/api",
            params={
                'module': 'account',
                'action': 'txlist',
                'address': contract_address,
                'startblock': latest_block,
                'endblock': end_block,
                'sort': 'asc',
                'apikey': apikey_etherscan,
                'page': 1,
                'offset': limit,
            }
        ).json()['result']

        transactions = list(filter(lambda tx: int(tx['timeStamp']) > latest_timestamp, transactions))

        print("There is {} transactions".format(len(transactions)))

        return transactions


def exportToJSON(dataframe):
    print("Exporting to Json..")
    json_data = {}
    if (contract_address == "0xD77700fC3C78d1Cb3aCb1a9eAC891ff59bC7946D".lower()):
        response_ethplorer = requests.get(
            "https://api.ethplorer.io/getTokenInfo/0x3b62f3820e0b035cc4ad602dece6d796bc325325?apiKey=" + apikey_ethplorer).json()

    json_data['index'] = 0
    json_data['registrar'] = response_ethplorer['name']
    eth_price = dataframe.loc[dataframe['timestamp'] == dataframe['timestamp'].max(), 'price'].item()
    eth_usd_price = float(requests.get(
        "https://api.etherscan.io/api?module=stats&action=ethprice&apikey=Z38JUQ2M61Z7TWK5EDB1NK783RRXPYBWRJ").json()[
                              'result']['ethusd'])
    prices = {'eth': eth_price,
              'usd': float(eth_usd_price) * float(eth_price)}
    json_data['price'] = prices
    json_data['oneHour'] = (eth_price /
                            dataframe[dataframe['date'] > (dataframe['date'].max() - pd.Timedelta(hours=1))].head(1)[
                                'price'].item()) - 1
    json_data['oneDay'] = (eth_price /
                           dataframe[dataframe['date'] > (dataframe['date'].max() - pd.Timedelta(hours=24))].head(1)[
                               'price'].item()) - 1
    json_data['sevenDays'] = (eth_price / dataframe[
        dataframe['date'] > (dataframe['date'].max() - pd.Timedelta(hours=(24 * 7)))].head(1)['price'].item()) - 1
    json_data['oneDayVolume'] = {
        'eth': dataframe[dataframe['date'] > (dataframe['date'].max() - pd.Timedelta(hours=24))]['value'].sum(),
        'usd': dataframe[dataframe['date'] > (dataframe['date'].max() - pd.Timedelta(hours=24))][
                   'value'].sum() * eth_usd_price}

    with open('./' + contract_address + '/export.json', 'w') as fp:
        json.dump(json_data, fp)

    print("Done.\n")


def updateTransactionInfos(transactions):
    print("Getting transactions infos..")

    transactions_infos = []
    transactions_len = len(transactions)
    for i in range(transactions_len):
        transaction = transactions[i]
        print("{} / {}".format(transactions_len, i + 1))

        transaction_info = requests.get(
            "https://api.ethplorer.io/getTxInfo/{}".format(transaction['hash']),
            params={
                'apiKey': apikey_ethplorer
            }
        ).json()

        transactions_infos.append(transaction_info)
        sleep(0.2)

    return transactions_infos


def updateInternalTransactions(transactions):
    print("Getting transactions internal infos..")

    transactions_internal_infos = []

    transactions_len = len(transactions)
    for i in range(transactions_len):
        transaction = transactions[i]
        print("{} / {}".format(transactions_len, i + 1))

        response = requests.get(
            "http://api.etherscan.io/api",
            params={
                "module": "account",
                "action": "txlistinternal",
                "txhash": transaction['hash'],
                "apikey": apikey_etherscan

            }
        ).json()

        if int(response['status']) == 1:
            response['result'][0]['hash'] = transaction['hash']

        transactions_internal_infos.append(response)

    return transactions_internal_infos


def createDataframe(list_transactions, list_transactions_infos, list_internal_transactions):
    print("Creating dataframe..")
    df_transactions = pd.DataFrame.from_dict(list_transactions)

    df_infos = pd.DataFrame.from_dict(list_transactions_infos)
    df_infos['value(token)'] = 0
    df_infos['date'] = ''

    mask = pd.isna(df_infos['operations'])
    df_infos.loc[mask == False, 'value(token)'] = df_infos.loc[mask == False, 'operations'].apply(
        lambda x: float(x[0]['value']) / 1000000000000000000)
    df_infos['date'] = df_infos['timestamp'].apply(lambda x: datetime.fromtimestamp(int(x)))

    df_transactions = df_transactions[
        list(set(df_transactions.columns) - set(df_infos.columns)) + ['hash']
        ].merge(df_infos, how='outer', on='hash').reset_index(drop=False)

    df_transactions = df_transactions.loc[df_transactions.astype(str).drop_duplicates(keep='first').index].reset_index(
        drop=True)

    df_transactions['value'] = df_transactions['value'].astype('float64')
    df_transactions['value(token)'] = df_transactions['value(token)'].astype('float64')

    df_transactions = df_transactions[~df_transactions['operations'].isna()].reset_index(drop=False)

    df_transactions['from'] = df_transactions['operations'].apply(lambda x: x[0]['from'])
    df_transactions['to'] = df_transactions['operations'].apply(lambda x: x[0]['to'])

    df_transactions['hour'] = df_transactions['date'].apply(lambda x: x.replace(minute=0, second=0))
    df_transactions['day'] = df_transactions['date'].apply(lambda x: datetime.date(x))

    df_internal = pd.DataFrame.from_dict(list_internal_transactions)
    df_internal['status'] = df_internal['status'].astype('int')
    df_internal = df_internal[df_internal.status == 1].reset_index(drop=True)
    df_internal = df_internal.dropna().reset_index(drop=True)

    df_internal.loc[:, 'hash'] = df_internal.loc[:, 'result'].apply(lambda x: x[0]['hash'])
    df_internal.loc[:, 'value'] = df_internal.loc[:, 'result'].apply(
        lambda x: float(x[0]['value']) / 1000000000000000000
    )

    df_transactions.loc[
        df_transactions['to'] == '0x0000000000000000000000000000000000000000',
        'value'
    ] = df_transactions.loc[
        df_transactions['to'] == '0x0000000000000000000000000000000000000000']['hash'].map(
        df_internal[
            df_internal['hash'].isin(
                df_transactions.loc[
                    df_transactions['to'] == '0x0000000000000000000000000000000000000000'
                ]['hash'])
        ].set_index('hash')['value']
    )

    df_transactions['price'] = 0
    df_transactions['price'] = df_transactions['price'].astype('int')
    mask = (df_transactions['value(token)'] != 0)
    df_transactions.loc[mask, 'price'] = df_transactions.loc[mask, 'value'] / df_transactions.loc[mask, 'value(token)']
    print("Dataframe created\n------------------------------------------")
    return df_transactions


def exportToArray(dataframe):
    dataframe['transactionType'] = ''
    dataframe.loc[dataframe['from'] == '0x0000000000000000000000000000000000000000', 'transactionType'] = 'buy'
    dataframe.loc[dataframe['to'] == '0x0000000000000000000000000000000000000000', 'transactionType'] = 'sell'

    dataframe = dataframe.groupby(
        ['timestamp', 'value', 'value(token)', 'transactionType', 'hour', 'blockNumber', 'hash']
    )['price'].mean().reset_index()

    return dataframe[['hour', 'blockNumber', 'price', 'hash']].to_numpy()


contract_address = '0xd77700fc3c78d1cb3acb1a9eac891ff59bc7946d'


def get_trades(latest_block, latest_timestamp, limit=100):
    print("Updating Contract: " + contract_address)

    transactions = get_transactions(latest_block, latest_timestamp, limit)
    transactions_infos = updateTransactionInfos(transactions)
    transactions_internal_infos = updateInternalTransactions(transactions)

    if len(transactions) != 0:
        dataframe = createDataframe(transactions, transactions_infos, transactions_internal_infos)
        result = exportToArray(dataframe)

        path = "{}/archived_transactions/{}/{}".format(BASE_DIR, contract_address, date.today())
        if not os.path.exists(path):
            os.makedirs(path)

        with open("{}/{}-transactions.json".format(path, datetime.now().strftime("%H%M")), 'w') as file:
            file.write(json.dumps({
                'latest_block': latest_block,
                'latest_timestamp': latest_timestamp,
                'limit': limit,
                'transactions': transactions,
                'transactions_infos': transactions_infos,
                'transaction_internal_infos': transactions_internal_infos,
            }))

        return result

    return []


if __name__ == '__main__':
    # first_block = 10894792
    # first_timestamp = 1600546741

    first_block = 11492339
    first_timestamp = 1608494400


    prices = get_trades(first_block, first_timestamp, limit=2)
    print(prices)
