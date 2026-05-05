from pydantic import BaseModel
from typing import Optional


class GameSettingsUpdate(BaseModel):
    show_global_leaderboard: Optional[bool] = None
    show_chapter_leaderboard: Optional[bool] = None
    show_challenge_leaderboard: Optional[bool] = None


class GameSettingsResponse(BaseModel):
    show_global_leaderboard: bool
    show_chapter_leaderboard: bool
    show_challenge_leaderboard: bool

    class Config:
        from_attributes = True
