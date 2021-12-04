"""Account serializer."""

# 3rd-party
from djoser.serializers import UserCreateSerializer

# Local
from .models import WorkshopCustomer


class CustomUserCreateSerializer(UserCreateSerializer):
    """CustomUserCreateSerializer class."""

    def create(self, validated_data):  # noqa: D102
        user = super(CustomUserCreateSerializer, self).create(validated_data)
        workshopcustomer = WorkshopCustomer.objects.create(user=user)
        workshopcustomer.save()
        return user
