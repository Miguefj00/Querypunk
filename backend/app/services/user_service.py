from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.utils.role_utils import ROLE_TEACHER, ROLE_STUDENT, ROLE_ADMIN
from app.database.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, ChangePasswordRequest, UserUpdate
from app.security.auth import verify_password
from app.security.password import hash_password
from app.utils.user_utils import generate_username_from_name


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
    def create_student_auto(
            db: Session,
            nombre: str,
            apellido: str,
            email: str,
            password: str
    ) -> User:

        username = generate_username_from_name(nombre, apellido)

        if UserRepository.get_by_email(db, email):
            raise HTTPException(status_code=409, detail="Email already exists")

        return UserService._create_user(
            db=db,
            username=username,
            email=email,
            password=password,
            role_id=ROLE_STUDENT
        )

    @staticmethod
    def change_password(db: Session, current_user: User, data: ChangePasswordRequest):
        if not verify_password(data.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        if len(data.new_password) < 6:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 6 characters"
            )

        current_user.password_hash = hash_password(data.new_password)

        db.commit()

        return {"detail": "Password updated successfully"}

    @staticmethod
    def get_all(db: Session, current_user: User):
        users = UserRepository.get_all(db)

        if current_user.role_id != ROLE_ADMIN:
            users = [u for u in users if u.role_id != ROLE_ADMIN]

        return users

    @staticmethod
    def get_by_id(db: Session, user_id: int, current_user: User):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.role_id == ROLE_ADMIN and current_user.role_id != ROLE_ADMIN:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    @staticmethod
    def update(db: Session, user_id: int, user_update: UserUpdate, current_user: User):
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        is_admin = current_user.role_id == ROLE_ADMIN

        if not is_admin and current_user.id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own user"
            )

        return UserRepository.update(db, user, user_update)

    @staticmethod
    def delete(db: Session, user_id: int, current_user: User):
        if current_user.id == user_id:
            raise HTTPException(
                status_code=400,
                detail="Admin cannot delete itself"
            )

        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        UserRepository.delete(db, user)

        return {"detail": "User deleted successfully"}
