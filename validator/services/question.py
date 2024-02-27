from validator.models.question import Question
from authentication.models import CustomUser
import uuid
from django.core.exceptions import ObjectDoesNotExist
from validator.exceptions import NotFoundRequestException, ForbiddenRequestException
from validator.dataclasses.create_question import CreateQuestionDataClass 

class QuestionService():
    def create(user: CustomUser, question: str, mode: str):
        questionObject = Question.objects.create(user=user, question=question, mode=mode)
        
        return CreateQuestionDataClass(
            username = questionObject.user.username,
            id = questionObject.id,
            question = questionObject.question,
            created_at = questionObject.created_at,
            mode = questionObject.mode
        )
    
    def get(user:CustomUser, pk:uuid):
        try:
            question = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Analisis tidak ditemukan")
        
        user_id = question.user.uuid
        
        if user.uuid != user_id:
            if user.is_superuser == True and question.mode == Question.ModeChoices.PENGAWASAN:
                return question
        else:
            raise ForbiddenRequestException("User not permitted to view this resource")

    def update_mode(user:CustomUser, mode:str, pk:uuid):
        try:
            question = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Analisis tidak ditemukan")
        
        user_id = question.user.uuid

        if user.uuid != user_id:
            raise ForbiddenRequestException("User not permitted to update this resource")
        
        question.mode = mode
        question.save()
        
        return question