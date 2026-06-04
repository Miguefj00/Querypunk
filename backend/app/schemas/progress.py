from pydantic import BaseModel


class DifficultyProgress(BaseModel):
    solved: int
    total: int


class ProgressResponse(BaseModel):
    global_challenges: dict[str, DifficultyProgress]
    played_challenges: dict[str, DifficultyProgress]