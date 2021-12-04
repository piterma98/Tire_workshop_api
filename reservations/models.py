"""Reservations models."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project
from accounts.models import WorkshopCustomer
from workshop.models import Workshop
from workshop.models import WorkshopPosition


class CarType(models.TextChoices):
    """Car type choices."""

    SEDAN = 'sedan', _('sedan')
    COUPE = 'coupe', _('coupe')
    WAGON = 'wagon', _('wagon')
    HATCHBACK = 'hatchback', _('hatchback')
    SUV = 'suv', _('suv')
    VAN = 'van', _('van')


class Reservation(models.Model):
    """Reservations model."""

    class Status(models.TextChoices):
        """Reservation status."""

        ACCEPTED = 'accepted', _('accepted')
        CANCELLED = 'cancelled', _('cancelled')
        DONE = 'done', _('done')

    class Meta:  # noqa: D106
        constraints = [
            models.UniqueConstraint(fields=['workshop', 'date', 'workshop_position'],
                                    name='unique_reservations'),
        ]

    customer = models.ForeignKey(WorkshopCustomer, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, blank=True,
                                 null=True)
    workshop_position = models.ForeignKey(WorkshopPosition, on_delete=models.SET_NULL,
                                          blank=True, null=True)
    date = models.DateTimeField()
    car_license_plat = models.CharField(max_length=30)
    status = models.CharField(_('Reservation status'), choices=Status.choices,
                              default=Status.ACCEPTED, max_length=30)
    car_type = models.CharField(_('Car type'), max_length=30, choices=CarType.choices)
    date_created = models.DateTimeField(_('Date created'), auto_now=True)

    def __str__(self):  # noqa: D105
        return f'{self.customer} {self.car_license_plat} {self.workshop} {self.workshop_position}'
