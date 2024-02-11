from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Spread, Polling
from .serializer import (
    SpreadSerializer,
    SpreadSerializerFull,
    PollingSerializer,
)


class SpreadViewSet(viewsets.ViewSet):

    # rename url parameter
    lookup_url_kwarg = "market_id"

    def list(self, request):
        """
        Calculate and return the current spread for all available markets.
        """

        spreads = Spread.get_each_markets_spread()
        serializer = SpreadSerializer(spreads, many=True)
        return Response(serializer.data)

    def retrieve(self, request, market_id: str = None):
        """
        Calculate and return the current spread for the specified market.
        """
        spread = Spread.create(market_id)
        serializer = SpreadSerializer(spread)
        return Response(serializer.data)

    @action(detail=True)
    def save(self, request, market_id=None):
        """
        Save the current spread for the specified market.
        """
        spread = Spread.create(market_id)
        spread.save()
        serializer = SpreadSerializerFull(spread)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(detail=True)
    def polling(self, request, market_id=None):
        """
        Return a comparison between the current spread vs.
        the latest stored one for the specified market.
        """
        try:
            stored_spreads = Spread.objects.filter(market_id__iexact=market_id)
            polling = Polling.create(stored_spreads.latest("fetch_date"))
            serializer = PollingSerializer(polling)
        except Spread.DoesNotExist:
            return Response(
                {"message": "No stored spread was found for this market"},
                status.HTTP_404_NOT_FOUND,
            )
        return Response(serializer.data)
