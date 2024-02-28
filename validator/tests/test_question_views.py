import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from validator.models.question import Question
from authentication.models import CustomUser
from validator.serializers import QuestionRequest, BaseQuestion
import uuid

class QuestionViewTest(APITestCase):
    def setUp(self):
        """
        Set Up objects
        """
        self.question_uuid = uuid.uuid4()
        self.question_uuid2 = uuid.uuid4()
        
        # users
        self.user1 = CustomUser(
            username="test-username",
            email="test@email.com"
        )
        self.user_uuid1 = self.user1.uuid
        self.user1.set_password('test-password')
        self.user1.save()

        self.user2 = CustomUser(
            username="test-username2",
            email="test2@email.com"
        )
        self.user_uuid2 = self.user2.uuid
        self.user2.set_password('test-password')
        self.user2.save()
        
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
        
        response_login = self.client.post(
            self.url_login,
            data=json.dumps(self.valid_credentials_login),
            content_type=self.content_type_login,
        )
        
        access_token = response_login.data['access_token']  # Extracting access token from login response
        
        # Set the token in the header for all subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
    def test_get_question(self):
        url = reverse('validator:get_question', kwargs={'pk': self.question_uuid})
        response = self.client.get(url)
        question = Question.objects.get(id=self.question_uuid)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(question.id)) 
        
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
        self.assertEqual(response.data['username'], 'test-username')
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
        response = self.client.put(url, self.valid_data_put, format='json')
        
        self.assertEqual(response.data['detail'], "User not permitted to update this resource")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)