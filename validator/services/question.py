import uuid
from datetime import (
    datetime, timedelta
)

from django.core.exceptions import ObjectDoesNotExist

from authentication.models import CustomUser

from history.enums import HistoryType

from validator.constants import ErrorMsg
from validator.dataclasses.create_question import CreateQuestionDataClass 
from validator.enums import QuestionType
from validator.exceptions import (
    NotFoundRequestException, ForbiddenRequestException
)
from validator.models.causes import Causes
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
            raise NotFoundRequestException(ErrorMsg.NOT_FOUND)
        
        user_id = question_object.user.uuid
        
        if question_object.mode == Question.ModeChoices.PRIBADI and user.uuid != user_id:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_GET)

        if question_object.mode == Question.ModeChoices.PENGAWASAN and not (user.is_superuser or user.uuid == user_id):
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_GET)

        return CreateQuestionDataClass(
            username = question_object.user.username,
            id = question_object.id,
            question = question_object.question,
            created_at = question_object.created_at,
            mode = question_object.mode
        )
    
    def get_all(self, user: CustomUser,time_range: str):
        """
        Returns a list of  all questions corresponding to a specified user.
        """

        today_datetime = datetime.now()
        last_week_datetime = today_datetime - timedelta(days=7)
        
        # get all publicly available questions of mode "PENGAWASAN", depending on time range
        match time_range:
            case HistoryType.LAST_WEEK.value:
                questions = Question.objects.filter(user=user, created_at__range=[last_week_datetime, today_datetime]
                                                    ).order_by('-created_at')
            case HistoryType.OLDER.value:
                questions = Question.objects.filter(user=user, created_at__lt=last_week_datetime
                                                    ).order_by('-created_at')
                
        # get all questions filtered by user
        response = self.make_question_response(questions)

        return response
    
    def get_all_privileged(self, user: CustomUser, time_range: str):
        """
        Returns a list of  all questions corresponding to a specified user.
        """
        # allow only superuser/staff (admins) to access resource
        if not user.is_superuser or not user.is_staff:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_GET)
        
        today_datetime = datetime.now()
        last_week_datetime = today_datetime - timedelta(days=7)
        
        # get all publicly available questions of mode "PENGAWASAN", depending on time range
        match time_range:
            case HistoryType.LAST_WEEK.value:
                questions = Question.objects.filter(mode=QuestionType.PENGAWASAN.value,
                                                    created_at__range=[last_week_datetime, today_datetime]
                                                    ).order_by('-created_at')
            case HistoryType.OLDER.value:
                questions = Question.objects.filter(mode=QuestionType.PENGAWASAN.value,
                                                    created_at__lt=last_week_datetime
                                                    ).order_by('-created_at')
        
        response = self.make_question_response(questions)

        return response

    def update_mode(self, user:CustomUser, mode:str, pk:uuid):
        try:
            question_object = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException(ErrorMsg.NOT_FOUND)
        
        user_id = question_object.user.uuid

        if user.uuid != user_id:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_UPDATE)
        
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
            raise NotFoundRequestException(ErrorMsg.NOT_FOUND)
        
        user_id = question_object.user.uuid

        if user.uuid != user_id:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_DELETE)
        
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
    
    """
    Utility functions.
    """
    def make_question_response(self, questions) -> list:
        response = []
        for question in questions:
            item = CreateQuestionDataClass(
                username = question.user.username,
                id = question.id,
                question = question.question,
                created_at = question.created_at,
                mode = question.mode
            )
            response.append(item)
        return response
