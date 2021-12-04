"""Reservations utils."""
# Standard Library
from datetime import datetime

# Django
from django.conf import settings
from django.utils import timezone

# 3rd-party
import pandas as pd

# Project
from workshop.models import BusinessHours

# Local
from .models import Reservation


def generate_list_of_available_dates(workshop, date, workshop_position):
    """Generate list of available dates."""
    available_dates = list()
    try:
        business_hours = workshop.businesshours_set.get(
            day_of_week=date.strftime('%A').lower())
    except BusinessHours.DoesNotExist:
        return available_dates
    if workshop.is_active and business_hours.is_open:
        reservations_on_this_day = Reservation.objects.filter(
            workshop=workshop,
            date__contains=date.strftime('%Y-%m-%d'),
            workshop_position=workshop_position)
        from_date = datetime.combine(date, business_hours.from_hour, tzinfo=timezone.utc)
        to_date = datetime.combine(date, business_hours.to_hour, tzinfo=timezone.utc)
        date_range = pd.date_range(from_date, to_date, freq=settings.RESERVATIONS_FREQUENCY)
        for date_value in date_range:
            date_value = date_value.to_pydatetime()
            if not reservations_on_this_day.filter(date=date_value):
                if datetime.now(tz=timezone.utc) < date_value:
                    available_dates.append(date_value)
    return available_dates
