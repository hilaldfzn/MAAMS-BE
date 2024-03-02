from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CreateQuestionDataClass(BaseModel):
    username: str
    id: UUID
    question: str
    created_at: datetime
    mode: str