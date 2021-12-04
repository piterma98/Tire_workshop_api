"""Workshop models."""
# Django
from django.db import models
from django.db.models import Avg
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Project
from accounts.models import WorkshopOwner


class Workshop(models.Model):
    """Workshop model."""

    owner = models.ForeignKey(WorkshopOwner, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.TextField(_('Workshop name'))
    description = models.TextField(_('Description'))
    city = models.CharField(_('City'), max_length=120, blank=True, null=True)
    zip_code = models.CharField(_('Zip code'), max_length=15, blank=True, null=True)
    street = models.CharField(_('Street'), max_length=150, blank=True, null=True)
    image = models.TextField(null=True, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=25, blank=True, null=True)
    page = models.URLField(_('Page url'), max_length=200)
    is_active = models.BooleanField(default=True)

    @property
    def average_rating(self):
        """Return workshop average rating."""
        value = self.rating_set.filter(
            workshop_id=self.id).aggregate(Avg('rate'))['rate__avg']
        if value:
            return round(value, 2)
        return 0

    def get_image(self):  # noqa : D102
        if self.image:
            return mark_safe(f'<img src="{self.image}"')

    get_image.short_description = 'Image render'

    def __str__(self):  # noqa : D105
        return self.name


class BusinessHours(models.Model):
    """Business hours model."""

    class Meta:  # noqa: D106
        constraints = [
            models.UniqueConstraint(fields=['workshop', 'day_of_week'], name='unique_days'),
        ]

    class DayOfWeek(models.TextChoices):  # noqa: D106
        MONDAY = 'monday', _('Monday')
        TUESDAY = 'tuesday', _('Tuesday')
        WEDNESDAY = 'wednesday', _('Wednesday')
        THURSDAY = 'thursday', _('Thursday')
        FRIDAY = 'friday', _('Friday')
        SATURDAY = 'saturday', _('Saturday')
        SUNDAY = 'sunday', _('Sunday')

    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, blank=True, null=True)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    day_of_week = models.CharField(_('Day of week'),
                                   max_length=20,
                                   choices=DayOfWeek.choices)
    is_open = models.BooleanField()

    def __str__(self):  # noqa: D105
        return f'{self.workshop} {self.day_of_week}'


class ServicesPriceList(models.Model):
    """Services price list."""

    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.TextField(_('Service name'))
    price = models.DecimalField(_('Service price'), max_digits=10, decimal_places=2)

    def __str__(self):  # noqa: D105
        return f'{self.workshop} {self.name}'


class WorkshopPosition(models.Model):
    """Workshop position."""

    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(_('Position name'), max_length=100)

    def __str__(self):  # noqa: D105
        return f'ID: {self.id} {self.workshop} {self.name}'
