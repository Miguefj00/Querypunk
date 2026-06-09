from pydantic import BaseModel


class DifficultyProgress(BaseModel):
    solved: int
    total: int


class ProgressResponse(BaseModel):
    global_challenges: dict[str, DifficultyProgress]
    played_challenges: dict[str, DifficultyProgress]


class SolvedChallengeResponse(
    BaseModel
):
    challenge_id: int
    chapter_id: int
    best_score: int
