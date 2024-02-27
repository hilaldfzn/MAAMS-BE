import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from validator.models.question import Question
from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer
from validator.serializers import QuestionRequest, QuestionResponse, BaseQuestion
import uuid

class QuestionViewTest(APITestCase):
    def setUp(self):
        """
        Set Up objects
        """
        self.client = self.client_class()
        self.question_uuid = uuid.uuid4()
        self.question_uuid2 = uuid.uuid4()
        
        # users
        self.user_uuid1 = uuid.uuid4()
        self.user1 = CustomUser.objects.create(
            uuid=self.user_uuid1,
            username="test-username",
            password="test-password",
            email="test@email.com"
        )
        self.user_data1 = CustomUserSerializer(self.user1).data

        
        self.user_uuid2 = uuid.uuid4()
        self.user2 = CustomUser.objects.create(
            uuid=self.user_uuid2,
            username="test2",
            password="test-password",
            email="test2@email.com"
        )
        self.user_data2 = CustomUserSerializer(self.user2).data
        
        # valid data
        self.valid_data = {'question': 'Test question', 'mode': Question.ModeChoices.PRIBADI}
        self.valid_data_put = {'id': self.question_uuid, 'mode': Question.ModeChoices.PENGAWASAN}

        # invalid data for post
        self.invalid_data_missing = {'question': 'Test question', 'mode': ''}
        self.invalid_data = {'question': 'Test question', 'mode': 'invalid'}
        
        # invalid data for put
        self.invalid_data_put = {'id': self.question_uuid, 'mode': 'invalid'}
        self.invalid_data_put_missing = {'id': self.question_uuid, 'mode': ''}
        self.invalid_data_put_user = {'id': self.question_uuid2, 'mode': Question.ModeChoices.PENGAWASAN}

        """
        Question created by user 1
        """
        Question.objects.create(
            user=self.user1,
            id=self.question_uuid, 
            question='pertanyaan 1',
            mode=Question.ModeChoices.PRIBADI
        )
        
        """
        Question created by user 2
        """
        Question.objects.create(
            user=self.user2,
            id=self.question_uuid2, 
            question='pertanyaan 2',
            mode=Question.ModeChoices.PRIBADI
        )
        
        """
        User login
        """
        self.url_login = reverse('authentication:login')
        self.content_type_login = 'application/json'
        self.valid_credentials_login = {
            'username': 'test-username',
            'password': 'test-password'
        }
        
        self.client.post(
            self.url_login,
            data=json.dumps(self.valid_credentials_login),
            content_type=self.content_type_login
        )
        
    def test_get_question(self):
        url = reverse('validator:get_question', kwargs={'pk': self.question_uuid})
        response = self.client.get(url)
        question = Question.objects.get(id=self.question_uuid)
        serializer = QuestionResponse(data=response)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.id, question.id)
        
    def test_get_non_existing_question(self):
        non_existing_pk = uuid.uuid4()
        url = reverse('validator:get_question', kwargs={'pk': non_existing_pk})
        response = self.client.get(url)
        
        self.assertEqual(response.data['detail'], "Analisis tidak ditemukan")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_forbidden(self):
        url = reverse('validator:get_question', kwargs={'pk': self.question_uuid2})
        response = self.client.get(url)
        
        self.assertEqual(response.data['detail'], "User not permitted to view this resource")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_post_question(self):
        url = reverse('validator:create_question')
        response = self.client.post(url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.get(id=response.data['id']).question, 'Test question')
    
    def test_post_question_missing_value(self):
        url = reverse('validator:create_question')
        response = self.client.post(url, self.invalid_data_missing, format='json')
        serializer = QuestionRequest(data=self.invalid_data)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_post_question_invalid_value(self):
        url = reverse('validator:create_question')
        response = self.client.post(url, self.invalid_data, format='json')
        
        serializer = QuestionRequest(data=self.invalid_data)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_question(self):
        url = reverse('validator:put_question', kwargs={'pk': self.question_uuid})
        response = self.client.put(url, self.valid_data_put, format='json')
        
        updated_question = Question.objects.get(pk=self.question_uuid)
        serializer = QuestionResponse(data=response)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_question.mode, Question.ModeChoices.PENGAWASAN)
        
    def test_put_question_invalid_value(self):
        url = reverse('validator:put_question', kwargs={'pk': self.question_uuid})
        response = self.client.put(url, self.invalid_data_put, format='json')
        
        serializer = BaseQuestion(data=self.invalid_data_put)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_question_missing_value(self):
        url = reverse('validator:put_question', kwargs={'pk': self.question_uuid})
        response = self.client.put(url, self.invalid_data_put_missing, format='json')
        
        serializer = BaseQuestion(data=self.invalid_data_put_missing)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_nonexisting_question(self):
        non_existing_pk = uuid.uuid4()
        url = reverse('validator:put_question', kwargs={'pk': non_existing_pk})
        response = self.client.put(url, self.valid_data_put, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_forbidden(self):
        url = reverse('validator:put_question', kwargs={'pk': self.question_uuid2})
        response = self.client.put(url)
        
        self.assertEqual(response.data['detail'], "User not permitted to update this resource")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)