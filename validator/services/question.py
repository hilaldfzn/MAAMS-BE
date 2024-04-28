from typing import List
import uuid
from datetime import (
    datetime, timedelta
)

from django.core.exceptions import ObjectDoesNotExist
from authentication.models import CustomUser

from validator.enums import HistoryType
from validator.constants import ErrorMsg
from validator.dataclasses.create_question import CreateQuestionDataClass 
from validator.enums import QuestionType
from validator.exceptions import (
    NotFoundRequestException, ForbiddenRequestException, InvalidTimeRangeRequestException, EmptyTagException, ValueNotUpdatedException
)
from validator.models.causes import Causes
from validator.models.question import Question
from validator.models.tag import Tag
from validator.serializers import Question


class QuestionService():
    
    def create(self, user: CustomUser, title:str, question: str, mode: str, tags: List[str]):
        if not tags:
            raise EmptyTagException(ErrorMsg.EMPTY_TAG)
        tags_object = []
        
        for tag_name in tags:
            try:
                tag = Tag.objects.get(name=tag_name)
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name=tag_name)
            finally:
                tags_object.append(tag)
                
        question_object = Question.objects.create(user=user, title=title, 
                                                  question=question, mode=mode)

        for tag in tags_object:
            question_object.tags.add(tag)
        
        tags = [tag.name for tag in question_object.tags.all()]

        return CreateQuestionDataClass(
            username = question_object.user.username,
            id = question_object.id,
            title=question_object.title,
            question = question_object.question,
            created_at = question_object.created_at,
            mode = question_object.mode,
            tags=tags
        )
    
    def get(self, user:CustomUser, pk:uuid):
        try:
            question_object = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException(ErrorMsg.NOT_FOUND)
        
        user_id = question_object.user.uuid
        
        if question_object.mode == Question.ModeChoices.PRIBADI and user.uuid != user_id:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_GET)

        if question_object.mode == Question.ModeChoices.PENGAWASAN and not (user.is_staff or user.is_superuser or user.uuid == user_id):
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_GET)
        
        response = self.make_question_response([question_object])

        return response[0]
    
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
    
    def get_recent(self, user: CustomUser):
        recent_question = Question.objects.filter(user=user).order_by('-created_at').first()

        if (recent_question):
            response = self.make_question_response([recent_question])
            response = response[0]
        else:
            response = recent_question

        return response
    
    def get_privileged(self, user: CustomUser, time_range: str, keyword: str):
        """
        Return a list for pengawasan questions by keyword and time range for privileged users.
        """
        # allow only superuser/staff (admins) to access resource
        if not user.is_superuser or not user.is_staff:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_GET)
        
        if not keyword:
            keyword = ''
            
        today_datetime = datetime.now()
        last_week_datetime = today_datetime - timedelta(days=7)
        
        # get all publicly available questions of mode "PENGAWASAN", depending on time range
        match time_range:
            case HistoryType.LAST_WEEK.value:
                questions = Question.objects.filter(question__icontains=keyword,
                                                    mode=QuestionType.PENGAWASAN.value,
                                                    created_at__range=[last_week_datetime, today_datetime]
                                                    ).order_by('-created_at')
            case HistoryType.OLDER.value:
                questions = Question.objects.filter(question__icontains=keyword,
                                                    mode=QuestionType.PENGAWASAN.value,
                                                    created_at__lt=last_week_datetime
                                                    ).order_by('-created_at')
            case _:
                raise InvalidTimeRangeRequestException(ErrorMsg.INVALID_TIME_RANGE)    
        response = self.make_question_response(questions)

        return response
    
    def get_matched(self, user: CustomUser, time_range: str, keyword: str):
        """
        Returns a list of matched questions corresponding to a specified user.
        """

        today_datetime = datetime.now()
        last_week_datetime = today_datetime - timedelta(days=7)
        
        # get all publicly available questions of mode "PENGAWASAN", depending on time range
        if time_range == HistoryType.LAST_WEEK.value:
            questions = Question.objects.filter(user=user, created_at__range=[last_week_datetime, today_datetime],
                                                question__icontains=keyword,
                                                ).order_by('-created_at')
        elif time_range == HistoryType.OLDER.value:
            questions = Question.objects.filter(user=user, created_at__lt=last_week_datetime,
                                                question__icontains=keyword,
                                                ).order_by('-created_at')
        else:
            raise InvalidTimeRangeRequestException(ErrorMsg.INVALID_TIME_RANGE)
             

        # get all questions filtered by user
        response = self.make_question_response(questions)

        return response

    def update_question(self, user: CustomUser, pk: uuid, **fields):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise NotFoundRequestException(ErrorMsg.NOT_FOUND)
        
        if user.uuid != question.user.uuid:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_UPDATE)
        
        updated = False
        
        for field, new_value in fields.items():
            if getattr(question, field) != new_value:
                setattr(question, field, new_value)
                updated = True
        question.save()
            
        if not updated:
            raise ValueNotUpdatedException(ErrorMsg.VALUE_NOT_UPDATED)

        tags = [tag.name for tag in question.tags.all()]
        return CreateQuestionDataClass(
            username=question.user.username,
            id=question.id,
            title=question.title,
            question=question.question,
            created_at=question.created_at,
            mode=question.mode,
            tags=tags
        )
        
    def delete(self, user:CustomUser, pk:uuid):
        try:
            question_object = Question.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundRequestException(ErrorMsg.NOT_FOUND)
        
        user_id = question_object.user.uuid

        if user.uuid != user_id:
            raise ForbiddenRequestException(ErrorMsg.FORBIDDEN_DELETE)
        
        tags = [tag.name for tag in question_object.tags.all()]
        question_data = CreateQuestionDataClass(
            username = question_object.user.username,
            id = question_object.id,
            title=question_object.title,
            question = question_object.question,
            created_at = question_object.created_at,
            mode = question_object.mode,
            tags=tags
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
        if len(questions) == 0:
            return response
        for question in questions:
            tags = [tag.name for tag in question.tags.all()]
            item = CreateQuestionDataClass(
                username = question.user.username,
                id = question.id,
                title=question.title,
                question = question.question,
                created_at = question.created_at,
                mode = question.mode,
                tags=tags
            )
            response.append(item)
            
        return response
