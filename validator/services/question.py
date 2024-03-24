from validator.models.causes import Causes
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
    not_found_message = "Analisis tidak ditemukan"
    
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
            raise NotFoundRequestException(QuestionService.not_found_message)
        
        user_id = question_object.user.uuid
        
        if question_object.mode == Question.ModeChoices.PRIBADI and user.uuid != user_id:
            raise ForbiddenRequestException("Pengguna tidak diizinkan untuk melihat analisis ini.")

        if question_object.mode == Question.ModeChoices.PENGAWASAN and not (user.is_superuser or user.uuid == user_id):
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
        # TODO: handle pagination
        """
        # allow only superuser/staff (admins) to access resource
        if not user.is_superuser or not user.is_staff:
            raise ForbiddenRequestException("Pengguna tidak diizinkan untuk melihat analisis ini.")
        # get all publicly available questions of mode "PENGAWASAN" 
        questions = Question.objects.filter(mode="PENGAWASAN")
        
        response = []
        for question in questions:
            item =  CreateQuestionDataClass(
                username = question.user.username,
                id = question.id,
                question = question.question,
                created_at = question.created_at,
                mode = question.mode
            )
            response.append(item)

        return response

    def search(self, user: CustomUser, search_query: str) -> list[CreateQuestionDataClass]:
        # TODO : Implement search functionality
        return []
    
    def update_mode(self, user:CustomUser, mode:str, pk:uuid):
        try:
            question_object = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException(QuestionService.not_found_message)
        
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
        
    def delete(self, user:CustomUser, pk:uuid):
        try:
            question_object = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException(QuestionService.not_found_message)
        
        user_id = question_object.user.uuid

        if user.uuid != user_id:
            raise ForbiddenRequestException("Pengguna tidak diizinkan untuk menghapus analisis ini.")
        
        question_data = CreateQuestionDataClass(
            username = question_object.user.username,
            id = question_object.id,
            question = question_object.question,
            created_at = question_object.created_at,
            mode = question_object.mode
        )
        related_causes = Causes.objects.filter(problem=question_object)
        related_causes.delete()
        question_object.delete()
        
        return question_data 