"""Rating views."""
# Django
from django.db import IntegrityError

# 3rd-party
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Project
from accounts.pagination import PageNumberPagination
from accounts.permissions import IsWorkshopCustomer

# Local
from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(ModelViewSet):
    """Rating view set."""

    serializer_class = RatingSerializer
    pagination_class = PageNumberPagination
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsWorkshopCustomer)

    def get_queryset(self):  # noqa: D102
        if not self.request.user.is_anonymous:
            return self.queryset.filter(
                customer=self.request.user.workshopcustomer).order_by('-date_created')

    def perform_create(self, serializer):  # noqa: D102
        return serializer.save(customer=self.request.user.workshopcustomer)

    def create(self, request, *args, **kwargs):    # noqa: D102
        try:
            return super().create(request)
        except IntegrityError:
            content = {'error': 'Review for given workshop already exists'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
