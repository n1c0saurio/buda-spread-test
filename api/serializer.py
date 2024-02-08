from rest_framework import serializers
from .models import Spread, Polling


class SpreadSerializer(serializers.ModelSerializer):
    """Serializer for `Spread` model"""

    class Meta:
        model = Spread
        fields = "__all__"


class PollingSerializer(serializers.ModelSerializer):
    """Serializer for `Polling` model"""

    # virtual fields to show amounts in the same fashion as Buda.com API
    current_spread = serializers.SerializerMethodField()
    stored_spread = serializers.SerializerMethodField()

    def get_current_spread(self, polling):
        return [polling.current_spread_value, polling.current_spread_currency]

    def get_stored_spread(self, polling):
        return [polling.stored_spread_value, polling.stored_spread_currency]

    class Meta:
        model = Polling
        fields = [
            "market_id",
            "current_spread",
            "stored_spread",
            "result",
            "stored_spread_date",
        ]
