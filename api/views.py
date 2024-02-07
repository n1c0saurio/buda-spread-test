from .models import Spread
from .serializer import SpreadSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class SpreadViewSet(viewsets.ViewSet):

    def list(self, request):
        spreads = Spread.get_each_markets_spread()
        serializer = SpreadSerializer(spreads, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        spread = Spread(pk)
        serializer = SpreadSerializer(spread)
        return Response(serializer.data)
