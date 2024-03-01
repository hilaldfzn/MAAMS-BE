from django.test import TestCase
from validator.models.question import Question
from authentication.models import CustomUser
import uuid

class QuestionModelTest(TestCase):
    
    def setUp(self):
        """
        setUp Question object
        """
        self.user_uuid = uuid.uuid4()
        self.valid_user = CustomUser.objects.create(
            uuid=self.user_uuid,
            username="test",
            password="test-password",
            email="test@email.com"
        )
        self.question_uuid = uuid.uuid4()
        
        Question.objects.create(
            user=self.valid_user,
            id=self.question_uuid,
            question='pertanyaan',
            mode=Question.ModeChoices.PRIBADI
        )
    
    def test_question(self):
        question = Question.objects.get(id=self.question_uuid)
        self.assertIsNotNone(question)        
        self.assertEqual(question.user.uuid, self.user_uuid)
        self.assertEqual(question.question, 'pertanyaan')
        self.assertEqual(question.mode, Question.ModeChoices.PRIBADI)
        