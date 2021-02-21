import datetime

from django.core.management.base import BaseCommand
from pyrogram import Client

from backend.local_settings import TELEGRAM_APP_ID, TELEGRAM_API_HASH, TELEGRAM_PRICE_BOT_TOKEN
from trades.fetchTrades.bakkt.get_bakkt_trades import get_bakkt_trades
from trades.fetchTrades.coinbase.get_cointbase_trades import get_coinbase_trades
from trades.fetchTrades.dea.get_dea_trades import get_dea_trades
from trades.fetchTrades.deus.get_deus_trades import get_deus_trades
from trades.models import Currency, Trade
from trades.update_trades import UpdateTrades


class Command(BaseCommand):
    help = 'update trades'

    def handle(self, *args, **options):
        last_trade = Trade.objects.first()
        if last_trade.timestamp + 12 * 60 * 60 > datetime.datetime.now().timestamp():
            app = Client(
                "bot",
                api_id=TELEGRAM_APP_ID,
                api_hash=TELEGRAM_API_HASH,
                bot_token=TELEGRAM_PRICE_BOT_TOKEN
            )
            app.start()
            app.send_message(
                'mmdmst',
                "There is a problem with chart scripts, last trade id: {}".format(last_trade.id)
            )
            app.stop()

        currency = Currency.objects.get(symbol='deus')
        update_trades = UpdateTrades(currency, get_deus_trades)
        update_trades.update()

        currency = Currency.objects.get(symbol='dea')
        update_trades = UpdateTrades(currency, get_dea_trades)
        update_trades.update()

        currency = Currency.objects.get(symbol='coinbase')
        update_trades = UpdateTrades(currency, get_coinbase_trades)
        update_trades.update()

        currency = Currency.objects.get(symbol='bakkt')
        update_trades = UpdateTrades(currency, get_bakkt_trades)
        update_trades.update()
