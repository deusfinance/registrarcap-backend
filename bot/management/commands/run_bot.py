import requests
from django.core.management.base import BaseCommand, CommandParser
import json
from pyrogram import Client
from pyrogram.types import Message
from requests import Session, Timeout, TooManyRedirects

from backend.local_settings import TELEGRAM_APP_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, COINMARKETCAP_API_KEY
from trades.models import Currency


def get_uniswap_price():
    epApiKey = 'freekey'
    interact_address = "0x83973dcaa04A6786ecC0628cc494a089c1AEe947"
    request_url = "https://api.ethplorer.io/getAddressInfo/" + str(interact_address) + "?apiKey=" + epApiKey
    res = requests.get(request_url).json()
    balance_a = float(res["tokens"][0]["balance"]) * (
            1 / 10 ** float(res["tokens"][0]["tokenInfo"]["decimals"]))
    balance_b = float(res["tokens"][1]["balance"]) * (
            1 / 10 ** float(res["tokens"][1]["tokenInfo"]["decimals"]))
    return (balance_a / balance_b), (balance_b / balance_a)


def get_eth_pice():
    request_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    answere = requests.get(request_url).json()
    return answere["ethereum"]["usd"]


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

        currencies = Currency.objects.all()

        @app.on_message()
        def handler(client, message: Message):
            print("Received '{}'".format(message.text))

            chat_id = message.chat.id

            is_self = message.from_user.is_self
            if is_self:
                print("It's my self")
                return

            pair = message.text[1:]
            print("Requested {}".format(pair))

            for currency in currencies:
                if pair.find(currency.symbol) == 0:
                    target_currency_symbol = pair[len(currency.symbol):]
                    last_trade = currency.trades.latest('timestamp')

                    if currency.symbol == 'deus':
                        message = (
                                "⚡️This price is based of the last mint/burn of $DEUS⚡️"
                                "\n💥So fresh from the <a href='deus.finance'>Bounding-Curve</a>💹"
                                "\n📜<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS Contract</a>📜"
                                "\n\n⬇️⬇️⬇️⬇️⬇️"
                                "\nActual price: " + str(round(last_trade.eth_price, 4)) +
                                " <a href='https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'>ETH</a> ($" +
                                str(round(last_trade.usd_price, 2)) +
                                ")" "\n⬆️⬆️⬆️⬆️⬆️"
                                "\n\n<a href='https://app.uniswap.org/#/swap?outputCurrency=0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>UNISWAP</a>"
                        )
                    elif currency.symbol == 'dea':
                        if pair == 'deausdc':
                            dea_per_usdc, usdc_per_dea = get_uniswap_price()
                            price_eth = get_eth_pice()
                            eth_per_dea = "%.4f" % (float(usdc_per_dea) / float(price_eth))
                            usdc_per_dea = "%.2f" % float(usdc_per_dea)

                            message = (
                                    "\n📜<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA Contract</a>📜"
                                    "\nKeep in mind this is the "
                                    "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>"
                                    " price (not $)."
                                    "\nThis price is from the "
                                    "<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA</a>"
                                    " / "
                                    "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>"
                                    " pool."
                                    "\n\n⬇️⬇️⬇️⬇️⬇️"
                                    "\nActual price: {} ".format(eth_per_dea) +
                                    "<a href='https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'>ETH</a>"
                                    "\n({} ".format(usdc_per_dea) +
                                    "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>)"
                                    "\n⬆️⬆️⬆️⬆️⬆️"
                                    "\n\n<a href='https://app.uniswap.org/#/swap?outputCurrency=0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>UNISWAP</a>"

                            )
                            app.send_message(
                                chat_id,
                                message,
                                disable_web_page_preview=True
                            )

                        message = (
                                "\n📜<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA Contract</a>📜"
                                "\nKeep in mind this is the $ / "
                                "<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS</a>"
                                " price (not "
                                "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>)."
                                "\nThis price is from the "
                                "<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA</a>"
                                " / "
                                "<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS</a>"
                                " pool."
                                "\n\n⬇️⬇️⬇️⬇️⬇️"
                                "\nActual price: {} ".format(round(last_trade.deus_price, 4)) +
                                "<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS</a>"
                                "\n(${})".format(round(last_trade.usd_price, 2)) +
                                "\n⬆️⬆️⬆️⬆️⬆️"
                                "\n\n<a href='https://app.uniswap.org/#/swap?outputCurrency=0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>UNISWAP</a>"

                        )
                    else:
                        message = getattr(
                            last_trade,
                            "{}_price".format(target_currency_symbol),
                            "Target currency is not supported yet"
                        )

                    app.send_message(
                        chat_id,
                        message,
                        disable_web_page_preview=True
                    )

            return

        app.run()
