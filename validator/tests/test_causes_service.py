from django.test import TestCase
from unittest.mock import patch
from django.conf import settings
from validator.services.causes import CausesService

class TestCausesService(TestCase):
    @patch('openai.Completion.create')
    def test_api_call_positive(self, mock_completion_create):
        mock_completion_create.return_value.choices[0].text = "test response"

        service = CausesService()
        prompt = "test prompt"
        response = service.api_call(prompt)

        self.assertEqual(response, "test response")
        mock_completion_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=5,
            n=5,
            temperature=0.5
        )

    @patch('openai.Completion.create')
    def test_api_call_negative(self, mock_completion_create):
        mock_completion_create.side_effect = Exception("API call failed")

        service = CausesService()
        prompt = "" 
        with self.assertRaises(Exception):
            service.api_call(prompt)

    @patch('openai.Completion.create')
    def test_api_call_edge_case(self, mock_completion_create):
        mock_completion_create.return_value.choices[0].text = "!@#$%^&*()_+"

        service = CausesService()
        prompt = "!@#$%^&*()_+"
        response = service.api_call(prompt)

        self.assertEqual(response, "!@#$%^&*()_+")