from pydantic import BaseModel


class GroupResponse(BaseModel):
    """ Group data returned after creation or update. """
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True


class GroupImportResult(BaseModel):
    """ Result of students import into a group. """
    group_id: int
    created_users: int
    users_assigned: int


class GroupListResponse(BaseModel):
    """ Group listing with aggregated student count. """
    id: int
    name: str
    description: str
    student_count: int

    class Config:
        from_attributes = True
