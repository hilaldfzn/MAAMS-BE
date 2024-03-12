import openai
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from validator.dataclasses.create_cause import CreateCauseDataClass
from validator.models import question
from validator.models.causes import Causes
from validator.services import question
from authentication.models import CustomUser
from validator.exceptions import NotFoundRequestException
import uuid
class CausesService:
    def api_call(self, prompt: str):
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=1,  
                n=3,           
                temperature=0  
            )
        answer = response.choices[0].text.strip()

        return answer

    def rca(self, user: CustomUser, question_id: uuid, row: int):
        return


    def create(user: CustomUser, question_id: uuid, cause: str, row: int, column: int, mode: str) -> CreateCauseDataClass:
        cause = Causes.objects.create(
            problem=question.Question.objects.get(pk=question_id),
            row=row,
            column=column,
            mode=mode,
            cause=cause
        )
        return CreateCauseDataClass(
            question_id=cause.problem.id,
            id=cause.id,
            row=cause.row,
            column=cause.column,
            mode=cause.mode,
            cause=cause.cause
        )

    def get(user: CustomUser, question_id: uuid, pk: uuid) -> CreateCauseDataClass:
        try:
            cause = Causes.objects.get(pk=pk, problem_id = question_id)
            return CreateCauseDataClass(
                question_id=question_id,
                id=cause.id,
                row=cause.row,
                column=cause.column,
                mode=cause.mode,
                cause=cause.cause
            )
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Sebab tidak ditemukan")

    def update(user: CustomUser, question_id: uuid, pk: uuid, cause: str) -> CreateCauseDataClass:
        try:
            causes = Causes.objects.get(problem_id = question_id, pk=pk)
            causes.cause = cause
            causes.save()

            return CreateCauseDataClass(
                question_id=question_id,
                id=causes.id,
                row=causes.row,
                column=causes.column,
                mode=causes.mode,
                cause=causes.cause
            )
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Sebab tidak ditemukan")