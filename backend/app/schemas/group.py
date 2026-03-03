from pydantic import BaseModel


class GroupResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True


class GroupImportResult(BaseModel):
    group_id: int
    created_users: int
    existing_users_assigned: int


class GroupListResponse(BaseModel):
    id: int
    name: str
    description: str
    student_count: int

    class Config:
        from_attributes = True
