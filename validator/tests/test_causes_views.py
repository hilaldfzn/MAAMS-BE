from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from validator.models.causes import Causes
from validator.models.question import Question
from authentication.models import CustomUser
import uuid

class CausesViewTest(APITestCase):
    def setUp(self):
        """
        Set Up objects
        """
        self.user1 = CustomUser.objects.create(
            username="test-username",
            email="test@email.com"
        )
        self.user2 = CustomUser.objects.create(
            username="test-username2",
            email="test2@email.com"
        )

        self.question_uuid1 = uuid.uuid4()
        self.question_uuid2 = uuid.uuid4()

        self.question1 = Question.objects.create(
            user=self.user1,
            id=self.question_uuid1,
            question='pertanyaan',
            mode=Question.ModeChoices.PRIBADI
        )

        self.question2 = Question.objects.create(
            user=self.user2,
            id=self.question_uuid2,
            question='pertanyaan',
            mode=Question.ModeChoices.PRIBADI
        )

        self.causes_uuid = uuid.uuid4()
        self.causes_uuid2 = uuid.uuid4()

        self.causes1 = Causes.objects.create(
            problem=self.question1,
            id=self.causes_uuid,
            row=1,
            column=1,
            mode=Causes.ModeChoices.PRIBADI,
            cause='cause'
        )

        self.causes2 = Causes.objects.create(
            problem=self.question2, 
            id=self.causes_uuid2,
            row=1,
            column=1,
            mode=Causes.ModeChoices.PRIBADI,
            cause='cause'
        )

        self.url_login = reverse('authentication:login')
        self.content_type_login = 'application/json'
        self.valid_credentials_login = {
            'username': 'test-username',
            'password': 'test-password'
        }

        response_login = self.client.post(
            self.url_login,
            data=self.valid_credentials_login,
            content_type=self.content_type_login,
        )

        access_token = response_login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
        self.post_url = 'validator:create_cause'
        self.get_url = 'validator:get_cause'
        self.put_url = 'validator:put_cause'

    def test_create_cause_positive(self):
        response = self.client.post(self.post_url, self.causes1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cause'], 'Test Cause')

    def test_create_cause_negative_missing_cause(self):
        self.invalid_data_missing_cause = {'problem': self.question_uuid, 'row': 1, 'column': 1, 'mode': Causes.ModeChoices.PRIBADI}
        response = self.client.post(self.post_url, self.invalid_data_missing_cause, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_forbidden_access(self):
        url = reverse(self.post_url, kwargs={'pk': str(self.causes_uuid2)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_cause_forbidden_access(self):
        url = reverse(self.get_url, kwargs={'pk': str(self.causes_uuid2)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_cause_forbidden_access(self):
        url = reverse(self.put_url, kwargs={'pk': str(self.causes_uuid2)})
        data = {'problem': self.question_uuid1, 'row': 1, 'column': 1, 'mode': Causes.ModeChoices.PRIBADI, 'cause': 'Updated Cause'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_cause_positive(self):
        url = reverse(self.get_url, kwargs={'pk': str(self.causes_uuid)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cause'], 'cause')

    def test_get_cause_negative_non_existing_cause(self):
        non_existing_pk = uuid.uuid4()
        url = reverse(self.get_url, kwargs={'pk': str(non_existing_pk)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_cause_positive(self):
        url = reverse(self.put_url, kwargs={'pk': str(self.causes_uuid)})
        data = {'problem': self.question_uuid1, 'row': 1, 'column': 1, 'mode': Causes.ModeChoices.PRIBADI, 'cause': 'Updated Cause'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cause'], 'Updated Cause')

    def test_put_cause_invalid_data(self):
        url = reverse(self.put_url, kwargs={'pk': str(self.causes_uuid)})
        invalid_data = {'problem': self.question_uuid1, 'row': 1, 'column': 1, 'mode': Causes.ModeChoices.PRIBADI, 'cause': ''}
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)