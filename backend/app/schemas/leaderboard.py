from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    position: int
    user_id: int
    username: str
    score: int
    