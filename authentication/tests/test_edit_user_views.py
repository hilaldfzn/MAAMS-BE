# tests/test_edit_user.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import CustomUser 
from authentication.serializers import EditUserSerializer 

class EditUserTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client = APIClient()

    def test_edit_user_valid_data(self):
        # Prepare valid data for editing user
        valid_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Send PATCH request to edit user
        response = self.client.patch('/api/v1/auth/update/', data=valid_data)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh user instance from the database
        self.user.refresh_from_db()

        # Check if user information has been updated
        self.assertEqual(self.user.username, valid_data['username'])
        self.assertEqual(self.user.email, valid_data['email'])
        self.assertTrue(self.user.check_password(valid_data['password']))

    def test_edit_user_partial_data(self):
        # Prepare partial data
        partial_data = {
            'username': 'newusername',
            # Missing 'email' and 'password'
        }

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Send PATCH request with partial data
        response = self.client.patch('/api/v1/auth/update/', data=partial_data)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the updated username and email are returned
        self.assertEqual(response.data['username'], partial_data['username'])
        self.assertEqual(response.data['email'], self.user.email)

    def test_edit_user_unauthenticated(self):
        # Prepare valid data for editing user
        valid_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }

        # Send PATCH request without authentication
        response = self.client.patch('/api/v1/auth/update/', data=valid_data)

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_user_invalid_data_type(self):
        # Prepare invalid data (non-integer value for 'num' field)
        invalid_data = {
            'username': 123,
            'email': 1111,
            'password': '5555',
        }

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Send PATCH request with invalid data
        response = self.client.patch('/api/v1/auth/update/', data=invalid_data)

        # Check if the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
