"""Reservations serializer."""

# 3rd-party
from rest_framework import serializers

# Local
from .models import Reservation
from .utils import generate_list_of_available_dates


class ReservationSerializer(serializers.ModelSerializer):
    """Reservation serializer."""

    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    position_name = serializers.CharField(source='workshop_position.name', read_only=True)

    class Meta:  # noqa: D106
        model = Reservation
        fields = [
            'id',
            'workshop',
            'workshop_name',
            'workshop_position',
            'position_name',
            'customer',
            'date',
            'status',
            'car_license_plate',
            'car_type',
        ]
        read_only_fields = ('id', 'status', 'customer')
        extra_kwargs = {'workshop': {'required': True},
                        'workshop_position': {'required': True}}

    def validate(self, data):
        """Check that given data is valid."""
        if data['workshop'] != data['workshop_position'].workshop:
            raise serializers.ValidationError('Position is not valid for given workshop')
        if not data['workshop'].is_active:
            raise serializers.ValidationError('Error')
        if data['date'] not in generate_list_of_available_dates(
                data['workshop'],
                data['date'],
                data['workshop_position']):
            raise serializers.ValidationError('Date is not available')
        return data


class WorkshopOwnerReservationSerializer(serializers.ModelSerializer):
    """Workshop owner reservation serializer."""

    class Meta:  # noqa: D106
        model = Reservation
        fields = [
            'id',
            'status',
        ]
        read_only_fields = ('id',)
