#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import json
import sys
import pandas as pd
import os

contract_address = sys.argv[1].lower()

json_data = {}
json_data['index'] = 0
json_data['registrar'] = requests.get(
    "https://api.ethplorer.io/getTokenInfo/"+str(contract_address)+"?apiKey=freekey").json()['name']

ether_price = float(requests.get(
    "https://api.etherscan.io/api?module=stats&action=ethprice&apikey=Z38JUQ2M61Z7TWK5EDB1NK783RRXPYBWRJ").json()['result']['ethusd'])

a = requests.get("https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=" +
                 str(contract_address)+"&vs_currencies=eth").json()

ether_deus_price = float(requests.get("https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=" +
                                      str(contract_address)+"&vs_currencies=eth").json()[contract_address]['eth'])

prices = {'eth': ether_deus_price,
          'usd': float(ether_deus_price) * float(ether_price)}
json_data['price'] = prices

pricedata = requests.get(
    "https://api.coingecko.com/api/v3/coins/deus-finance/market_chart?vs_currency=eth&days=30").json()

df = pd.DataFrame.from_dict(pricedata)
df['Date'] = df['prices'].apply(lambda x: pd.Timestamp(x[0], unit='ms'))
df['Price'] = df['prices'].apply(lambda x: x[1])
df['Price'] = df['Price'].astype('float')

df['VolumeETH'] = df['total_volumes'].apply(lambda x: x[1])
df['VolumeETH'] = df['VolumeETH'].astype('float')

json_data['oneHour'] = (df.iloc[-1]['Price'] / df.iloc[-2]['Price']) - 1
json_data['oneDay'] = (df.iloc[-1]['Price'] / df.iloc[-24]['Price']) - 1
json_data['sevenDays'] = (df.iloc[-1]['Price'] / df.iloc[-(24*7)]['Price']) - 1
json_data['oneDayVolume'] = {'eth': df.iloc[-1]['VolumeETH'],
                             'usd': df.iloc[-1]['VolumeETH']*ether_price}

dir_name = './{}'.format(contract_address)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

with open('./{}/export.json'.format(dir_name), 'w') as fp:
    json.dump(json_data, fp)

# In[ ]:
