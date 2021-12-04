"""Workshop admin test."""

# Django
from django.apps import apps
from django.contrib import admin
from django.test import SimpleTestCase

# Project
from workshop.models import BusinessHours
from workshop.models import ServicesPriceList
from workshop.models import WorkshopPosition


class TestAdmin(SimpleTestCase):
    """Test admin apps."""

    def test_all_models_are_registered(self):
        """Test all models."""
        app = apps.get_app_config('workshop')
        models = app.get_models()
        for model in models:
            try:
                self.assertIs(
                    True,
                    admin.site.is_registered(model),
                    msg=f'Did you forget to register the "{model.__name__}" in the django-admin?')
            except AssertionError as exception:
                # these models have been registred as inlines in the admin.
                if model in [BusinessHours, ServicesPriceList, WorkshopPosition]:
                    continue
                else:
                    raise exception
