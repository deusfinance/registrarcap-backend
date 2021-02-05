from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db.models import Q

from trades.models import Trade
from trades.update_trades import UpdateTrades


class Command(BaseCommand):
    help = 'update trades'

    def handle(self, *args, **options):

        trades = Trade.objects.filter(Q(eth_price=0) | Q(btc_price=0) | Q(usd_price=0)).order_by('timestamp')

        if trades.count():
            print("There is {} broken trades".format(trades.count()))
            update_trades = UpdateTrades(None, None)
            update_trades.fetch_prices(
                trades[0].timestamp,
                trades[trades.count() - 1].timestamp,
                'deus'
            )
            for trade in trades:
                print(trade.id)

                if trade.eth_price == 0:
                    trade.eth_price = Decimal(
                        update_trades.get_closest_price(
                            trade.timestamp,
                            update_trades.prices['deus_to_eth']
                        )
                    ) * trade.deus_price

                if trade.btc_price == 0:
                    trade.btc_price = Decimal(
                        update_trades.get_closest_price(
                            trade.timestamp,
                            update_trades.prices['eth_to_btc']
                        )
                    ) * trade.eth_price

                if trade.usd_price == 0:
                    trade.usd_price = Decimal(
                        update_trades.get_closest_price(
                            trade.timestamp,
                            update_trades.prices['eth_to_usd']
                        )
                    ) * trade.eth_price

                trade.save()
        else:
            print("All trades are ok")
