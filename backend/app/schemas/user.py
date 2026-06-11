from datetime import datetime
from typing import Literal, Optional, List
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    """ Payload to create a new user. """
    username: str
    email: EmailStr
    password: str
    role: Literal["student", "teacher"]


class UserUpdate(BaseModel):
    """ Payload to update and validate user profile data. """
    username: str | None = None
    email: EmailStr | None = None
    @field_validator("username")
    @classmethod
    def validate_username(cls, value):

        if value is None:
            return value

        value = value.strip()

        if len(value) == 0:
            raise ValueError(
                "Username cannot be empty"
            )

        if len(value) < 3:
            raise ValueError(
                "Username must contain at least 3 characters"
            )

        return value


class ChangePasswordRequest(BaseModel):
    """ Payload to change the authenticated user's password. """
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    """ User data returned after creation or update. """
    id: int
    username: str
    email: str
    role_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """ Basic user information used in listings. """
    id: int
    username: str
    email: EmailStr
    role_id: int

    class Config:
        from_attributes = True


class UserRead(UserBase):
    """ Extended user profile including timestamps. """
    created_at: Optional[datetime]
    last_login: Optional[datetime]


class UserInGroupResponse(BaseModel):
    """ User data when listing members of a group. """
    username: str
    email: str

    class Config:
        from_attributes = True


class UserBulkDelete(BaseModel):
    """ Payload to delete multiple users. """
    user_ids: List[int]

