import requests
from django.core.management.base import BaseCommand, CommandParser
import json
from pyrogram import Client
from pyrogram.types import Message
from requests import Session, Timeout, TooManyRedirects

from backend.local_settings import TELEGRAM_APP_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, COINMARKETCAP_API_KEY

# Set key here
epApiKey = 0
ecApiKey = 0


class Deus:
    zero_address = "0x0000000000000000000000000000000000000000"

    def __init__(self, token_address="0x3b62f3820e0b035cc4ad602dece6d796bc325325",
                 interact_address="0x0000000000000000000000000000000000000000"):
        self.token_address = str(token_address).lower()
        self.interact_address = str(interact_address).lower()

    def __calc_usd_price_of_token(self, price_eth):
        price_eth_usd = self.get_eth_pice()
        return str(float(price_eth) * float(price_eth_usd))

    def __get_txn_infos(self, txn, deus_amount, buy):
        request_url = "https://api.ethplorer.io/getTxInfo/" + txn + "?apiKey=" + epApiKey
        answere = requests.get(request_url).json()
        # self.get_eth_pice()
        if buy == True:
            eth_value = answere["value"]
            price = float(eth_value) / deus_amount
            return price
        if buy == False:
            request_url = "https://api.etherscan.io/api?module=account&action=txlistinternal&txhash=" + str(
                txn) + "&apikey=" + ecApiKey
            answere = requests.get(request_url).json()
            eth_value = int(answere["result"][0]["value"])
            eth_value = eth_value * (1 / 10 ** 18)
            price = float(eth_value) / deus_amount
            return price

    def __last_price(self, req):
        # found_buy = False
        # found_sell = False
        # buy_price = "Not found"
        # sell_price = "Not found"
        for x in req:
            if x["from"].lower() == self.interact_address:
                print(x["transactionHash"])
                deus_amount = int(x["value"]) * (1 / 10 ** int(x["tokenInfo"]["decimals"]))
                price_eth = self.__get_txn_infos(x["transactionHash"], deus_amount, True)
                return price_eth
            elif x["to"].lower() == self.interact_address:
                print(x["transactionHash"])
                deus_amount = int(x["value"]) * (1 / 10 ** int(x["tokenInfo"]["decimals"]))
                price_eth = self.__get_txn_infos(x["transactionHash"], deus_amount, False)
                return price_eth

    def get_eth_pice(self):
        request_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        answere = requests.get(request_url).json()
        return answere["ethereum"]["usd"]

    def get_price(self, option=None):
        if option == None:
            request_url = "https://api.ethplorer.io/getTokenHistory/" + str(
                self.token_address) + "?apiKey=" + epApiKey + "&type=transfer&limit=1000"
            answere = requests.get(request_url).json()
            price_eth = self.__last_price(answere["operations"])
            price_usd = self.__calc_usd_price_of_token(price_eth)
            return price_eth, price_usd
        elif option == "dea":
            request_url = "https://api.ethplorer.io/getTokenHistory/" + str(
                self.token_address) + "?apiKey=" + epApiKey + "&type=transfer&limit=1000"
            answere = requests.get(request_url).json()
            price_eth = self.__last_price(answere["operations"])
            price_usd = self.__calc_usd_price_of_token(price_eth)
            return price_eth, price_usd

    def get_uniswap_price(self):
        request_url = "https://api.ethplorer.io/getAddressInfo/" + str(self.interact_address) + "?apiKey=" + epApiKey
        answere = requests.get(request_url).json()
        balance_a = float(answere["tokens"][0]["balance"]) * (
                1 / 10 ** float(answere["tokens"][0]["tokenInfo"]["decimals"]))
        balance_b = float(answere["tokens"][1]["balance"]) * (
                1 / 10 ** float(answere["tokens"][1]["tokenInfo"]["decimals"]))
        return (balance_a / balance_b), (balance_b / balance_a)


def get_price(symbol, target):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': target,
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        if data['status']['error_code'] == 0:
            return data['data'][symbol.upper()]['quote'][target.upper()]['price'], False
        else:
            print(data['status'])
            return data['status']['error_message'], True
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


class Command(BaseCommand):
    help = 'runs price bot'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Send errors to chat'
        )

    def handle(self, *args, **options):
        is_debug = options['debug']

        app = Client(
            "bot",
            api_id=TELEGRAM_APP_ID,
            api_hash=TELEGRAM_API_HASH,
            bot_token=TELEGRAM_BOT_TOKEN
        )

        @app.on_message()
        def handler(client, message: Message):
            print("Received '{}'".format(message.text))

            chat_id = message.chat.id

            is_self = message.from_user.is_self
            if is_self:
                print("It's my self")
                return

            pair = message.text.split('/')[1:]

            if len(pair) != 2:
                app.send_message(chat_id, "Send command in this format: /{symbol}/{target}, e.g. /deus/usd")
                return

            result, is_error = get_price(*pair)

            deus = Deus()
            price_eth, price_usd = deus.get_price()
            price_usd = "%.2f" % float(price_usd)
            price_eth = "%.4f" % float(price_eth)

            message = "⚡️This price is based of the last mint/burn of $DEUS⚡️" + "\n💥So fresh from the <a href='deus.finance'>Bounding-Curve</a>💹" + "\n📜<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS Contract</a>📜" + "\n\n⬇️⬇️⬇️⬇️⬇️" + "\nActual price: " + str(
                price_eth) + " <a href='https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'>ETH</a> ($" + str(
                price_usd) + ")" + "\n⬆️⬆️⬆️⬆️⬆️" + "\n\n<a href='https://app.uniswap.org/#/swap?outputCurrency=0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>UNISWAP</a>"

            if is_error and is_debug:
                app.send_message(chat_id, result)
            else:

                app.send_message(chat_id, message)

            app.run()
