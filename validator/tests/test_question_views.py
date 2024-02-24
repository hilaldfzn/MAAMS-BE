import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from validator.models.question import Question
from validator.serializers import QuestionResponse, QuestionRequest, QuestionUpdateModeRequest
import uuid

class QuestionViewTest(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.question_uuid = uuid.uuid4()
        # TODO: Add user to the field
        self.valid_data = {'question': 'Test question', 'mode': 'pribadi'}
        self.invalid_data_missing = {'question': 'Test question', 'mode': ''}
        self.invalid_data = {'question': 'Test question', 'mode': 'bohong'}
        self.valid_data_patch = {'id': self.question_uuid, 'mode': 'pengawasan'}
        self.invalid_data_patch = {'id': self.question_uuid, 'mode': 'bohong'}
        self.invalid_data_patch_missing = {'id': self.question_uuid, 'mode': ''}

        Question.objects.create(
            # TODO: Add user to the field
            id=self.question_uuid, question='pertanyaan1', mode='Pribadi'
        )
        
    def test_get_question(self):
        url = reverse('validator:get_question', kwargs={'pk': self.question_uuid})
        response = self.client.get(url)
        question = Question.objects.get(id=self.question_uuid)
        serializer = QuestionResponse(question)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_non_existing_question(self):
        non_existing_pk = uuid.uuid4()
        url = reverse('validator:get_question', kwargs={'pk': non_existing_pk})
        response = self.client.get(url)
        
        # TODO: Add user to the field
        self.assertEqual(response.data['detail'], "Analisis tidak ditemukan")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_post_question(self):
        url = reverse('validator:create_question')
        response = self.client.post(url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.get(id=response.data['id']).question, 'Test question')
    
    def test_post_question_missing_value(self):
        url = reverse('validator:create_question')
        response = self.client.post(url, self.invalid_data_missing, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_post_question_invalid_value(self):
        url = reverse('validator:create_question')
        response = self.client.post(url, self.invalid_data, format='json')
        serializer = QuestionRequest(data=self.invalid_data)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_question(self):
        url = reverse('validator:patch_question')
        response = self.client.put(url, self.valid_data_patch, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_question = Question.objects.get(pk=self.question_uuid)
        self.assertEqual(updated_question.mode, "Pribadi")
        
    def test_patch_question_invalid_value(self):
        url = reverse('validator:patch_question')
        response = self.client.put(url, self.invalid_data_patch, format='json')
        
        serializer = QuestionUpdateModeRequest(data=self.invalid_data_patch)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_patch_question_missing_value(self):
        url = reverse('validator:patch_question')
        response = self.client.put(url, self.invalid_data_patch, format='json')
        
        serializer = QuestionUpdateModeRequest(data=self.invalid_data_patch)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)