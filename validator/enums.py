from enum import Enum


class QuestionType(Enum):
    PENGAWASAN = 'PENGAWASAN'
    PRIBADI = 'PRIBADI'

class HistoryType(Enum):
    LAST_WEEK = 'last_week'
    OLDER = 'older'