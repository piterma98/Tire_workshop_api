"""Ratings models."""
# Django
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project
from accounts.models import WorkshopCustomer
from workshop.models import Workshop


class Rating(models.Model):
    """Rating model."""

    class Meta:  # noqa: D106
        constraints = [
            models.UniqueConstraint(fields=['workshop', 'customer'], name='unique_review'),
        ]

    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(WorkshopCustomer, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    rate = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(5)])
    description = models.TextField(_('Description'))
    date_created = models.DateTimeField(_('Date created'), auto_now=True)

    def __str__(self):  # noqa: D105
        return f'{self.workshop} {self.customer}'
