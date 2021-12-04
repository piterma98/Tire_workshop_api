"""Project urls."""
# Django
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

# 3rd-party
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Tire workshop API',
        default_version='v1',
        description='TODO',
        contact=openapi.Contact(email='admin@admin.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include('workshop.urls')),
    path('', include('reservations.urls')),
    path('', include('rating.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui(
            'swagger',
            cache_timeout=0),
            name='schema-swagger-ui'),
    ]
