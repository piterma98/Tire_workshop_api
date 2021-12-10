"""Workshop serializers."""
# 3rd-party
from rest_framework import serializers

# Local
from .models import BusinessHours
from .models import ServicesPriceList
from .models import Workshop
from .models import WorkshopPosition


class BusinessHoursSerializer(serializers.ModelSerializer):
    """Business hours serializer."""

    workshop_name = serializers.ReadOnlyField(source='workshop.name')

    class Meta:  # noqa: D106
        model = BusinessHours
        fields = ('id', 'workshop_name', 'day_of_week', 'from_hour', 'to_hour', 'is_open')
        read_only_fields = ('id', 'day_of_week')


class ServicesPriceListSerializer(serializers.ModelSerializer):
    """Services price list serializer."""

    workshop_name = serializers.ReadOnlyField(source='workshop.name')

    class Meta:  # noqa: D106
        model = ServicesPriceList
        fields = ('id', 'workshop', 'workshop_name', 'name', 'price')
        extra_kwargs = {'workshop': {'required': True}}

    def create(self, validated_data):  # noqa: D102
        request = self.context.get('request', None)
        workshop_owner = request.user.workshopowner
        if workshop_owner != validated_data['workshop'].owner:
            raise serializers.ValidationError({'detail': 'You are not workshop owner'})
        return super().create(validated_data)


class WorkshopSerializer(serializers.ModelSerializer):
    """Workshop serializer."""

    class Meta:  # noqa: D106
        model = Workshop
        fields = [
            'id',
            'name',
            'description',
            'city',
            'zip_code',
            'street',
            'image',
            'phone_number',
            'page',
            'average_rating',
        ]
        read_only_fields = ('id', 'average_rating')


class WorkshopPositionSerializer(serializers.ModelSerializer):
    """Workshop position serializer."""

    class Meta:  # noqa: D106
        model = WorkshopPosition
        fields = [
            'id',
            'name',
        ]
