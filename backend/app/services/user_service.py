from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.roles import ROLE_TEACHER, ROLE_STUDENT
from app.database.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate
from app.security.passwords import hash_password


class UserService:

    @staticmethod
    def create(db: Session, data: UserCreate):

        if UserRepository.get_by_username(db, data.username):
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )

        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        if data.role == "teacher":
            role_id = ROLE_TEACHER
        else:
            role_id = ROLE_STUDENT

        user = User(
            Username=data.username,
            Email=data.email,
            Password_hash=hash_password(data.password),
            Role_id=role_id,
            Created_at=datetime.utcnow().isoformat(),
            Last_login=None
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def register(db, data):
        user = User(
            Username=data.username,
            Email=data.email,
            Password_hash=hash_password(data.password),
            Role_id=ROLE_STUDENT,
            Created_at=datetime.utcnow().isoformat(),
            Last_login=None
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
