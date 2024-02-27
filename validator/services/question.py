from validator.models.question import Question
from authentication.models import CustomUser
import uuid

class QuestionService():
    def create_question(user_id: uuid, question: str, mode: str):
        user = CustomUser.objects.get(id=user_id)
        question = Question.objects.create(user=user, question=question, mode=mode)
        return question
    
    def get_question(pk):
        return ""

    def update_mode(mode:str, pk:uuid.uuid4):
      return ""