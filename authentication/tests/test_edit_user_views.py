

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

    def test_edit_user_non_unique_username(self):
        CustomUser.objects.create_user(
            username='newusername',
            email='another@example.com',
            password='anotherpassword'
        )

        invalid_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['case_error'], 'This username is already in use.')

    def test_edit_user_non_unique_email(self):
        CustomUser.objects.create_user(
            username='anotheruser',
            email='newemail@example.com',
            password='anotherpassword'
        )

        invalid_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['case_error'], 'This email is already in use.')
        
    def test_edit_user_same_password(self):
        same_password_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'password': 'testpassword'
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=same_password_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['case_error'], 'New password cannot be the same as the current one.')
        
    def test_edit_user_same_username(self):
        same_username_data = {
            'username': self.user.username, 
            'email': 'newemail@example.com',
            'password': 'newpassword'
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=same_username_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['case_error'], 'New username cannot be the same as the current one.')

    def test_edit_user_same_email(self):
        same_email_data = {
            'username': 'newusername',
            'email': self.user.email,
            'password': 'newpassword'
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch('/api/v1/auth/update/', data=same_email_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['case_error'], 'New email cannot be the same as the current one.')


