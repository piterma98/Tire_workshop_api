"""Workshop urls."""
# Django
from django.conf.urls import include
from django.urls import path

# 3rd-party
from rest_framework.routers import DefaultRouter

# Local
from .views import BusinessHoursViewSet
from .views import ServicePriceListViewSet
from .views import WorkshopViewSet

router = DefaultRouter()
router.register(r'workshop', WorkshopViewSet)
router.register(r'businesshour', BusinessHoursViewSet)
router.register(r'servicepricelist', ServicePriceListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
