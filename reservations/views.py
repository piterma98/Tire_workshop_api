"""Reservations views."""

# 3rd-party
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Project
from accounts.pagination import PageNumberPagination
from accounts.permissions import IsWorkshopCustomer
from accounts.permissions import IsWorkshopOwner

# Local
from .models import Reservation
from .serializers import ReservationSerializer
from .serializers import WorkshopOwnerReservationSerializer


class ReservationViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    """Reservation view set."""

    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, IsWorkshopCustomer)

    def get_queryset(self):  # noqa: D102
        if not self.request.user.is_anonymous:
            if hasattr(self.request.user, 'workshopcustomer'):
                return self.queryset.filter(
                    customer=self.request.user.workshopcustomer).order_by('-date_created')
            if hasattr(self.request.user, 'workshopowner'):
                return self.queryset.filter(workshop__owner=self.request.user.workshopowner)

    @action(methods=['patch'], detail=True, url_path='workshop', url_name='workshop-update',
            serializer_class=WorkshopOwnerReservationSerializer,
            permission_classes=(IsAuthenticated, IsWorkshopOwner))
    def status_update(self, request, pk=None):
        """Update reservation status."""
        self.queryset = Reservation.objects.all()
        reservation = self.get_object()
        serializer = self.get_serializer(reservation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
