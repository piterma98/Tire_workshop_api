"""Reservations urls."""
# Django
from django.urls import include
from django.urls import path

# 3rd-party
from rest_framework.routers import DefaultRouter

# Local
from .views import ReservationViewSet

router = DefaultRouter()
router.register(r'reservation', ReservationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
