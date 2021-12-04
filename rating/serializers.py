"""Rating serializers."""
# 3rd-party
from rest_framework import serializers

# Local
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """Services price list serializer."""

    customer_name = serializers.CharField(source='customer.user', read_only=True)

    class Meta:  # noqa: D106
        model = Rating
        fields = ('id', 'workshop', 'rate', 'description', 'date_created', 'customer_name')
        read_only_fields = ('id', 'date_created', 'customer_name')
