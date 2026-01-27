from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: Literal["student", "teacher"]

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int = Field(alias="Id")
    username: str = Field(alias="Username")
    email: str = Field(alias="Email")
    role_id: int = Field(alias="Role_id")

    class Config:
        from_attributes = True

