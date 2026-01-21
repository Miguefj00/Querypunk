from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: int


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role_id: int

    class Config:
        from_attributes = True

