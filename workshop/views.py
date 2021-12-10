"""Workshop views."""

# Standard Library
from datetime import datetime

# 3rd-party
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

# Project
from accounts.pagination import PageNumberPagination
from accounts.permissions import IsWorkshopBusinessObjOwner
from accounts.permissions import IsWorkshopObjOwner
from accounts.permissions import IsWorkshopOwner
from accounts.permissions import method_permission_classes
from rating.models import Rating
from rating.serializers import RatingSerializer
from reservations.models import Reservation
from reservations.serializers import ReservationSerializer
from reservations.utils import generate_list_of_available_dates

# Local
from .models import BusinessHours
from .models import ServicesPriceList
from .models import Workshop
from .models import WorkshopPosition
from .serializers import BusinessHoursSerializer
from .serializers import ServicesPriceListSerializer
from .serializers import WorkshopPositionSerializer
from .serializers import WorkshopSerializer


class BusinessHoursViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin, UpdateModelMixin):
    """Business hours view set."""

    serializer_class = BusinessHoursSerializer
    queryset = BusinessHours.objects.filter(workshop__is_active=True)
    permission_classes = (IsAuthenticated, IsWorkshopOwner, IsWorkshopBusinessObjOwner)

    def get_queryset(self):  # noqa: D102
        if not self.request.user.is_anonymous:
            qs = self.queryset.filter(
                workshop__owner=self.request.user.workshopowner)
            return qs


class ServicePriceListViewSet(ModelViewSet):
    """Service price list view set."""

    serializer_class = ServicesPriceListSerializer
    queryset = ServicesPriceList.objects.filter(workshop__is_active=True)
    permission_classes = (IsAuthenticated, IsWorkshopOwner, IsWorkshopBusinessObjOwner)

    def get_queryset(self):  # noqa: D102
        if not self.request.user.is_anonymous:
            return self.queryset.filter(
                workshop__owner=self.request.user.workshopowner)


class WorkshopViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin, UpdateModelMixin):
    """Workshop view set."""

    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.filter(is_active=True).order_by('id')
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'city']

    @method_permission_classes((IsAuthenticated, IsWorkshopObjOwner, IsWorkshopOwner))
    def update(self, request, *args, **kwargs):  # noqa: D102
        return super().update(request, *args, **kwargs)

    @method_permission_classes((IsAuthenticated, IsWorkshopObjOwner, IsWorkshopOwner))
    def partial_update(self, request, *args, **kwargs):  # noqa: D102
        return super().partial_update(request, *args, **kwargs)

    @action(methods=['get'], detail=True, url_path='service_list',
            url_name='service-list')
    def service_list(self, request, pk=None):
        """Get list of workshop service price list."""
        workshop = self.get_object()
        object_list = ServicesPriceList.objects.filter(workshop=workshop)
        object_json = ServicesPriceListSerializer(object_list, many=True)
        return Response(object_json.data)

    @action(methods=['get'], detail=True, url_path='businesshour-list',
            url_name='businesshour-list')
    def businesshour_list(self, request, pk=None):
        """Get list of workshop businesshour list."""
        workshop = self.get_object()
        object_list = BusinessHours.objects.filter(workshop=workshop)
        order = BusinessHours.DayOfWeek.values
        sorted_qs = sorted(object_list, key=lambda x: order.index(x.day_of_week))
        object_json = BusinessHoursSerializer(sorted_qs, many=True)
        return Response(object_json.data)

    @action(methods=['get'], detail=True, url_path='rating_list',
            url_name='rating-list')
    def rating_list(self, request, pk=None):
        """Get list of workshop ratings."""
        workshop = self.get_object()
        object_list = Rating.objects.filter(workshop=workshop).order_by('-date_created')
        object_json = RatingSerializer(object_list, many=True)
        return Response(object_json.data)

    @action(methods=['get'], detail=True, url_path='position_list',
            url_name='position-list',
            permission_classes=(IsAuthenticated,))
    def position_list(self, request, pk=None):
        """Get list of workshop positions."""
        workshop = self.get_object()
        object_list = WorkshopPosition.objects.filter(workshop=workshop)
        object_json = WorkshopPositionSerializer(object_list, many=True)
        return Response(object_json.data)

    @action(methods=['get'], detail=False, url_path='owner_list', url_name='owner-list',
            permission_classes=(IsAuthenticated, IsWorkshopObjOwner, IsWorkshopOwner))
    def owner_list(self, request, pk=None):
        """Get list of owner workshops."""
        queryset = self.queryset.filter(owner=request.user.workshopowner)
        object_json = self.serializer_class(queryset, many=True)
        return Response(object_json.data)

    @action(methods=['get'], detail=True, url_path=r'reservation_list/(?P<date>\d{4}-\d{2}-\d{2})',
            url_name='reservations-list',
            permission_classes=(IsAuthenticated, IsWorkshopObjOwner, IsWorkshopOwner))
    def reservation_list(self, request, date, pk=None):
        """Get list of reservations on given day for workshop."""
        try:
            date_converted = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        workshop = self.get_object()
        object_list = Reservation.objects.filter(
            workshop=workshop,
            date__year=date_converted.year,
            date__month=date_converted.month,
            date__day=date_converted.day)
        object_json = ReservationSerializer(object_list, many=True)
        return Response(object_json.data)

    @action(methods=['get'], detail=True,
            url_path=r'reservation_dates_list/(?P<date>\d{4}-\d{2}-\d{2})/(?P<position_id>[^/.]+)',
            url_name='reservation-dates',
            permission_classes=(IsAuthenticated,))
    def reservation_dates_list(self, request, date, position_id, pk=None):
        """Return a list of available reservations dates."""
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
            workshop = self.get_object()
            position = workshop.workshopposition_set.get(id=position_id)
        except (WorkshopPosition.DoesNotExist, ValueError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not position.workshop == workshop:
            return Response({'detail': 'Invalid position id'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            dates = generate_list_of_available_dates(workshop, date, position)
            if not dates:
                return Response({'detail': 'No available dates with given parameters'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response(dates, status=status.HTTP_200_OK)
