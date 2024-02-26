import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer


class LoginViewTest(APITestCase):

    maxDiff = None

    def setUp(self):
        """
        Setup client & valid user credentials to log in with.
        """
        self.url = reverse('authentication:login')
        self.content_type = 'application/json'
        self.valid_user = CustomUser(
            username="test-username",
            email="test@email.com"
        )
        self.valid_user.set_password('test-password')
        self.valid_user.save()
        self.valid_credentials = {
            'username': 'test-username',
            'password': 'test-password'
        }
        self.invalid_credentials = {
            'username': 'dummy-username',
            'password': 'dummy-password'
        }
        refresh = RefreshToken.for_user(self.valid_user)
        serializer = CustomUserSerializer(self.valid_user)
        self.valid_payload = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'data': serializer.data,
            'detail': 'Successfully logged in.'
        }
        self.invalid_payload = {
            'detail': 'Incorrect username or password.'
        }
        
    def test_login_with_valid_credentials_returns_access_token(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_credentials),
            content_type=self.content_type
        )
        self.assertEqual(
            type(response.data['access_token']), type(self.valid_payload['access_token']))
        self.assertEqual(
            type(response.data['refresh_token']), type(self.valid_payload['refresh_token']))
        self.assertEqual(
            response.data['data'], self.valid_payload['data'])
        self.assertEqual(
            response.data['detail'], self.valid_payload['detail'])
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)
  
    def test_login_with_active_tokens_returns_new_tokens(self):
        self.client.post(
            self.url,
            data=json.dumps(self.valid_credentials),
            content_type=self.content_type
        )
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_credentials),
            content_type=self.content_type
        )
        self.assertEqual(
            type(response.data['access_token']), type(self.valid_payload['access_token']))
        self.assertEqual(
            type(response.data['refresh_token']), type(self.valid_payload['refresh_token']))
        self.assertEqual(
            response.data['data'], self.valid_payload['data'])
        self.assertEqual(
            response.data['detail'], self.valid_payload['detail'])
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)
        
    def test_login_with_invalid_credentials_raises_exception(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_credentials),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_valid_user_password_mismatch(self):
        response = self.client.post(
            self.url,
            data=json.dumps({
                "username": "test-username",
                "password": "invalid-password"
            }),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_missing_params_raises_exception(self):
        response = self.client.post(
            self.url,
            data=json.dumps({ "username": "malformed-request" }),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_http_method_raises_exception(self):
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            