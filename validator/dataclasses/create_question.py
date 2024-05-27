from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel


class CreateQuestionDataClass(BaseModel):
    username: str
    id: UUID
    title: str
    question: str
    created_at: datetime
    mode: str
    tags: List[str]