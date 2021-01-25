from django.core.management.base import BaseCommand, CommandParser
import json
from pyrogram import Client
from pyrogram.types import Message
from requests import Session, Timeout, TooManyRedirects

from backend.local_settings import TELEGRAM_APP_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, COINMARKETCAP_API_KEY


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
            print(pair, result, is_error)
            if is_error and is_debug:
                app.send_message(chat_id, result)
            else:
                app.send_message(chat_id, result)

        app.run()
