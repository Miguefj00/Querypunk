from pydantic import BaseModel


class ResetRunRequest(BaseModel):
    challenge_id: int
