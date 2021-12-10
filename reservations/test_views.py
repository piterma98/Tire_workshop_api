"""Reservations test views."""
# Standard Library
import random
from datetime import datetime
from datetime import time
from datetime import timedelta

# 3rd-party
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Project
from accounts.factories import UserFactory
from accounts.factories import WorkshopCustomerFactory
from accounts.factories import WorkshopOwnerFactory
from reservations.factories import ReservationFactory
from reservations.models import Reservation
from workshop.factories import BusinessHoursFactory
from workshop.factories import WorkshopFactory
from workshop.factories import WorkshopPositionFactory


class ReservationsViewSetTestCase(APITestCase):
    """Reservations view set test."""

    def setUp(self):
        """User setup."""
        self.data = {
            'email': 'user@user.pl',
            'password': 'ZAQ!2wsx',
        }
        self.user = UserFactory(email=self.data['email'])
        self.user.set_password(self.data['password'])
        self.customer = WorkshopCustomerFactory(user=self.user)
        self.user.save()
        self.jwt_get_token_url = reverse('jwt-create')
        response = self.client.post(self.jwt_get_token_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.data2 = {
            'email': 'user2@user.pl',
            'password': 'ZAQ!2wsx',
        }
        self.owner_user = UserFactory(email=self.data2['email'])
        self.owner_user.set_password(self.data2['password'])
        self.owner = WorkshopOwnerFactory(user=self.owner_user)
        self.workshop = WorkshopFactory(owner=self.owner)
        self.owner_user.save()
        self.position = WorkshopPositionFactory(workshop=self.workshop)
        self.date = datetime.today() + timedelta(days=1)
        self.bussineshours = BusinessHoursFactory(
            workshop=self.workshop, day_of_week=self.date.strftime('%A').lower(),
            is_open=True, from_hour=time(hour=7), to_hour=time(hour=15))

    def test_get_reservation_dates(self):
        """GET a list of reservation dates."""
        response = self.client.get(reverse('workshop-reservation-dates', kwargs={
            'pk': self.workshop.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'position_id': self.position.id,
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_reservation_date(self):
        """POST a reservation date."""
        date = self.client.get(reverse('workshop-reservation-dates', kwargs={
            'pk': self.workshop.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'position_id': self.position.id,
        }))
        random_date = date.data[random.randrange(len(date.data))]
        response = self.client.post(reverse('reservation-list'), {
            'workshop': self.workshop.id,
            'workshop_position': self.position.id,
            'date': random_date,
            'car_license_plate': 'TEST123',
            'car_type': 'sedan',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_bad_reservation_date(self):
        """POST a non existing reservation date."""
        response = self.client.post(reverse('reservation-list'), {
            'workshop': self.workshop.id,
            'date': datetime.now(),
            'workshop_position': self.position.id,
            'car_license_plate': 'TEST123',
            'car_type': 'sedan',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_reservation_list(self):
        """GET a list of reservations."""
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_change_owner(self):
        """Owner can change reservation status."""
        response = self.client.post(self.jwt_get_token_url, self.data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        ReservationFactory(workshop=self.workshop, customer=self.customer,
                           workshop_position=self.position)
        reservations = Reservation.objects.filter(workshop__owner=self.owner)
        random_reservation = reservations[random.randrange(len(reservations))]
        response = self.client.patch(
            reverse('reservation-workshop-update', kwargs={'pk': random_reservation.id}),
            {'status': 'done'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated(self):
        """Unauthenticated users may not use reservations endpoint."""
        self.client.credentials(HTTP_AUTHORIZATION='')

        with self.subTest('GET list'):
            date = datetime.today() + timedelta(days=1)
            response = self.client.get(reverse('workshop-reservation-dates', kwargs={
                'pk': self.workshop.id,
                'date': date.strftime('%Y-%m-%d'),
                'position_id': self.position.id,
            }))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest('POST'):
            response = self.client.post(reverse('reservation-list'), {
                'workshop': self.workshop.id,
                'date': datetime.now(),
                'car_license_plat': 'TEST123',
                'car_type': 'van',
            }, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
