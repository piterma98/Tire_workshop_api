"""Accounts manager."""
# Django
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """CustomUser manager."""

    def create_user(self, email, password=None, **extra_fields):  # noqa: D102
        if not email:
            raise ValueError(_('User must have an email'))
        email = self.normalize_email(email)
        username = email.split('@')[0]
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):   # noqa: D102
        user = self.create_user(email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
