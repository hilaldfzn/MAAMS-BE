from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class CreateQuestionDataClass(BaseModel):
    username: str
    id: UUID
    question: str
    created_at: datetime
    mode: str
