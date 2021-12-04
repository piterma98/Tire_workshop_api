"""Accounts factories."""
# Django
from django.contrib.auth import get_user_model

# 3rd-party
import factory
from factory.django import DjangoModelFactory

# Local
from .models import WorkshopCustomer
from .models import WorkshopOwner


class UserFactory(DjangoModelFactory):
    """User factory."""

    class Meta:  # noqa: D106
        model = get_user_model()
        django_get_or_create = ['email', 'username']

    email = factory.Faker('email', locale='pl_PL')
    username = factory.LazyAttribute(lambda u: u.email.split('@')[0])
    first_name = factory.Faker('first_name', locale='pl_PL')
    last_name = factory.Faker('last_name', locale='pl_PL')
    is_active = True


class WorkshopOwnerFactory(DjangoModelFactory):
    """Workshop owner factory."""

    class Meta:  # noqa: D106
        model = WorkshopOwner

    user = factory.SubFactory(UserFactory)


class WorkshopCustomerFactory(DjangoModelFactory):
    """Workshop customer factory."""

    class Meta:  # noqa: D106
        model = WorkshopCustomer

    user = factory.SubFactory(UserFactory)
