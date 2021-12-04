"""Workshop admin."""
# Django
from django.contrib import admin

# Local
from .forms import BusinessHourAdminForm
from .forms import WorkshopAdminForm
from .models import BusinessHours
from .models import ServicesPriceList
from .models import Workshop
from .models import WorkshopPosition


class BusinessHoursAdmin(admin.StackedInline):
    """Business hours inline admin."""

    model = BusinessHours
    form = BusinessHourAdminForm
    max_num = 7


class ServicesPriceListAdmin(admin.StackedInline):
    """Business hours inline admin."""

    model = ServicesPriceList


class WorkshopPositionAdmin(admin.StackedInline):
    """Workshop position inline admin."""

    model = WorkshopPosition


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    """Workshop admin."""

    form = WorkshopAdminForm

    list_display = [
        'id',
        'name',
        'owner',
        'city',
    ]

    list_filter = [
        'name',
        'owner',
        'city',
    ]

    exclude = [
        'image',
    ]

    search_fields = [
        'id',
        'name',
        'owner__user__email',
        'city',
    ]

    readonly_fields = ['get_image', 'average_rating']

    inlines = [BusinessHoursAdmin, ServicesPriceListAdmin, WorkshopPositionAdmin]
