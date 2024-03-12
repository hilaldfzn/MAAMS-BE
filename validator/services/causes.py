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
import math
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

    def validate(self, question_id: uuid):
        max_row = Causes.objects.filter(problem_id=question_id).order_by('-row').values_list('row', flat=True).first()
        causes = Causes.objects.filter(problem_id=question_id, row=max_row)
        problem = question.Question.objects.get(pk=question_id)

        for cause in causes:
            if max_row == 1:
                prompt = f"Is '{cause.cause}' the cause of '{problem.question}'? Answer using True/False"
                if self.api_call(prompt):
                    cause.status = True
                    cause.save()
            else:
                prev_cause = Causes.objects.filter(problem_id=question_id, row=max_row-1, column=cause.column).first()
                if prev_cause and prev_cause.cause == cause.cause:
                    prompt = f"Is '{cause.cause}' the cause of '{prev_cause.cause}'? Answer using True/False"
                    if self.api_call(prompt):
                        cause.status = True
                        cause.save()


    def create(self, question_id: uuid, cause: str, row: int, column: int, mode: str) -> CreateCauseDataClass:
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
            cause=cause.cause,
            status=cause.status
        )

    def get(self, question_id: uuid, pk: uuid) -> CreateCauseDataClass:
        try:
            cause = Causes.objects.get(pk=pk, problem_id = question_id)
            return CreateCauseDataClass(
                question_id=question_id,
                id=cause.id,
                row=cause.row,
                column=cause.column,
                mode=cause.mode,
                cause=cause.cause,
                status=cause.status
            )
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Sebab tidak ditemukan")

    def update(self, question_id: uuid, pk: uuid, cause: str) -> CreateCauseDataClass:
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
                cause=causes.cause,
                status=causes.status
            )
        except ObjectDoesNotExist:
            raise NotFoundRequestException("Sebab tidak ditemukan")