import json
import uuid

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import CustomUser
from validator.models.question import Question
from validator.models.causes import Causes
from validator.serializers import (
    QuestionRequest, BaseQuestion
)

from django.core.exceptions import ObjectDoesNotExist

class QuestionViewTest(APITestCase):
    def setUp(self):
        """
        Set Up objects
        """
        self.question_uuid = uuid.uuid4()
        self.question_uuid2 = uuid.uuid4()
        self.question_uuid_super = uuid.uuid4()
        self.question_uuid_super2 = uuid.uuid4()
        
        self.user1 = CustomUser(
            username="test-username",
            email="test@email.com",
            is_superuser=True,
            is_staff=True 
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
        self.invalid_data_missing = {'question': 'Test question missing', 'mode': ''}
        self.invalid_data = {'question': 'Test question invalid', 'mode': 'invalid'}
        
        # invalid data for put
        self.invalid_data_put = {'id': self.question_uuid, 'mode': 'invalid'}
        self.invalid_data_put_missing = {'id': self.question_uuid, 'mode': ''}
        self.invalid_data_put_user = {'id': self.question_uuid2, 'mode': Question.ModeChoices.PENGAWASAN}
        
        # urls
        self.post_url = 'validator:create_question'
        self.get_url = 'validator:get_question'
        self.get_all_public_url = 'validator:get_question_public'
        self.put_url = 'validator:put_question'
        self.delete_url = 'validator:delete_question'

        """
        Question created by user 1
        """
        self.question1 = Question.objects.create(
            user=self.user1,
            id=self.question_uuid, 
            question='pertanyaan 1',
            mode=Question.ModeChoices.PRIBADI
        )
                
        self.causes_uuid = uuid.uuid4()
        Causes.objects.create(
            problem=self.question1,
            id=self.causes_uuid,
            row=1,
            column=1,
            mode=Causes.ModeChoices.PRIBADI,
            cause='cause',
            status=False
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
        Supervised Questions
        """
        self.question_super = Question.objects.create(
            user=self.user1,
            id=self.question_uuid_super, 
            question='pertanyaan supervised',
            mode=Question.ModeChoices.PENGAWASAN
        )
        
        self.question_super = Question.objects.create(
            user=self.user2,
            id=self.question_uuid_super2, 
            question='pertanyaan supervised',
            mode=Question.ModeChoices.PENGAWASAN
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
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
    def test_get_question(self):
        url = reverse(self.get_url, kwargs={'pk': self.question_uuid})
        response = self.client.get(url)
        question = Question.objects.get(id=self.question_uuid)
        
        causes_count = Causes.objects.filter(problem_id=self.question_uuid).count()
        self.assertEqual(causes_count, 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(question.id))

    # TODO: refactor tests to cover pagination cases
    def test_get_all_public_questions(self):
        # set user as superuser (for admin testing purposes)
        self.user1.is_superuser = True
        self.user1.is_staff = True
        self.user1.save()

        url = reverse(self.get_all_public_url)
        response = self.client.get(url)
        questions = Question.objects.filter(mode="PENGAWASAN")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), len(questions))

        # reset user status
        self.user1.is_superuser = False
        self.user1.is_staff = False
        self.user1.save()

    def test_get_all_public_questions_forbidden(self):
        # reset user status
        self.user1.is_superuser = False
        self.user1.is_staff = False
        self.user1.save()

        url = reverse(self.get_all_public_url)
        response = self.client.get(url)

        self.assertEqual(response.data['detail'], "Pengguna tidak diizinkan untuk melihat analisis ini.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_non_existing_question(self):
        non_existing_pk = uuid.uuid4()
        url = reverse(self.get_url, kwargs={'pk': non_existing_pk})
        response = self.client.get(url)
        
        self.assertEqual(response.data['detail'], "Analisis tidak ditemukan")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_forbidden(self):
        url = reverse(self.get_url, kwargs={'pk': self.question_uuid2})
        response = self.client.get(url)
        
        self.assertEqual(response.data['detail'], "Pengguna tidak diizinkan untuk melihat analisis ini.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_supervised_question(self):
        url = reverse(self.get_url, kwargs={'pk': self.question_uuid_super2})
        response = self.client.get(url)
        question = Question.objects.get(id=self.question_uuid_super2)
                
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(question.id)) 
        
    def test_post_question(self):
        url = reverse(self.post_url)
        response = self.client.post(url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'test-username')
        self.assertEqual(Question.objects.get(id=response.data['id']).question, 'Test question')
    
    def test_post_question_missing_value(self):
        url = reverse(self.post_url)
        response = self.client.post(url, self.invalid_data_missing, format='json')
        serializer = QuestionRequest(data=self.invalid_data)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_post_question_invalid_value(self):
        url = reverse(self.post_url)
        response = self.client.post(url, self.invalid_data, format='json')
        
        serializer = QuestionRequest(data=self.invalid_data)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_question(self):
        url = reverse(self.put_url, kwargs={'pk': self.question_uuid})
        response = self.client.put(url, self.valid_data_put, format='json')
        
        updated_question = Question.objects.get(pk=self.question_uuid)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_question.mode, Question.ModeChoices.PENGAWASAN)
        
    def test_put_question_invalid_value(self):
        url = reverse(self.put_url, kwargs={'pk': self.question_uuid})
        response = self.client.put(url, self.invalid_data_put, format='json')
        
        serializer = BaseQuestion(data=self.invalid_data_put)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_question_missing_value(self):
        url = reverse(self.put_url, kwargs={'pk': self.question_uuid})
        response = self.client.put(url, self.invalid_data_put_missing, format='json')
        
        serializer = BaseQuestion(data=self.invalid_data_put_missing)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_nonexisting_question(self):
        non_existing_pk = uuid.uuid4()
        url = reverse(self.put_url, kwargs={'pk': non_existing_pk})
        response = self.client.put(url, self.valid_data_put, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_forbidden(self):
        url = reverse(self.put_url, kwargs={'pk': self.question_uuid2})
        response = self.client.put(url, self.valid_data_put, format='json')
        
        self.assertEqual(response.data['detail'], "Pengguna tidak diizinkan untuk mengubah analisis ini.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_delete_question(self):
        url = reverse(self.delete_url, kwargs={'pk': self.question_uuid})
        response = self.client.delete(url)

        self.assertEqual(response.data['message'], "Analisis berhasil dihapus")
        self.assertEqual(uuid.UUID(response.data['deleted_question']['id']), self.question_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(ObjectDoesNotExist):
            Question.objects.get(pk=self.question_uuid)
        
        causes_count = Causes.objects.filter(problem_id=self.question_uuid).count()
        self.assertEqual(causes_count, 0)
        
    def test_delete_question_not_found(self):
        non_existing_pk = uuid.uuid4()
        url = reverse(self.delete_url, kwargs={'pk': non_existing_pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Analisis tidak ditemukan")
        
    def test_delete_question_forbidden(self):
        url = reverse(self.delete_url, kwargs={'pk': self.question_uuid2})
        response = self.client.delete(url)
                
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Pengguna tidak diizinkan untuk menghapus analisis ini.")

    def test_get_supervised_question_fail(self):
        valid_credentials_login2 = {
            'username': 'test-username2',
            'password': 'test-password'
        }
        
        response_login = self.client.post(
            self.url_login,
            data=json.dumps(valid_credentials_login2),
            content_type=self.content_type_login,
        )
        
        access_token = response_login.data['access_token']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse(self.get_url, kwargs={'pk': self.question_uuid_super})
        response = self.client.get(url)
                
        self.assertEqual(response.data['detail'], "Pengguna tidak diizinkan untuk melihat analisis ini.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_search_questions(self):
        search_url = reverse('validator:search_questions')

        search_query = 'pertanyaan'

        # Make a GET request to the search endpoint with the query parameter
        response = self.client.get(f'{search_url}?query={search_query}')

        # Verify that the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        search_results = response.data['payload'] 
        self.assertTrue(len(search_results) > 0)

        for question in search_results:
            self.assertIn(search_query.lower(), question['question'].lower())

    def test_search_questions_no_results(self):
        """
        Test searching for questions with a query that matches no questions.
        """
        search_url = reverse('validator:search_questions')  
        search_query = "nonexistent query"
        
        response = self.client.get(f"{search_url}?query={search_query}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 0, "Expected no questions to match the search query")

    def test_search_questions_forbidden(self):
        """
        Test searching for questions without proper permissions, if applicable.
        """
        self.client.logout()  
        
        search_url = reverse('validator:search_questions')  
        search_query = "example query"
        
        response = self.client.get(f"{search_url}?query={search_query}")
        self.assertNotEqual(response.status_code, status.HTTP_200_OK, "Expected search to be forbidden without proper permissions")
