"""Account serializer."""

# 3rd-party
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer

# Local
from .models import WorkshopCustomer


class CustomUserCreateSerializer(UserCreateSerializer):
    """CustomUserCreateSerializer class."""

    def create(self, validated_data):  # noqa: D102
        user = super(CustomUserCreateSerializer, self).create(validated_data)
        workshopcustomer = WorkshopCustomer.objects.create(user=user)
        workshopcustomer.save()
        return user


class CustomUserSerializer(UserSerializer):
    """Extended Custom User Serializer."""

    class Meta(UserSerializer.Meta):
        """Extend User serializer fields."""

        fields = UserSerializer.Meta.fields + ('is_workshop_owner',
                                               'is_workshop_customer')
        read_only_fields = UserSerializer.Meta.read_only_fields + ('is_workshop_owner',
                                                                   'is_workshop_customer')
