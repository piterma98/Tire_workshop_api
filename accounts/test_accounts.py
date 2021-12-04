"""Test accounts."""
# Django
from django.urls import reverse

# 3rd-party
from rest_framework import status
from rest_framework.test import APITestCase

# Local
from .models import CustomUser
from .models import WorkshopCustomer


class AccountTests(APITestCase):
    """Accounts tests."""

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
        token_url = reverse('jwt-create')
        token_response = self.client.post(token_url, data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK, token_response.content)
        token = token_response.data['access']
        token_verify_url = reverse('jwt-verify')
        token_verify_response = self.client.post(token_verify_url, {'token': token}, format='json')
        self.assertEqual(token_verify_response.status_code, status.HTTP_200_OK)
