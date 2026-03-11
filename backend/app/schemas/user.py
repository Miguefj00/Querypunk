from datetime import datetime
from typing import Literal, Optional, List
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["student", "teacher"]


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int

    class Config:
        from_attributes = True


class UserRead(UserBase):
    created_at: Optional[datetime]
    last_login: Optional[datetime]


class UserInGroupResponse(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserBulkDelete(BaseModel):
    user_ids: List[int]

