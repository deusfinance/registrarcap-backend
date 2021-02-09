from django.core.management.base import BaseCommand

from trades.fetchTrades.bakkt.get_bakkt_trades import get_bakkt_trades
from trades.fetchTrades.coinbase.get_cointbase_trades import get_coinbase_trades
from trades.fetchTrades.dea.get_dea_trades import get_dea_trades
from trades.fetchTrades.deus.get_deus_trades import get_deus_trades
from trades.models import Currency
from trades.update_trades import UpdateTrades


class Command(BaseCommand):
    help = 'update trades'

    def handle(self, *args, **options):
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
