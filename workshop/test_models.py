"""Workshop test models."""

# Django
from django.test import TestCase

# Local
from .factories import ServicesPriceListFactory
from .factories import WorkshopFactory
from .factories import WorkshopPositionFactory


class WorkshopTestCase(TestCase):
    """Workshop test."""

    def test_str(self):
        """Test for string representation."""
        workshop = WorkshopFactory()
        self.assertEqual(f'{workshop}', workshop.name)


class WorkshopPositionTestCase(TestCase):
    """Workshop position test."""

    def test_str(self):
        """Test for string representation."""
        workshop = WorkshopFactory()
        workshop_position = WorkshopPositionFactory(workshop=workshop)
        self.assertEqual(f'{workshop_position}',
                         f'ID: {workshop_position.id} '
                         f'{workshop_position.workshop.name} '
                         f'{workshop_position.name}')


class ServicesPriceListTestCase(TestCase):
    """Workshop services price list test."""

    def test_str(self):
        """Test for string representation."""
        workshop = WorkshopFactory()
        service = ServicesPriceListFactory(workshop=workshop)
        self.assertEqual(f'{service}', f'{service.workshop.name} {service.name}')
