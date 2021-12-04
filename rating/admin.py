"""Rating admin."""
# Django
from django.contrib import admin

# Local
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating admin."""

    list_display = [
        'id',
        'customer',
        'workshop',
        'date_created',
    ]

    list_filter = [
        'customer',
        'workshop',
        'date_created',
    ]

    search_fields = [
        'id',
        'customer__user__email',
        'workshop__name',
    ]

    readonly_fields = ['date_created']
