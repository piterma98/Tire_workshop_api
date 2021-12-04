"""Workshop factories."""
# Standard Library
import random
from datetime import time

# 3rd-party
import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal

# Project
from accounts.factories import WorkshopOwnerFactory

# Local
from .models import BusinessHours
from .models import ServicesPriceList
from .models import Workshop
from .models import WorkshopPosition
from .utils import encode_image_to_base64


class WorkshopFactory(DjangoModelFactory):
    """Workshop factory."""

    class Meta:  # noqa: D106
        model = Workshop

    owner = factory.SubFactory(WorkshopOwnerFactory)
    name = factory.Faker('company', locale='pl_PL')
    city = factory.Faker('city', locale='pl_PL')
    zip_code = factory.Faker('zipcode')
    description = factory.Faker('text', locale='pl_PL')
    street = factory.Faker('street_address', locale='pl_PL')
    image = factory.LazyAttribute(lambda _: encode_image_to_base64(
        factory.django.ImageField()._make_data(
            {'width': 400, 'height': 300})),
                                  )
    phone_number = factory.Faker('phone_number', locale='pl_PL')
    page = factory.Faker('url', locale='pl_PL')
    is_active = True


class BusinessHoursFactory(DjangoModelFactory):
    """Business hours factory."""

    class Meta:  # noqa: D106
        model = BusinessHours
        django_get_or_create = ('workshop', 'day_of_week')

    workshop = factory.Iterator(Workshop.objects.all())
    day_of_week = factory.Faker('random_element', elements=BusinessHours.DayOfWeek.values)
    from_hour = time(hour=random.randint(6, 8))
    to_hour = time(hour=random.randint(15, 17))
    is_open = True


class ServicesPriceListFactory(DjangoModelFactory):
    """Service price list factory."""

    class Meta:  # noqa: D106
        model = ServicesPriceList

    name = factory.Sequence(lambda n: f'Service {n}')
    price = FuzzyDecimal(10, 100, 2)


class WorkshopPositionFactory(DjangoModelFactory):
    """Workshop position factory."""

    class Meta:  # noqa: D106
        model = WorkshopPosition

    workshop = factory.Iterator(Workshop.objects.all())
    name = factory.Sequence(lambda n: f'Position {n}')
