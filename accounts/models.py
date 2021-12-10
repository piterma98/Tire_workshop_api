"""Accounts models."""
# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    """CustomUser model."""

    email = models.EmailField(_('email address'), unique=True, validators=[validate_email])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):  # noqa: D105
        return self.email

    @property
    def is_workshop_owner(self):
        """Return user type."""
        return hasattr(self, 'workshopowner')

    @property
    def is_workshop_customer(self):
        """Return user type."""
        return hasattr(self, 'workshopcustomer')


class WorkshopOwner(models.Model):
    """WorkshopOwner model."""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        """Owner username toString."""
        return self.user.email


class WorkshopCustomer(models.Model):
    """WorkShopCustomer model."""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        """Client username toString."""
        return self.user.email
