from typing import List, Any, Optional

from pydantic import BaseModel


class AttemptCreate(BaseModel):
    challenge_id: int
    query: str


class AttemptResponse(BaseModel):
    correct: bool
    rows_returned: int
    columns: List[str]
    rows: List[List[Any]]
    hints: Optional[List[str]] = None
    score: Optional[int] = None
    run_score: int | None = None
    best_score: int | None = None
