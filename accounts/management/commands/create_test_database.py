"""Create test database."""
# Standard Library
import random
from datetime import datetime
from datetime import time
from datetime import timedelta

# Django
from django.core.management.base import BaseCommand

# Project
from accounts.factories import WorkshopCustomerFactory
from accounts.models import CustomUser
from rating.factories import RatingFactory
from reservations.factories import ReservationFactory
from reservations.utils import generate_list_of_available_dates
from workshop.factories import BusinessHoursFactory
from workshop.factories import ServicesPriceListFactory
from workshop.factories import WorkshopFactory
from workshop.factories import WorkshopPositionFactory
from workshop.models import BusinessHours
from workshop.models import Workshop
from workshop.models import WorkshopPosition


class Command(BaseCommand):
    """Command."""

    help = 'Create test database.'

    def handle(self, *args, **options):
        """Handle command."""
        WorkshopFactory.create_batch(random.randrange(2, 8))
        for workshop in Workshop.objects.all():
            for day in BusinessHours.DayOfWeek.values:
                if day == 'sunday':
                    BusinessHoursFactory(workshop=workshop, day_of_week=day, is_open=False,
                                         from_hour=time(hour=0), to_hour=time(hour=0))
                else:
                    BusinessHoursFactory(workshop=workshop, day_of_week=day, is_open=True,
                                         from_hour=time(hour=random.randint(6, 8)),
                                         to_hour=time(hour=random.randint(15, 17)))
            ServicesPriceListFactory.create_batch(size=random.randrange(2, 10), workshop=workshop)
        for workshop in Workshop.objects.all():
            WorkshopPositionFactory(workshop=workshop)
        for x in range(3):
            WorkshopCustomerFactory()
        for workshop in Workshop.objects.all():
            workshop_positions = WorkshopPosition.objects.filter(workshop=workshop)
            for x in range(5):
                random_position = workshop_positions[random.randrange(len(workshop_positions))]
                dates = generate_list_of_available_dates(
                    workshop,
                    datetime.today() + timedelta(days=1),
                    random_position)
                if dates:
                    date = dates[random.randrange(len(dates))]
                    ReservationFactory(workshop=workshop,
                                       date=date,
                                       workshop_position=random_position)
        for x in range(20):
            RatingFactory()
        if not CustomUser.objects.filter(is_superuser=True).exists():
            CustomUser.objects.create_superuser(
                first_name='a',
                last_name='b',
                email='admin@admin.pl',
                password='123456')

        self.stdout.write(self.style.SUCCESS('Successfully created test database'))
