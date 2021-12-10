"""Test accounts."""
# Django
from django.urls import reverse

# 3rd-party
from rest_framework import status
from rest_framework.test import APITestCase

# Local
from .factories import UserFactory
from .factories import WorkshopCustomerFactory
from .models import CustomUser
from .models import WorkshopCustomer


class AccountTests(APITestCase):
    """Accounts tests."""

    jwt_get_token_url = reverse('jwt-create')

    def test_create_account(self):
        """Test create user."""
        url = reverse('customuser-list')
        data = {'email': 'user123@example.com',
                'password': 'ZAQ!2wsx',
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(WorkshopCustomer.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, data['email'])

    def test_token_auth(self):
        """Test token auth."""
        register_url = reverse('customuser-list')
        data = {'email': 'user123@example.com',
                'password': 'ZAQ!2wsx',
                }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token_response = self.client.post(self.jwt_get_token_url, data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK, token_response.content)
        token = token_response.data['access']
        token_verify_url = reverse('jwt-verify')
        token_verify_response = self.client.post(token_verify_url, {'token': token}, format='json')
        self.assertEqual(token_verify_response.status_code, status.HTTP_200_OK)

    def test_user_type(self):
        """Test user type."""
        data = {
            'email': 'user2@user.pl',
            'password': 'ZAQ!2wsx',
        }
        user = UserFactory(email=data['email'])
        WorkshopCustomerFactory(user=user)
        user.set_password(data['password'])
        user.save()
        response = self.client.post(self.jwt_get_token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('customuser-me'))
        self.assertEqual(response.data['is_workshop_customer'], True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
