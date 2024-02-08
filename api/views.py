from .models import Spread, Polling
from .serializer import SpreadSerializer, PollingSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class SpreadViewSet(viewsets.ViewSet):

    def list(self, request):
        spreads = Spread.get_each_markets_spread()
        serializer = SpreadSerializer(spreads, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        spread = Spread.create(pk)
        serializer = SpreadSerializer(spread)
        return Response(serializer.data)

    @action(detail=True)
    def save(self, request, pk=None):
        spread = Spread.create(pk)
        spread.save()
        serializer = SpreadSerializer(spread)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(detail=True)
    def polling(self, request, pk=None):
        """
        Return a comparison between the current market spread
        vs. the latest stored one for the same market.
        """
        try:
            stored_spreads = Spread.objects.filter(market_id__iexact=pk)
            polling = Polling.create(stored_spreads.latest("fetch_date"))
            serializer = PollingSerializer(polling)
        except Spread.DoesNotExist:
            return Response(
                {"message": "No stored spread was found for this market"},
                status.HTTP_404_NOT_FOUND,
            )
        return Response(serializer.data)
