"""Rating factories."""
# 3rd-party
import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

# Project
from accounts.models import WorkshopCustomer
from workshop.models import Workshop

# Local
from .models import Rating


class RatingFactory(DjangoModelFactory):
    """Business hours factory."""

    class Meta:  # noqa: D106
        model = Rating
        django_get_or_create = ('workshop', 'customer')

    workshop = factory.Iterator(Workshop.objects.all())
    customer = factory.Iterator(WorkshopCustomer.objects.all())
    rate = fuzzy.FuzzyInteger(1, 5)
    description = factory.Faker('text', locale='pl_PL')
