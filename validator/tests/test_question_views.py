from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from validator.models.question import Question
from validator.serializers import QuestionRequest, QuestionResponse
import uuid
from validator.models.question import Question

class QuestionViewTest(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.question_uuid = uuid.uuid4()

        # TODO: Add user to the field
        self.valid_data = {'question': 'Test question', 'mode': Question.ModeChoices.PRIBADI}
        self.invalid_data_missing = {'question': 'Test question', 'mode': ''}
        self.invalid_data = {'question': 'Test question', 'mode': 'bohong'}
        self.valid_data_put = {'mode': Question.ModeChoices.PENGAWASAN}
        self.invalid_data_put = {'id': self.question_uuid, 'mode': 'bohong'}
        self.invalid_data_put_missing = {'id': self.question_uuid, 'mode': ''}

        Question.objects.create(
            # TODO: Add user to the field
            id=self.question_uuid, question='pertanyaan1', mode=Question.ModeChoices.PRIBADI
        )
        
    def test_get_question(self):
        url = reverse('validator:get_question', kwargs={'pk': self.question_uuid})
        response = self.client.get(url)
        question = Question.objects.get(id=self.question_uuid)
        serializer = QuestionRequest(question)
        
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
        serializer = QuestionResponse(data=self.invalid_data)
        
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
        
        serializer = QuestionRequest(data=self.invalid_data_put)
        
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_question_missing_value(self):
        url = reverse('validator:put_question', kwargs={'pk': self.question_uuid})
        response = self.client.put(url, self.invalid_data_put, format='json')
            
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_nonexisting_question_(self):
        non_existing_pk = uuid.uuid4()
        url = reverse('validator:put_question', kwargs={'pk': non_existing_pk})
        response = self.client.put(url, self.valid_data_put, format='json')
            
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)