import uuid

from django.core.exceptions import ObjectDoesNotExist

from authentication.models import CustomUser
from validator.dataclasses.create_question import CreateQuestionDataClass 
from validator.exceptions import (
    NotFoundRequestException, ForbiddenRequestException
)
from validator.models.question import Question
from validator.serializers import Question


class QuestionService():
    def create(self, user: CustomUser, question: str, mode: str):
        question_object = Question.objects.create(user=user, question=question, mode=mode)
        
        return CreateQuestionDataClass(
            username = question_object.user.username,
            id = question_object.id,
            question = question_object.question,
            created_at = question_object.created_at,
            mode = question_object.mode
        )
    
    def get(self, user:CustomUser, pk:uuid):
        try:
            question_object = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Analisis tidak ditemukan")
        
        user_id = question_object.user.uuid
        if user.uuid != user_id:
            raise ForbiddenRequestException("Pengguna tidak diizinkan untuk melihat analisis ini.")
                
        return CreateQuestionDataClass(
            username = question_object.user.username,
            id = question_object.id,
            question = question_object.question,
            created_at = question_object.created_at,
            mode = question_object.mode
        )
    
    def get_all(self, user: CustomUser) -> list[CreateQuestionDataClass]:
        """
        Returns a list of  all questions corresponding to a specified user.
        # TODO: core implementation
        # TODO: handle pagination
        """
        return []

    def update_mode(self, user:CustomUser, mode:str, pk:uuid):
        try:
            question_object = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Analisis tidak ditemukan")
        
        user_id = question_object.user.uuid

        if user.uuid != user_id:
            raise ForbiddenRequestException("Pengguna tidak diizinkan untuk mengubah analisis ini.")
        
        question_object.mode = mode
        question_object.save()
        
        return CreateQuestionDataClass(
            username = question_object.user.username,
            id = question_object.id,
            question = question_object.question,
            created_at = question_object.created_at,
            mode = question_object.mode
        )
    