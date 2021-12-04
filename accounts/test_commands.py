"""Accounts test commands."""
# Standard Library
from io import StringIO

# Django
from django.core.management import call_command
from django.test import TestCase


class CommandTestCase(TestCase):
    """Command test case."""

    def test_wait_for_db(self):
        """Test db connection."""
        out = StringIO()
        call_command('wait_for_db', stdout=out)
        self.assertIn('Database connection OK', out.getvalue())
