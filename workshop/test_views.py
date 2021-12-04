"""Workshop test views."""
# Standard Library
import random
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone

# 3rd-party
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Project
from accounts.factories import UserFactory
from accounts.factories import WorkshopCustomerFactory
from accounts.factories import WorkshopOwnerFactory
from rating.factories import RatingFactory

# Local
from .factories import BusinessHoursFactory
from .factories import ServicesPriceListFactory
from .factories import WorkshopFactory
from .factories import WorkshopPositionFactory
from .models import BusinessHours
from .models import ServicesPriceList
from .models import Workshop


class WorkshopViewSetTestCase(APITestCase):
    """Workshop view set test."""

    def setUp(self):
        """User setup."""
        self.data = {
            'email': 'user@user.pl',
            'password': 'ZAQ!2wsx',
        }
        self.user = UserFactory(email=self.data['email'])
        self.user.set_password(self.data['password'])
        self.user.save()
        jwt_get_token_url = reverse('jwt-create')
        response = self.client.post(jwt_get_token_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    @staticmethod
    def get_detail_url(workshop_id):
        """Get workshop url."""
        return reverse('workshop-detail', kwargs={'pk': workshop_id})

    def test_get(self):
        """GET a workshop detail."""
        workshop = WorkshopFactory()
        response = self.client.get(self.get_detail_url(workshop.id))
        self.assertEqual(str(workshop), response.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        """GET a list of Workshops."""
        WorkshopFactory.create_batch(size=5)
        url = reverse('workshop-list')
        response = self.client.get(url)
        self.assertEqual(Workshop.objects.count(), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """Delete is not implemented."""
        workshop = WorkshopFactory()
        response = self.client.delete(self.get_detail_url(workshop.id))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_service_list(self):
        """Get list of workshop service price list."""
        workshop = WorkshopFactory()
        size = random.randrange(2, 10)
        ServicesPriceListFactory.create_batch(size=size, workshop=workshop)
        response = self.client.get(reverse('workshop-service-list',
                                           kwargs={'pk': workshop.id}))
        self.assertEqual(ServicesPriceList.objects.count(), size)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workshop_owner(self):
        """Only workshop owner can use put/update method on api."""
        workshop_owner = WorkshopOwnerFactory(user=self.user)
        workshop = WorkshopFactory(owner=workshop_owner)
        response = self.client.patch(reverse('workshop-detail', kwargs={'pk': workshop.id}), {
            'name': 'TEST',
            'descripotion': 'Text',
            'page': 'https://www.google.pl/',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_list(self):
        """Get a list of owner workshops."""
        workshop_owner = WorkshopOwnerFactory(user=self.user)
        WorkshopFactory(owner=workshop_owner)
        response = self.client.get(reverse('workshop-owner-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_position_list(self):
        """Get a list of workshop positions."""
        workshop_owner = WorkshopOwnerFactory(user=self.user)
        workshop = WorkshopFactory(owner=workshop_owner)
        position = WorkshopPositionFactory(workshop=workshop)
        response = self.client.get(reverse('workshop-position-list',
                                           kwargs={'pk': workshop.id}))
        self.assertEqual(response.data[0]['name'], position.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rating_list(self):
        """Get a list of workshop ratings."""
        workshop = WorkshopFactory()
        RatingFactory(workshop=workshop, customer=WorkshopCustomerFactory())
        response = self.client.get(reverse('workshop-rating-list',
                                           kwargs={'pk': workshop.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservations_day_list(self):
        """Get a list of reservations on given day."""
        workshop_owner = WorkshopOwnerFactory(user=self.user)
        workshop = WorkshopFactory(owner=workshop_owner)
        position = WorkshopPositionFactory(workshop=workshop)
        WorkshopCustomerFactory.create_batch(size=3)
        next_monday = datetime.today().replace(
            tzinfo=timezone.utc) + timedelta(days=(7 - datetime.today().weekday()))
        for day in [x for x in BusinessHours.DayOfWeek.values]:
            if day == BusinessHours.DayOfWeek.SUNDAY:
                BusinessHoursFactory(workshop=workshop, day_of_week=day, is_open=False,
                                     from_hour=time(hour=0), to_hour=time(hour=0))
            else:
                BusinessHoursFactory(workshop=workshop, day_of_week=day, is_open=True,
                                     from_hour=time(hour=random.randint(6, 8)),
                                     to_hour=time(hour=random.randint(15, 17)))
        response = self.client.get(reverse('workshop-reservation-dates',
                                           kwargs={
                                               'pk': workshop.id,
                                               'date': datetime.strftime(next_monday, '%Y-%m-%d'),
                                               'position_id': position.id,
                                           }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated(self):
        """Unauthenticated users can only use get method on API."""
        workshop = WorkshopFactory()
        self.client.credentials(HTTP_AUTHORIZATION='')

        with self.subTest('PUT page'):
            response = self.client.put(reverse('workshop-detail', kwargs={'pk': workshop.id}), {
                'name': 'string',
                'city': 'string',
                'zip_code': 'string',
                'street': 'string',
                'image': 'string',
                'phone_number': 'string',
                'page': 'string',
            })
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest('GET'):
            """GET a detail page for a Workshop."""
            workshop = WorkshopFactory()
            response = self.client.get(self.get_detail_url(workshop.id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], workshop.name)


class BusinessHoursViewSetTestCase(APITestCase):
    """Business hours view set test."""

    def setUp(self):
        """Workshop owner user setup."""
        self.data = {
            'email': 'user@user.pl',
            'password': 'ZAQ!2wsx',
        }
        self.user = UserFactory(email=self.data['email'])
        self.user.set_password(self.data['password'])
        self.workshopowner = WorkshopOwnerFactory(user=self.user)
        self.user.save()
        jwt_get_token_url = reverse('jwt-create')
        response = self.client.post(jwt_get_token_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.workshop = WorkshopFactory(owner=self.workshopowner)
        for day in [x for x in BusinessHours.DayOfWeek.values]:
            if day == 'sunday':
                BusinessHoursFactory(workshop=self.workshop, day_of_week=day, is_open=False,
                                     from_hour=time(hour=0), to_hour=time(hour=0))
            else:
                BusinessHoursFactory(workshop=self.workshop, day_of_week=day, is_open=True,
                                     from_hour=time(hour=random.randint(6, 8)),
                                     to_hour=time(hour=random.randint(15, 17)))

    def test_get_list(self):
        """GET a list page of Business hours."""
        response = self.client.get(reverse('businesshours-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        """Partial update for Business hours."""
        data = self.client.get(reverse('businesshours-list'))
        response = self.client.patch(reverse('businesshours-detail',
                                             kwargs={'pk': data.data[0]['id']}), {
                                         'from_hour': '08:00:00',
                                         'to_hour': '15:00:00',
                                     })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated(self):
        """Unauthenticated users may not use the API."""
        self.client.credentials(HTTP_AUTHORIZATION='')

        with self.subTest('PUT page'):
            """PUT test Reservation."""
            response = self.client.put(reverse('businesshours-detail',
                                               kwargs={'pk': self.workshop.id}), {
                                           'day_of_week': 'monday',
                                           'from_hour': 'string',
                                           'to_hour': 'string',
                                           'is_open': True,
                                       })
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest('GET list'):
            """GET a list page for a Reservation."""
            response = self.client.get(reverse('businesshours-list'))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ServicePriceListViewSetTestCase(APITestCase):
    """Service price list view set test."""

    def setUp(self):
        """Workshop owner user setup."""
        self.data = {
            'email': 'user@user.pl',
            'password': 'ZAQ!2wsx',
        }
        self.user = UserFactory(email=self.data['email'])
        self.user.set_password(self.data['password'])
        self.workshopowner = WorkshopOwnerFactory(user=self.user)
        self.user.save()
        jwt_get_token_url = reverse('jwt-create')
        response = self.client.post(jwt_get_token_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.workshop = WorkshopFactory(owner=self.workshopowner)

    def test_get_list(self):
        """GET a list page of Business hours."""
        ServicesPriceListFactory.create_batch(random.randrange(2, 8))
        response = self.client.get(reverse('servicespricelist-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        """Update service."""
        service_price_list = ServicesPriceListFactory(workshop=self.workshop)
        response = self.client.patch(reverse('servicespricelist-detail',
                                             kwargs={'pk': service_price_list.id}),
                                     data={
                                         'name': 'New name',
                                         'price': '20.00',
                                     }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        """Create new service."""
        response = self.client.post(reverse('servicespricelist-list'), {
            'workshop': self.workshop.id,
            'name': 'Cleaning',
            'price': '100.00',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
