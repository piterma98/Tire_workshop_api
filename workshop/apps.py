"""Workshop apps."""
# Django
from django.apps import AppConfig


class WorkshopConfig(AppConfig):
    """Workshop config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workshop'
