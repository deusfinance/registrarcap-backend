from django.core.management.base import BaseCommand
from pyrogram import Client
from pyrogram.types import Message

from backend.local_settings import TELEGRAM_APP_ID, TELEGRAM_API_HASH, TELEGRAM_PRICE_BOT_TOKEN
from bot.command_handlers.dea import DeaCommandHandler
from bot.command_handlers.deus import DeusCommandHandler
from bot.command_handlers.us_stocks import UsStocksCommandHandler


class Command(BaseCommand):
    help = 'runs price bot'

    command_handler_classes = [
        DeusCommandHandler,
        DeaCommandHandler,
        UsStocksCommandHandler
    ]

    def handle(self, *args, **options):

        app = Client(
            "bot",
            api_id=TELEGRAM_APP_ID,
            api_hash=TELEGRAM_API_HASH,
            bot_token=TELEGRAM_PRICE_BOT_TOKEN
        )

        command_handlers = [c(app) for c in self.command_handler_classes]

        @app.on_message()
        def handler(client, message: Message):
            message_text = message.text
            print("Received '{}'".format(message_text))

            is_self = message.from_user.is_self
            if is_self:
                print("It's my self")
                return

            for command_handler in command_handlers:
                if message_text in list(map(lambda x: x.lower(), command_handler.get_supported_commands())):
                    command_handler.handle(client, message)
                    break

        app.run()
