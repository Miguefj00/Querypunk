from pydantic import BaseModel


class ChallengeBase(BaseModel):
    chapter_id: int
    title: str
    description: str
    solution: str


class ChallengeCreate(BaseModel):
    title: str
    description: str
    solution: str


class ChallengeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    solution: str | None = None


class ChallengeResponse(ChallengeBase):
    id: int

    class Config:
        from_attributes = True
