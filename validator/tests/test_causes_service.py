from django.test import TestCase
from unittest.mock import patch, Mock
from django.conf import settings
from validator.services.causes import CausesService
from validator.models.causes import Causes
from validator.models.question import Question
import uuid

class CausesServiceTest(TestCase):
    @patch('validator.services.causes.Anthropic')
    def test_api_call_positive(self, mock_anthropic):
        mock_client = Mock()
        correct_prompt = "\n\nHuman: Is 'Example cause' the cause of 'Example problem'? Answer using only True/False \n\nAssistant:"
        mock_client.completions.create.return_value = Mock(completion='True')
        mock_anthropic.return_value = mock_client

        service = CausesService()
        prompt = "Is 'Example cause' the cause of 'Example problem'? Answer using only True/False"
        response = service.api_call(prompt)

        self.assertTrue(response)
        mock_client.completions.create.assert_called_once_with(
            model="claude-2.1",
            max_tokens_to_sample=300,
            prompt=correct_prompt
        )

    @patch('validator.services.causes.Anthropic')
    def test_api_call_negative(self, mock_anthropic):
        mock_client = Mock()
        mock_client.completions.create.side_effect = Exception("API call failed")
        mock_anthropic.return_value = mock_client

        service = CausesService()
        prompt = "test prompt"
        with self.assertRaises(Exception):
            service.api_call(prompt)

    @patch('validator.services.causes.Anthropic')
    def test_api_call_forbidden_access(self, mock_anthropic):
        mock_client = Mock()
        mock_client.completions.create.side_effect = Exception("Unauthorized: Invalid API key")
        mock_anthropic.return_value = mock_client

        service = CausesService()
        prompt = "Test prompt"
        with self.assertRaises(Exception):
            service.api_call(prompt)
    
    def test_rca_row_1(self):
        question_id = uuid.uuid4()
        question = Question.objects.create(pk=question_id, question='Test question')
        cause1 = Causes.objects.create(problem=question, row=1, column=1, mode='PRIBADI', cause='Cause 1')
        cause2 = Causes.objects.create(problem=question, row=1, column=2, mode='PRIBADI', cause='Cause 2')
        
        with patch.object(CausesService, 'api_call', return_value=True):
            service = CausesService()
            service.validate(question_id)
        
        cause1.refresh_from_db()
        cause2.refresh_from_db()
        self.assertTrue(cause1.status)
        self.assertTrue(cause2.status)

    def test_rca_row_greater_than_1_with_prev_cause(self):
        question_id = uuid.uuid4()
        question = Question.objects.create(pk=question_id, question='Test question')

        Causes.objects.create(problem=question, row=1, column=1, mode='PRIBADI', cause='Cause 1')
        cause2 = Causes.objects.create(problem=question, row=2, column=1, mode='PRIBADI', cause='Cause 1')

        with patch.object(CausesService, 'api_call', return_value=True):
            service = CausesService()
            service.validate(question_id)

        cause2.refresh_from_db()

        self.assertTrue(cause2.status)