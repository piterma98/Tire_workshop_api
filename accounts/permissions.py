"""Accounts permissions."""
# 3rd-party
from rest_framework.permissions import BasePermission


class IsWorkshopOwner(BasePermission):
    """WorkshopOwner permission."""

    def has_permission(self, request, view):  # noqa: D102
        return request.user.is_workshop_owner


class IsWorkshopCustomer(BasePermission):
    """WorkshopCustomer permission."""

    def has_permission(self, request, view):  # noqa: D102
        return request.user.is_workshop_customer


class IsWorkshopObjOwner(BasePermission):
    """Check if is workshop owner."""

    def has_object_permission(self, request, view, obj):  # noqa: D102
        if obj.owner == request.user.workshopowner:
            return True
        return False


class IsWorkshopBusinessObjOwner(BasePermission):
    """Check if is workshop business hours owner."""

    def has_object_permission(self, request, view, obj):  # noqa: D102
        if obj.workshop.owner == request.user.workshopowner:
            return True
        return False


def method_permission_classes(classes):
    """Permissions per method."""
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator
