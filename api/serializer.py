from rest_framework import serializers
from .models import Spread, Polling
from decimal import Decimal


class SpreadSerializer(serializers.ModelSerializer):
    """Serializer for `Spread` model"""

    class Meta:
        model = Spread
        fields = [
            "market_id",
            "value",
            "currency",
        ]


class SpreadSerializerFull(serializers.ModelSerializer):
    """Serializer for all `Spread` model attributes"""

    class Meta:
        model = Spread
        fields = "__all__"


class PollingSerializer(serializers.ModelSerializer):
    """Serializer for `Polling` model"""

    # virtual fields to show amounts in the same fashion as Buda.com API
    current_spread = serializers.SerializerMethodField()
    stored_spread = serializers.SerializerMethodField()

    def get_current_spread(self, polling) -> tuple[Decimal, str]:
        return [polling.current_spread_value, polling.current_spread_currency]

    def get_stored_spread(self, polling) -> tuple[Decimal, str]:
        return [polling.stored_spread_value, polling.stored_spread_currency]

    class Meta:
        model = Polling
        fields = [
            "market_id",
            "current_is_greater",
            "stored_is_greater",
            "difference",
            "current_spread",
            "stored_spread",
            "stored_spread_date",
        ]
