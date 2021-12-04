"""Reservations apps."""
# Django
from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    """Reservations config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'
