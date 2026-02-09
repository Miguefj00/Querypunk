from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.roles import ROLE_TEACHER, ROLE_STUDENT
from app.database.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate
from app.security.password import hash_password


class UserService:

    @staticmethod
    def _create_user(
            db: Session,
            *,
            username: str,
            email: str,
            password: str,
            role_id: int
    ) -> User:
        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role_id=role_id,
            created_at=datetime.utcnow().isoformat(),
            last_login=None
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def create(db: Session, data: UserCreate):

        if UserRepository.get_by_username(db, data.username):
            raise HTTPException(status_code=409, detail="Username already exists")

        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=409, detail="Email already exists")

        if data.role == "teacher":
            role_id = ROLE_TEACHER
        else:
            role_id = ROLE_STUDENT

        return UserService._create_user(
            db,
            username=data.username,
            email=data.email,
            password=data.password,
            role_id=role_id
        )

    @staticmethod
    def register(db, data):
        if UserRepository.get_by_username(db, data.username):
            raise HTTPException(status_code=409, detail="Username already exists")

        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=409, detail="Email already exists")

        return UserService._create_user(
            db,
            username=data.username,
            email=data.email,
            password=data.password,
            role_id=ROLE_STUDENT
        )
