from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CreateQuestionDataClass(BaseModel):
    problem_id: str
    id: UUID
    row: int
    column: int
    mode: str
    cause: str