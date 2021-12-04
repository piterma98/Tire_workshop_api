"""Reservations forms."""
# Django
from django import forms
from django.core.exceptions import ValidationError

# Local
from .utils import generate_list_of_available_dates


class ReservationAdminForm(forms.ModelForm):
    """Reservation admin form."""

    def clean(self):  # noqa: D102
        if self.cleaned_data['workshop'] != self.cleaned_data['workshop_position'].workshop:
            raise ValidationError('Position is not valid')
        if self.cleaned_data['date'] not in generate_list_of_available_dates(
                self.cleaned_data['workshop'],
                self.cleaned_data['date'],
                self.cleaned_data['workshop_position']):
            raise ValidationError('Date is not available')
        super(ReservationAdminForm, self).clean()
