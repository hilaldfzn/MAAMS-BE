from rest_framework.test import APITestCase
from rest_framework import status

class CustomPageNumberPaginationTest(APITestCase):

    def test_positive_pagination_default_parameters(self):
        response = self.client.get('/api/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_positive_pagination_custom_parameters(self):
        response = self.client.get('/api/history?p=2&count=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_positive_pagination_maximum_page_size(self):
        response = self.client.get('/api/history?p=1&count=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_negative_pagination_invalid_page_number(self):
        response = self.client.get('/api/history?p=0&count=4')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_pagination_invalid_count(self):
        response = self.client.get('/api/history?p=1&count=-2')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_pagination_count_exceeds_max_page_size(self):
        response = self.client.get('/api/history?p=1&count=10')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_pagination_invalid_query_parameters(self):
        response = self.client.get('/api/history?page=1&size=5')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_pagination_missing_count_parameter(self):
        response = self.client.get('/api/history?p=1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
