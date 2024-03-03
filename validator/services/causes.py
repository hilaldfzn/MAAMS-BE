from authentication.models import CustomUser
import openai
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import CustomUser
from validator.dataclasses.create_cause import CreateCauseDataClass
from validator.models.causes import Causes
from validator.exceptions import NotFoundRequestException, ForbiddenRequestException

class CausesService:
    @staticmethod
    def api_call(self, prompt: str):
        # Integrate with ChatGPT
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=5,  # TODO: determine most optimal param
            n=5,  # TODO: determine most optimal param
            temperature=0  # TODO: determine most optimal param
        )
        answer = response.choices[0].text.strip()

        return answer

    def check_root_cause(input_string: str, previous_cause: str) -> bool:
        # Check root cause logic (as shown in the previous response)
        pass

    def create(user: CustomUser, cause_data: CreateCauseDataClass) -> CreateCauseDataClass:
        cause = Causes.objects.create(
            problem_id=cause_data.problem_id,
            row=cause_data.row,
            column=cause_data.column,
            mode=cause_data.mode,
            cause=cause_data.cause
        )
        return CreateCauseDataClass(
            problem_id=cause.problem_id,
            id=cause.id,
            row=cause.row,
            column=cause.column,
            mode=cause.mode,
            cause=cause.cause
        )

    def get(user: CustomUser, pk: int) -> CreateCauseDataClass:
        try:
            cause = Causes.objects.get(pk=pk, problem__user=user)
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

    def update(user: CustomUser, cause_data: CreateCauseDataClass, pk: int) -> CreateCauseDataClass:
        try:
            cause = Causes.objects.get(pk=pk, problem__user=user)
            cause.problem_id = cause_data.problem_id
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