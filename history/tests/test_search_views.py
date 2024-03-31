from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from history.enums import HistoryType
from rest_framework_simplejwt.tokens import AccessToken
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime
from history.views.search_bar import SearchHistory
from history.services.search_bar import SearchBarHistoryService

class TestSearchHistory(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = SearchHistory.as_view()
        self.user = mixer.blend('authentication.CustomUser')
        self.access_token = AccessToken.for_user(self.user)
        self.access_token = AccessToken.for_user(self.user)
        self.keyword = 'test'
        self.url = '/api/v1/history/search/'

    def test_search_history_last_week_positive(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        with patch.object(SearchBarHistoryService, 'filter') as mock_filter:
            mock_filter.return_value = [
                        {
                            'id': '1',
                            'question': 'Test question',
                            'created_at': '2022-01-01T00:00:00Z',
                            'mode': HistoryType.LAST_WEEK.value
                        }
                    ]       
            response = self.client.get(self.url, {'mode': HistoryType.LAST_WEEK.value, 'keyword': self.keyword})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data['results']), 1)

    def test_search_history_older_positive(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        with patch.object(SearchBarHistoryService, 'filter') as mock_filter:
            mock_filter.return_value = [
                        {
                            'id': '1',
                            'question': 'Test question',
                            'created_at': '2022-01-01T00:00:00Z',
                            'mode': HistoryType.OLDER.value
                        }
                    ]            
            response = self.client.get(self.url, {'mode': HistoryType.OLDER.value, 'keyword': self.keyword})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data['results']), 1)

    def test_search_history_invalid_mode_negative(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url, {'mode': 'invalid_mode', 'keyword': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_history_missing_mode_negative(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url, {'keyword': self.keyword})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_history_invalid_user_negative(self):
        response = self.client.get(self.url, {'mode': HistoryType.LAST_WEEK.value, 'keyword': self.keyword})
        self.assertEqual(response.status_code, 401)

    def test_search_history_no_results_negative(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url, {'mode': HistoryType.LAST_WEEK.value, 'keyword': self.keyword})

        with patch.object(SearchBarHistoryService, 'filter') as mock_filter:
            mock_filter.return_value = []
            self.assertEqual(response.status_code, 404)
