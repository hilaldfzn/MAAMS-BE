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
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens= 5,  # TODO: determine most optimal param
            n= 5,  # TODO: determine most optimal param
            temperature= 0.5  # TODO: determine most optimal param
        )
        answer = response.choices[0].text.strip()

        return answer

    def create(user: CustomUser, question_id: uuid, cause: str, row: int, column: int, mode: str) -> CreateCauseDataClass:
        cause = Causes.objects.create(
            problem= question.QuestionService.get(question_id),
            row=row,
            column=column,
            mode=mode,
            cause=cause
        )
        return CreateCauseDataClass(
            problem_id=cause.question.id,
            id=cause.id,
            row=cause.row,
            column=cause.column,
            mode=cause.mode,
            cause=cause.cause
        )

    def get(user: CustomUser, question_id: uuid, pk: int) -> CreateCauseDataClass:
        try:
            problem= question.QuestionService.get(question_id)
            cause = Causes.objects.get(pk=pk, problem=problem)
            return CreateCauseDataClass(
                problem_id=cause.problem_id,
                id=cause.id,
                row=cause.row,
                column=cause.column,
                mode=cause.mode,
                cause=cause.cause
            )
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Sebab tidak ditemukan")

    def update(user: CustomUser, question_id: uuid, cause_data: CreateCauseDataClass, pk: int) -> CreateCauseDataClass:
        try:
            problem= question.QuestionService.get(question_id)
            cause = Causes.objects.get(pk=pk, problem=problem)
            cause.row = cause_data.row
            cause.column = cause_data.column
            cause.mode = cause_data.mode
            cause.cause = cause_data.cause
            cause.save()
            return CreateCauseDataClass(
                problem_id=cause.problem_id,
                id=cause.id,
                row=cause.row,
                column=cause.column,
                mode=cause.mode,
                cause=cause.cause
            )
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Sebab tidak ditemukan")