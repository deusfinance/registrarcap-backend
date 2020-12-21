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

        duplicates = 0
        for tx in raw_transactions:
            transaction_hash = tx[3]

            trade_data = {
                "timestamp": int(tx[0].timestamp()),
                "block": tx[1],
                "price": tx[2],
                "hash": transaction_hash
            }

            if not Trade.objects.filter(hash=transaction_hash).exists():
                trade = Trade(**trade_data)
                trade.save()
            else:
                duplicates += 1
                print('duplicate hash', trade_data)

        print("{} of {} trades has duplicate hashes".format(duplicates, len(raw_transactions)))
