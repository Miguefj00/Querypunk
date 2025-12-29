from pydantic import BaseModel

class AttemptCreate(BaseModel):
    challenge_id: int
    submitted_query: str

class AttemptResponse(BaseModel):
    is_correct: bool
    score_awarded: float
    attempt_number: int
    hint_unlocked: str | None
