from time import sleep
import pandas as pd
import requests
from datetime import datetime
import json
import os

pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.max_colwidth', 400)

apikey_ethplorer = 'EK-2Le3Q-DXBEUjQ-bsqj1'
apikey_etherscan = 'Z38JUQ2M61Z7TWK5EDB1NK783RRXPYBWRJ'


def updateTransactions(contract_address, return_new_ones=False):
    if bool_log: print("------------------------------------------")
    if bool_log: print("Updating transactions..")
    latest_block = int(requests.get(
        "https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=" + apikey_etherscan).json()['result'],
                       0)
    if (os.path.isdir('./' + contract_address + '/')):
        if os.path.isfile('./' + contract_address + '/transactions.json'):
            try:
                with open('./' + contract_address + '/transactions.json') as json_file:
                    list_transactions = json.load(json_file)
                    latest_local_timestamp = int(list_transactions[-1]['timeStamp'])
                    latest_local_block = int(list_transactions[-1]['blockNumber'])
            except:
                list_transactions = []
                latest_local_block = 0
                latest_local_timestamp = 0
        else:
            with open('./' + contract_address + '/transactions.json', 'w'):
                pass
            list_transactions = []
            latest_local_block = 0
            latest_local_timestamp = 0
    else:
        os.makedirs('./' + contract_address + '/')
        with open('./' + contract_address + '/transactions.json', 'w'):
            pass
        list_transactions = []
        latest_local_block = 0
        latest_local_timestamp = 0

    if latest_local_block != latest_block:

        request = "http://api.etherscan.io/api?module=account&action=txlist&address=" + str(
            contract_address) + "&startblock=" + str(latest_local_block) + "&endblock=" + str(
            latest_block) + "&sort=asc&apikey=" + str(apikey_etherscan)

        list_api_transactions = requests.get(request).json()['result']
        list_api_transactions = list(
            filter(lambda tx: int(tx['timeStamp']) > latest_local_timestamp, list_api_transactions))

        list_transactions.extend(list_api_transactions)

        if len(list_api_transactions) > 0:
            if bool_log: print("Added " + str(
                len(list_api_transactions)) + " new transactions.\n------------------------------------------")
        else:
            if bool_log: print("Alread up to date.")
        with open('./' + contract_address + '/transactions.json', 'w') as file:
            file.write(json.dumps(list_transactions))

        if return_new_ones:
            return list_api_transactions
        return list_transactions


def exportToJSON(dataframe):
    if bool_log: print("Exporting to Json..")
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

    if bool_log: print("Done.\n")


def updateTransactionInfos(contract_address, return_new_ones=False):
    if bool_log: print("Updating transaction infos..")
    with open('./' + contract_address + '/transactions.json') as json_file:
        list_transactions = json.load(json_file)

    if (os.path.isdir('./' + contract_address + '/')):
        if os.path.isfile('./' + contract_address + '/transaction-infos.json'):
            try:
                with open('./' + contract_address + '/transaction-infos.json') as json_file:
                    list_transactions_infos = json.load(json_file)
                    latest_local_timestamp = None
                    i = -1
                    while not latest_local_timestamp:
                        latest_local_timestamp = list_transactions_infos[i]['timestamp']
                        i -= 1
            except:
                list_transactions_infos = []
                if os.path.isfile('./' + contract_address + '/transactions.json'):
                    latest_local_timestamp = int(list_transactions[0]['timeStamp'])
                else:
                    latest_local_timestamp = 0
        else:
            with open('./' + contract_address + '/transaction-infos.json', 'w'):
                pass
            list_transactions_infos = []
            latest_local_timestamp = 0
    else:
        os.makedirs('./' + contract_address + '/')
        with open('./' + contract_address + '/transaction-infos.json', 'w'):
            pass
        list_transactions_infos = []
        latest_local_timestamp = 0

    list_api_transactionInfos = []
    length_transactions = len(
        list(filter(lambda tx: int(tx['timeStamp']) > int(latest_local_timestamp), list_transactions)))

    if length_transactions > 0:
        abc = 0
        for transaction in list(
                filter(lambda tx: int(tx['timeStamp']) > int(latest_local_timestamp), list_transactions)):
            request = "https://api.ethplorer.io/getTxInfo/" + str(transaction['hash']) + "?apiKey=" + str(
                apikey_ethplorer)
            print(abc)
            abc += 1
            list_api_transactionInfos.append(requests.get(request).json())
            sleep(0.2)

        list_transactions_infos.extend(list_api_transactionInfos)

        with open('./' + contract_address + '/transaction-infos.json', 'w') as file:
            file.write(json.dumps(list_transactions_infos))

        if bool_log: print("Added " + str(
            len(list_api_transactionInfos)) + " new transaction infos.\n------------------------------------------")
    else:
        if bool_log: print("Already up to date.\n------------------------------------------")

    if return_new_ones:
        return list_api_transactionInfos
    return list_transactions_infos


