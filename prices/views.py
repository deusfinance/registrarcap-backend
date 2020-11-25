from django.db.models.deletion import get_candidate_relations_to_delete
from rest_framework.response import Response
from rest_framework.views import APIView

from prices.get_candlesticks import get_candlesticks
from prices.get_prices import get_prices


class PricesApiView(APIView):

    def get(self, request):
        contract_addresses = [
            '0x3b62f3820e0b035cc4ad602dece6d796bc325325',
            # '0x80ab141f324c3d6f2b18b030f1c4e95d4d658778',
        ]
        prices = get_prices(contract_addresses)

        return Response(prices)


class CandlesticksApiView(APIView):

    def get(self, request):
        candlesticks = get_candlesticks(
            '0x3b62f3820e0b035cc4ad602dece6d796bc325325',
            request.GET.get('resolution', 60),
            request.GET.get('from'),
            request.GET.get('to'),
        )
        return Response(candlesticks)
