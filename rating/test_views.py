"""Rating view test."""

# 3rd-party
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Project
from accounts.factories import UserFactory
from accounts.factories import WorkshopCustomerFactory
from rating.factories import RatingFactory
from workshop.factories import WorkshopFactory


class RatingViewSetTestCase(APITestCase):
    """Rating view set test."""

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
        self.workshop_customer = WorkshopCustomerFactory(user=self.user)

    @classmethod
    def setUpTestData(cls):  # noqa: D102
        WorkshopFactory.create_batch(5)
        WorkshopCustomerFactory.create_batch(5)

    @staticmethod
    def get_detail_url(rating_id):
        """Get workshop url."""
        return reverse('rating-detail', kwargs={'pk': rating_id})

    def test_get(self):
        """GET a workshop detail."""
        rating = RatingFactory(customer=self.workshop_customer)
        response = self.client.get(self.get_detail_url(rating.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        """Get a list of ratings."""
        RatingFactory.create_batch(size=5, customer=self.workshop_customer)
        response = self.client.get(reverse('rating-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        """Post a new rating."""
        rating = RatingFactory.build()
        response = self.client.post(
            reverse('rating-list'),
            data={
                'workshop': rating.workshop.id,
                'rate': rating.rate,
                'description': rating.description,
            }, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch(self):
        """Patch existing rating."""
        existing_rating = RatingFactory(customer=self.workshop_customer)
        rating = RatingFactory.build()
        response = self.client.patch(
            self.get_detail_url(existing_rating.id),
            data={
                'rate': rating.rate,
                'description': rating.description,
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """Delete existing rating."""
        rating = RatingFactory(customer=self.workshop_customer)
        response = self.client.delete(self.get_detail_url(rating.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated(self):
        """Unauthenticated users may not use rating endpoint."""
        self.client.credentials(HTTP_AUTHORIZATION='')

        with self.subTest('GET'):
            rating = RatingFactory()
            response = self.client.get(self.get_detail_url(rating.id))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest('GET list'):
            response = self.client.get(reverse('rating-list'))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
