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

        self.question_uuid = uuid.uuid4()

        self.question = Question.objects.create(
            user=self.valid_user,
            id=self.question_uuid,
            question='pertanyaan',
            mode=Question.ModeChoices.PRIBADI
        )

        self.causes_uuid = uuid.uuid4()
        self.causes_uuid2 = uuid.uuid4()

        self.causes1 = Causes.objects.create(
            problem=self.question,
            id=self.causes_uuid,
            row=1,
            column=1,
            mode=Causes.ModeChoices.PRIBADI,
            cause='cause'
        )

        self.causes2 = Causes.objects.create(
            problem=self.question, 
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