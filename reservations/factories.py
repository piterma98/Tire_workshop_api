"""Reservations factories."""
# Standard Library
import datetime

# 3rd-party
import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

# Project
from accounts.models import WorkshopCustomer
from workshop.factories import WorkshopPositionFactory
from workshop.models import Workshop

# Local
from .models import CarType
from .models import Reservation


class ReservationFactory(DjangoModelFactory):
    """Reservation factory."""

    class Meta:  # noqa: D106
        model = Reservation

    customer = factory.Faker('random_element', elements=WorkshopCustomer.objects.all())
    workshop = factory.Faker('random_element', elements=Workshop.objects.all())
    workshop_position = factory.SubFactory(WorkshopPositionFactory,
                                           workshop=factory.SelfAttribute('..workshop'))
    date = fuzzy.FuzzyDateTime(
        datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2015, 12, 31, 20, tzinfo=datetime.timezone.utc),
    )
    car_license_plate = fuzzy.FuzzyText(length=8)
    car_type = factory.Faker('random_element', elements=CarType.values)
