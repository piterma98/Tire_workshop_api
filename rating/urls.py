"""Rating url."""
# Django
from django.urls import include
from django.urls import path

# 3rd-party
from rest_framework.routers import DefaultRouter

# Project
from rating.views import RatingViewSet

router = DefaultRouter()
router.register(r'rating', RatingViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
