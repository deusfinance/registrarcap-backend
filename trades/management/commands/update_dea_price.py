import requests
from django.core.management.base import BaseCommand
from trades.models import Trade
from trades.update_trades import UpdateTrades


class Command(BaseCommand):
    help = 'update trades'

    def handle(self, *args, **options):
        url = "https://dr-collector-api.herokuapp.com/v1/transactions?poolContract=0x92adab6d8dc13dbd9052b291cfc1d07888299d65&from={}&to={}"
        from_timestamp = 0
        to_timestamp = 99999999999999
        dea_deus_swaps = requests.get(url.format(from_timestamp, to_timestamp)).json()['results']
        deus_to_dea = [(s['timestamp'], 1 / s['price']) for s in dea_deus_swaps]

        for trade in Trade.objects.filter(timestamp__gte=deus_to_dea[0][0]).all():
            print(trade.id)
            if trade.currency.symbol == 'deus':
                trade.deus_price = 1
            trade.dea_price = UpdateTrades.get_closest_price(trade.timestamp, deus_to_dea) * trade.deus_price
            trade.save()
