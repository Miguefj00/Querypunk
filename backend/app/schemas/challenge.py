from typing import Optional

from pydantic import BaseModel

from app.database.enums import DifficultyEnum


class ChallengePublic(BaseModel):
    """Public challenge data"""
    id: int
    chapter_id: int
    title: str
    description: str
    difficulty: DifficultyEnum

    class Config:
        from_attributes = True


class ChallengeWithSolution(ChallengePublic):
    """Extended challenge data including solution for teachers/admins"""
    solution: str
    generated_by_system: int


class ValidationRules(BaseModel):
    """Rules used to validate or enforce SQL constraints in a challenge"""
    must_use_avg: bool = False
    must_use_subquery: bool = False
    forbid_literals: bool = False
    no_group_by: bool = False
    must_use_group_by: bool = False
    must_use_join: bool = False
    forbid_select_all: bool = False


class ChallengeCreate(BaseModel):
    """Payload to create a new challenge."""
    title: str
    description: str
    solution: str
    validation_rules: Optional[ValidationRules] = None


class ChallengeCreateWithExpectedQuery(ChallengeCreate):
    """Challenge creation including expected query result snapshot"""
    expected_result: str


class ChallengeUpdate(BaseModel):
    """Payload to update a challenge."""
    title: str | None = None
    description: str | None = None
    solution: str | None = None
    validation_rules: Optional[ValidationRules] = None


class ChallengeUpdateWithExpectedQuery(ChallengeUpdate):
    """Challenge update including expected result snapshot."""
    expected_result: str



