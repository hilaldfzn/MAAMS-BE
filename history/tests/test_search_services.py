from django.test import TestCase
from faker import Faker
from unittest.mock import patch
from datetime import datetime, timedelta
from mixer.backend.django import mixer
from authentication.models import CustomUser
from history.enums import HistoryType
from history.exceptions import InvalidModeRequestException
from validator.exceptions import NotFoundRequestException
from history.services.search_bar import SearchBarHistoryService

class TestSearchBarHistoryService(TestCase):
    def setUp(self):
        self.service = SearchBarHistoryService()
        self.fake = Faker()
        self.user = CustomUser.objects.create(username=self.fake.user_name())

    def test_filter_last_week_positive(self):
        last_week_questions = [
            mixer.blend('validator.Question', 
                        user=self.user, 
                        question=self.fake.sentence(), 
                        created_at=self.fake.date_time_between(start_date='-7d', end_date='now'))
            for _ in range(5)
        ]

        with patch.object(SearchBarHistoryService, 'filter') as mock_filter:
            mock_filter.return_value = last_week_questions
            result = self.service.filter(user=self.user, keyword=self.fake.word(), mode=HistoryType.LAST_WEEK.value)
            self.assertEqual(len(result), len(last_week_questions))

    def test_filter_older_positive(self):
        older_questions = [
            mixer.blend('validator.Question', user=self.user, question='Older question', created_at=datetime.now() - timedelta(days=9))
            for _ in range(5)
        ]
        
        with patch.object(SearchBarHistoryService, 'get_older') as mock_get_older:
            mock_get_older.return_value = older_questions
            result = self.service.filter(user=self.user, keyword='test', mode=HistoryType.OLDER.value)
            mock_get_older.assert_called_once_with(self.user, 'test', datetime.now() - timedelta(days=7))
            self.assertEqual(len(result), len(older_questions))

    def test_get_older_no_questions(self):
        result = self.service.get_older(self.user, 'test', datetime.now() - timedelta(days=7))
        self.assertQuerysetEqual(result, [])

    def test_filter_invalid_mode_negative(self):
        with self.assertRaises(InvalidModeRequestException):
            self.service.filter(user=self.user, keyword=self.fake.word(), mode='invalid_mode')

    def test_filter_not_found_negative(self):
        with self.assertRaises(NotFoundRequestException):
            self.service.filter(user=self.user, keyword=self.fake.word(), mode=HistoryType.LAST_WEEK.value)

    def test_filter_invalid_user_negative(self):
        with self.assertRaises(NotFoundRequestException):
            self.service.filter(user=None, keyword=self.fake.word(), mode=HistoryType.LAST_WEEK.value)

    def test_filter_invalid_keyword_negative(self):
        with self.assertRaises(NotFoundRequestException):
            self.service.filter(user=self.user, keyword=None, mode=HistoryType.LAST_WEEK.value)

    def test_filter_no_questions_negative(self):
        with self.assertRaises(NotFoundRequestException):
            self.service.filter(user=self.user, keyword=self.fake.word(), mode=HistoryType.LAST_WEEK.value)
