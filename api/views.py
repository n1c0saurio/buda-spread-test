from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from requests.exceptions import HTTPError
from django.db import DatabaseError
from .models import Spread, Polling
from .serializer import (
    SpreadSerializer,
    SpreadSerializerFull,
    PollingSerializer,
)

# API documentation
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiRequest,
    OpenApiExample,
)


class SpreadViewSet(viewsets.ViewSet):

    # rename url parameter
    lookup_url_kwarg = "market_id"

    # set no auth for this endpoint
    authentication_classes = []

    @extend_schema(
        summary="Get spreads for all markets",
        responses={200: SpreadSerializer},
        examples=[
            OpenApiExample(
                "Example 1",
                summary="List of spread objects",
                value={
                    "market_id": "ETH-CLP",
                    "value": 21278.0,
                    "currency": "CLP",
                },
            ),
        ],
    )
    def list(self, request):
        """
        Calculate and return the current spread for all available markets.
        """
        try:
            spreads = Spread.get_each_markets_spread()
            serializer = SpreadSerializer(spreads, many=True)
        except HTTPError as e:
            return Response(
                {"message": "Can't retrieve the data to calculate the spread"},
                e.response.status_code,
            )
        return Response(serializer.data)

    @extend_schema(
        summary="Get a spread",
        responses={200: SpreadSerializer},
        parameters=[
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="market_id",
                type=OpenApiTypes.STR,
                required=True,
                description="ID of the market to calculate the spread from",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Valid market ID",
                        value="BTC-CLP",
                    ),
                ],
            ),
        ],
        examples=[
            OpenApiExample(
                "Example 1",
                summary="Spread object",
                value={
                    "market_id": "BTC-CLP",
                    "value": 481795.0,
                    "currency": "CLP",
                },
            ),
        ],
    )
    def retrieve(self, request, market_id: str = None):
        """
        Calculate and return the current spread for the specified market.
        """
        try:
            spread = Spread.create(market_id)
            serializer = SpreadSerializer(spread)
        except HTTPError as e:
            return Response(
                {"message": "Can't retrieve the data to calculate the spread"},
                e.response.status_code,
            )
        return Response(serializer.data)

    @extend_schema(
        summary="Save the current spread",
        responses={201: SpreadSerializerFull},
        parameters=[
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="market_id",
                type=OpenApiTypes.STR,
                required=True,
                description="ID of the market to save the spread from",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Valid market ID",
                        value="BTC-CLP",
                    ),
                ],
            ),
        ],
        examples=[
            OpenApiExample(
                "Example 1",
                summary="The full spread object stored in database",
                value={
                    "id": 13,
                    "market_id": "BTC-CLP",
                    "value": 481795.0,
                    "currency": "CLP",
                    "fetch_date": "2019-08-24T14:15:22Z",
                },
            ),
        ],
    )
    @action(detail=True)
    def save(self, request, market_id=None):
        """
        Save the current spread for the specified market.
        """
        try:
            spread = Spread.create(market_id)
            spread.save()
            serializer = SpreadSerializerFull(spread)
        except HTTPError as e:
            return Response(
                {"message": "Can't retrieve the data to calculate the spread"},
                e.response.status_code,
            )
        except DatabaseError:
            return Response(
                {"message": "Can't save the spread on database"},
                status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(serializer.data, status.HTTP_201_CREATED)

    @extend_schema(
        summary="Save a custom spread",
        responses={201: SpreadSerializerFull},
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "market_id": {
                        "description": "ID of the market",
                        "type": "string",
                    },
                    "value": {
                        "description": "Value of the Spread",
                        "type": "Decimal",
                    },
                    "currency": {
                        "description": "Corresponding currency of the value",
                        "type": "string",
                    },
                },
            },
        },
        examples=[
            OpenApiExample(
                "Example 1",
                summary="The full spread object stored in database",
                value={
                    "id": 26,
                    "market_id": "BTC-CLP",
                    "value": 1000.0,
                    "currency": "CLP",
                    "fetch_date": "2024-02-19T16:35:13Z",
                },
            ),
        ],
    )
    @action(detail=False, methods=["post"])
    def make(self, request):
        """
        Save a Spread with a user defined values.
        """
        try:
            spread = Spread.make(request.data)
            spread.save()
            serializer = SpreadSerializerFull(spread)
        except DatabaseError:
            return Response(
                {"message": "Can't save the spread on database"},
                status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(serializer.data, status.HTTP_201_CREATED)

    @extend_schema(
        summary="Compare spreads",
        responses={200: PollingSerializer},
        parameters=[
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="market_id",
                type=OpenApiTypes.STR,
                required=True,
                description="ID of the market to compare the spread data from",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Valid market ID",
                        value="BTC-CLP",
                    ),
                ],
            ),
        ],
        examples=[
            OpenApiExample(
                "Example 1",
                summary="Polling object",
                value={
                    "market_id": "BTC-CLP",
                    "current_is_greater": True,
                    "stored_is_greater": False,
                    "difference": 303395.0,
                    "current_spread": [410110.0, "CLP"],
                    "stored_spread": [106715.0, "CLP"],
                    "stored_spread_date": "2019-08-24T14:15:22Z",
                },
            ),
        ],
    )
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
