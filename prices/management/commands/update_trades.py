from django.core.management.base import BaseCommand

from prices.get_transactions import update_transactions
from prices.models import Trade


class Command(BaseCommand):
    help = 'update trades'

    def handle(self, *args, **options):
        raw_transactions = update_transactions()

        trades = []

        try:
            latest_trade = Trade.objects.latest('timestamp')
            latest_timestamp = latest_trade.timestmap
        except Trade.DoesNotExist:
            latest_timestamp = 0

        for tx in raw_transactions:

            timestamp = int(tx[0].timestamp())
            if timestamp < latest_timestamp:
                continue

            trades.append(Trade(**{
                "timestamp": timestamp,
                "price": tx[1]
            }))

        trades.sort(key=lambda o: o.timestamp)

        Trade.objects.bulk_create(trades)
