"""Reservations admin."""
# Django
from django.contrib import admin

# Local
from .forms import ReservationAdminForm
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservations admin."""

    form = ReservationAdminForm

    list_display = [
        'id',
        'customer',
        'date',
        'workshop',
        'status',
        'date_created',
    ]

    list_filter = [
        'customer',
        'workshop',
        'date',
        'status',
        'date_created',
    ]

    search_fields = [
        'id',
        'customer__user__email',
        'workshop__name',
        'date',
        'status',
    ]

    readonly_fields = ['date_created']
