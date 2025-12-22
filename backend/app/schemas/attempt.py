from pydantic import BaseModel

class AttemptCreate(BaseModel):
    challenge_id: int
    submitted_query: str
