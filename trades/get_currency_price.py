import requests


def get_currency_price(symbol):
    url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=BTC,ETH,USD".format(symbol)
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    print(get_currency_price('ETH'))
    print(get_currency_price('BTC'))
