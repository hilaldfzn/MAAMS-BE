from validator.models.question import Question
from authentication.models import CustomUser
from validator.exceptions import NotFoundRequestException
from datetime import datetime, timedelta
from history.enums import HistoryType
from history.exceptions import InvalidModeRequestException

class SearchBarHistoryService():
    def filter(self, user: CustomUser, keyword: str, mode:HistoryType):
        today_datetime = datetime.now()
        last_week_datetime = today_datetime - timedelta(days=7)

        if not keyword:
            keyword = ''

        if mode == HistoryType.OLDER.value:
            questions = self.get_older(user, keyword, last_week_datetime)
        elif mode == HistoryType.LAST_WEEK.value:
            questions = self.get_last_week(user, keyword, last_week_datetime, today_datetime)
        else:
            raise InvalidModeRequestException('Invalid Mode')

        if not questions:
            raise NotFoundRequestException("Analisis tidak ditemukan")
        return questions

    def get_last_week(self, user, keyword, startdate, enddate):
        questions = Question.objects.filter(user=user, 
                                            question__icontains=keyword,
                                            created_at__range=[startdate, enddate])
        return questions

    def get_older(self, user, keyword, cutoff_date):
        questions = Question.objects.filter(user=user, 
                                            question__icontains=keyword,
                                            created_at__lte=cutoff_date)
        return questions
