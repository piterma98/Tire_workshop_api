"""Accounts admin."""
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local
from .models import CustomUser
from .models import WorkshopCustomer
from .models import WorkshopOwner


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom user admin."""

    list_display = ('id', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active')
    list_filter = ('email', 'first_name', 'last_name', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active',
                'is_superuser'),
            },
         ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'id')
    ordering = ('email',)


@admin.register(WorkshopOwner)
class WorkshopOwnerAdmin(admin.ModelAdmin):
    """WorkshopOwner admin."""

    list_display = [
        'user',
    ]

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
    ]

    autocomplete_fields = [
        'user',
    ]


@admin.register(WorkshopCustomer)
class WorkShopCustomerAdmin(admin.ModelAdmin):
    """WorkShopCustomer admin."""

    list_display = [
        'user',
    ]

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
    ]

    autocomplete_fields = [
        'user',
    ]