def updateInternalTransactions(list_transactions, return_new_ones=False):
    if bool_log: print("Updating internal transactions..")
    with open('./' + contract_address + '/transactions.json') as json_file:
        list_transactions = json.load(json_file)

    if os.path.isdir('./' + contract_address + '/'):
        if os.path.isfile('./' + contract_address + '/transaction-internal-infos.json'):
            try:
                with open('./' + contract_address + '/transaction-internal-infos.json') as json_file:
                    list_transaction_internal_infos = json.load(json_file)
                    latest_local_timestamp = list_transaction_internal_infos[-1]['result'][0]['timeStamp']
            except:
                list_transaction_internal_infos = []
                if os.path.isfile('./' + contract_address + '/transactions.json'):
                    latest_local_timestamp = int(list_transactions[0]['timeStamp'])
                else:
                    latest_local_timestamp = 0
        else:
            with open('./' + contract_address + '/transaction-internal-infos.json', 'w'):
                pass
            list_transaction_internal_infos = []
            latest_local_timestamp = 0
    else:
        os.makedirs('./' + contract_address + '/')
        with open('./' + contract_address + '/transaction-internal-infos.json', 'w'):
            pass
        list_transaction_internal_infos = []
        latest_local_timestamp = 0

    list_api_transaction_internal_infos = []
    length_transactions = len(
        list(filter(lambda tx: int(tx['timeStamp']) > int(latest_local_timestamp), list_transactions)))

    if length_transactions > 0:
        abc = 0
        for transaction in list(
                filter(lambda tx: int(tx['timeStamp']) > int(latest_local_timestamp), list_transactions)):
            print(abc)
            abc += 1
            request = "http://api.etherscan.io/api?module=account&action=txlistinternal&txhash=" + str(
                transaction['hash']) + "&apikey=" + apikey_etherscan
            response = requests.get(request).json()

            if int(response['status']) == 1:
                response['result'][0]['hash'] = transaction['hash']

            list_api_transaction_internal_infos.append(response)

        list_transaction_internal_infos.extend(list_api_transaction_internal_infos)

        with open('./' + contract_address + '/transaction-internal-infos.json', 'w') as file:
            file.write(json.dumps(list_transaction_internal_infos))

        if bool_log: print("Added " + str(
            length_transactions) + " new internal transactions.\n------------------------------------------")
    else:
        if bool_log: print("Already up to date.\n------------------------------------------")

    if return_new_ones:
        return list_api_transaction_internal_infos
    return list_transaction_internal_infos


def createDataframe(list_transactions, list_transactions_infos, list_internal_transactions, *args, **kwargs):
    if bool_log: print("Creating dataframe..")
    df_transactions = pd.DataFrame.from_dict(list_transactions[1:])

    df_infos = pd.DataFrame.from_dict(list_transactions_infos[1:])
    df_infos['value(token)'] = 0
    df_infos['date'] = ''

    mask = pd.isna(df_infos['operations'])
    df_infos.loc[mask == False, 'value(token)'] = df_infos.loc[mask == False, 'operations'].apply(
        lambda x: float(x[0]['value']) / 1000000000000000000)
    df_infos['date'] = df_infos['timestamp'].apply(lambda x: datetime.fromtimestamp(int(x)))

    df_transactions = df_transactions[list(set(df_transactions.columns) - set(df_infos.columns)) + ['hash']].merge(
        df_infos, how='outer', on='hash').reset_index(drop=True)

    df_transactions = df_transactions.loc[df_transactions.astype(str).drop_duplicates(keep='first').index].reset_index(
        drop=True)

    df_transactions['value'] = df_transactions['value'].astype('float64')
    df_transactions['value(token)'] = df_transactions['value(token)'].astype('float64')

    df_transactions = df_transactions[~df_transactions['operations'].isna()].reset_index(drop=True)

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
        lambda x: float(x[0]['value']) / 1000000000000000000)
    df_transactions.loc[df_transactions['to'] == '0x0000000000000000000000000000000000000000', 'value'] = \
        df_transactions.loc[df_transactions['to'] == '0x0000000000000000000000000000000000000000']['hash'].map(
            df_internal[df_internal['hash'].isin(
                df_transactions.loc[df_transactions['to'] == '0x0000000000000000000000000000000000000000'][
                    'hash'])].set_index('hash')['value'])

    df_transactions['price'] = 0
    df_transactions['price'] = df_transactions['price'].astype('int')
    mask = (df_transactions['value(token)'] != 0)
    df_transactions.loc[mask, 'price'] = df_transactions.loc[mask, 'value'] / df_transactions.loc[mask, 'value(token)']
    if bool_log: print("Dataframe created\n------------------------------------------")
    return df_transactions


def plot(dataframe):
    if bool_log: print("Creating plot..\n")
    df_plot = dataframe.groupby('hour')['price'].mean()
    df_plot.plot(figsize=(5, 5));


# def exportToJSON(dataframe):


def exportToCSV(dataframe):
    dataframe['transactionType'] = ''
    dataframe.loc[dataframe['from'] == '0x0000000000000000000000000000000000000000', 'transactionType'] = 'buy'
    dataframe.loc[dataframe['to'] == '0x0000000000000000000000000000000000000000', 'transactionType'] = 'sell'

    dataframe[['value', 'value(token)', 'transactionType']].to_csv('./' + contract_address + '/highcharts-export.csv',
                                                                   index=False)

    # return dataframe[['value', 'value(token)', 'transactionType']]


def exportToArray(dataframe):
    dataframe['transactionType'] = ''
    dataframe.loc[dataframe['from'] == '0x0000000000000000000000000000000000000000', 'transactionType'] = 'buy'
    dataframe.loc[dataframe['to'] == '0x0000000000000000000000000000000000000000', 'transactionType'] = 'sell'

    dataframe = dataframe.groupby(['timestamp', 'value', 'value(token)', 'transactionType', 'hour'])[
        'price'].mean().reset_index()

    return dataframe[['hour',  # 'value', 'value(token)', 'transactionType',
                      'price']].to_numpy()

    print(dataframe[['hour',  # 'value', 'value(token)', 'transactionType',
                     'price']].to_numpy())


contract_address = '0xd77700fc3c78d1cb3acb1a9eac891ff59bc7946d'
bool_log = True


def update_transactions(return_new_ones=False):
    if bool_log: print("Updating Contract: " + contract_address)

    list_transactions = updateTransactions(contract_address, return_new_ones)
    list_transactions_infos = updateTransactionInfos(contract_address, return_new_ones)

    list_internal_transactions = updateInternalTransactions(contract_address, return_new_ones)

    dataframe = createDataframe(list_transactions, list_transactions_infos, list_internal_transactions, internal=True)

    # exportToJSON(dataframe)
    return exportToArray(dataframe)


if __name__ == '__main__':
    prices = update_transactions()
    print(prices)
