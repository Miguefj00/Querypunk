from pydantic import BaseModel
from typing import Optional


class ChapterBase(BaseModel):
    title: str
    description: str


class ChapterCreate(ChapterBase):
    pass


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ChapterResponse(ChapterBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
