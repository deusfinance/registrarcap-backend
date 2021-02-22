import json
import os
from pprint import pprint
from time import sleep

import requests

from backend.local_settings import FINNHUB_API_KEY
from backend.settings import BASE_DIR
from bot.bot_command_handler import BaseCommandHandler


class UsStocksCommandHandler(BaseCommandHandler):
    symbols = []

    def get_supported_commands(self):
        if self.supported_commands:
            return self.supported_commands

        path = BASE_DIR + '/cache/finnhub_us_symbols.json'
        if os.path.isfile(path):
            with open(path, 'r') as f:
                symbols = json.load(f)
        else:
            response = requests.get(
                'https://finnhub.io/api/v1/stock/symbol?exchange=US&token={}'.format(FINNHUB_API_KEY)
            )
            symbols = response.json()

            with open(path, 'w') as f:
                json.dump(symbols, f)

        self.symbols = symbols
        self.supported_commands = ['/' + s['symbol'] for s in self.symbols]
        return self.supported_commands

    def handle(self, client, message):
        chat_id = message.chat.id
        symbol = self.get_symbol(message.text[1:])
        response = requests.get('https://finnhub.io/api/v1/quote?symbol={}&token={}'.format(
            symbol['symbol'],
            FINNHUB_API_KEY
        ))
        pprint(symbol)

        if response.status_code == 429:
            print("Reached finnhub limit, sleep for 10 seconds.")
            sleep(10)

        data = response.json()
        response_message = (
                symbol['description'] + "\n" +
                "".format() +
                str(data['c'])
        )

        self.app.send_message(
            chat_id,
            response_message,
            disable_web_page_preview=True
        )

    def get_symbol(self, symbol_name):
        return [s for s in self.symbols if s['symbol'].lower() == symbol_name.lower()][0]
