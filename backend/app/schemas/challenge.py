from typing import Optional

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
    generated_by_system: int


class ValidationRules(BaseModel):
    must_use_avg: bool = False
    must_use_subquery: bool = False
    forbid_literals: bool = False
    no_group_by: bool = False
    must_use_group_by: bool = False
    must_use_join: bool = False
    forbid_select_all: bool = False


class ChallengeCreate(BaseModel):
    title: str
    description: str
    solution: str
    validation_rules: Optional[ValidationRules] = None


class ChallengeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    solution: str | None = None
    validation_rules: Optional[ValidationRules] = None



