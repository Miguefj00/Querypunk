from pydantic import BaseModel


class ChallengePublic(BaseModel):
    id: int
    chapter_id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class ChallengeWithSolution(ChallengePublic):
    solution: str


class ChallengeCreate(BaseModel):
    title: str
    description: str
    solution: str


class ChallengeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    solution: str | None = None


