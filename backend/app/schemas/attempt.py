from typing import List, Any

from pydantic import BaseModel


class AttemptCreate(BaseModel):
    challenge_id: int
    query: str


class AttemptResponse(BaseModel):
    correct: bool
    rows_returned: int
    columns: List[str]
    rows: List[List[Any]]
