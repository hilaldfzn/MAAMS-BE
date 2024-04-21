from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TriggerErrorTests(APITestCase):
    def test_division_by_zero(self):
        url = reverse('trigger-error')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
