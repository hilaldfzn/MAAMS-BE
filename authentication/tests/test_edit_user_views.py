

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import CustomUser 
from authentication.serializers import EditUserSerializer 

class EditUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client = APIClient()

    def test_edit_user_valid_data(self):
        valid_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=valid_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, valid_data['username'])
        self.assertEqual(self.user.email, valid_data['email'])
        self.assertTrue(self.user.check_password(valid_data['password']))

    def test_edit_user_partial_data(self):
        partial_data = {
            'username': 'newusername',

        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=partial_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['username'], partial_data['username'])
        self.assertEqual(response.data['email'], self.user.email)

    def test_edit_user_unauthenticated(self):
        valid_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }

        response = self.client.patch('/api/v1/auth/update/', data=valid_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_user_invalid_data_type(self):
        invalid_data = {
            'username': 123,
            'email': 1111,
            'password': '5555',
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
