import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import CustomUser


class RegisterViewTest(APITestCase):
    maxDiff = None

    def setUp(self):
        """
        Setup client & valid user credentials to register with.
        """
        self.url = reverse('authentication:register')
        self.content_type = 'application/json'
        self.valid_user_data = {
            'username': 'test-username',
            'email': 'test@email.com',
            'password': 'test-password',
            'password2': 'test-password'
        }
        self.invalid_user_data = {
            'username': 'test-username',
            'email': 'invalid-email',  # Email tidak valid
            'password': 'test-password',
            'password2': 'test-password'
        }
        self.missing_params_data = {
            'email': 'test@email.com',  # Parameter username tidak ada
            'password': 'test-password',
            'password2': 'test-password'
        }
    
    def test_register_with_mismatched_passwords_raises_exception(self):
        invalid_user_data = {
            'username': 'test-username',
            'email': 'test@email.com',
            'password': 'test-password1',  # Password berbeda
            'password2': 'test-password2'   # Password berbeda
        }
        response = self.client.post(
            self.url,
            data=json.dumps(invalid_user_data),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_with_valid_data_creates_user(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_user_data),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username=self.valid_user_data['username']).exists())
    
    def test_register_with_existing_username_raises_exception(self):
        # Membuat user dengan username yang sudah ada sebelumnya
        CustomUser.objects.create_user(
            username=self.valid_user_data['username'],
            email=self.valid_user_data['email'],
            password=self.valid_user_data['password']
        )
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_user_data),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_email_raises_exception(self):
        # Membuat user dengan email yang sudah ada sebelumnya
        CustomUser.objects.create_user(
            username='existing-user',
            email=self.valid_user_data['email'],  # Gunakan email yang sama
            password='existing-password'
        )
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_user_data),  # Gunakan data yang sama dengan email yang sudah ada
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    def test_register_with_invalid_data_raises_exception(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_user_data),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_missing_params_raises_exception(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.missing_params_data),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_invalid_http_method_raises_exception(self):
        response = self.client.delete(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)





