from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    """Entry in a leaderboard ranking"""
    position: int
    user_id: int
    username: str
    score: int
    