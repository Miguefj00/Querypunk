from pydantic import BaseModel
from typing import Optional


class ChapterBase(BaseModel):
    """ Base chapter information shared across schemas. """
    title: str
    description: str


class ChapterCreate(ChapterBase):
    """ Payload to create a chapter. """
    pass


class ChapterUpdate(BaseModel):
    """ Payload to update chapter. """
    title: Optional[str] = None
    description: Optional[str] = None


class ChapterResponse(ChapterBase):
    """ Chapter data returned by the API. """
    id: int
    user_id: int
    difficulty: Optional[str] = None
    creator_username: str

    class Config:
        from_attributes = True
