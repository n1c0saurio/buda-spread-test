from rest_framework import serializers
from .models import Spread


class SpreadSerializer(serializers.ModelSerializer):
    """Serializer for `Spread` model"""

    class Meta:
        model = Spread
        fields = "__all__"
