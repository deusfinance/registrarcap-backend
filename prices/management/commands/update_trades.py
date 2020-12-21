from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from prices.get_transactions import get_trades
from prices.models import Trade


class Command(BaseCommand):
    help = 'update trades'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('limit', nargs='?', type=int, default=1000)

    @transaction.atomic
    def handle(self, *args, **options):
        limit = options['limit']

        trades = []

        try:
            latest_trade = Trade.objects.latest('timestamp')
            latest_timestamp = latest_trade.timestamp
            latest_block = latest_trade.block
            print("latest_trade: #{}".format(latest_trade.id))
        except Trade.DoesNotExist:
            latest_timestamp = 0
            latest_block = 0

        raw_transactions = get_trades(latest_block, latest_timestamp, limit=limit)

        for tx in raw_transactions:
            timestamp = int(tx[0].timestamp())

            trades.append(Trade(**{
                "timestamp": timestamp,
                "block": tx[1],
                "price": tx[2]
            }))

        trades.sort(key=lambda o: o.timestamp)

        Trade.objects.bulk_create(trades)
