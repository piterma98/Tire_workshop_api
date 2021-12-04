"""Rating apps."""
# Django
from django.apps import AppConfig


class RatingConfig(AppConfig):
    """Rating config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rating'
