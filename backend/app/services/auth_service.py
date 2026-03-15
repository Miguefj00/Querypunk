from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.session_repository import SessionRepository
from app.security.auth import create_access_token
from app.security.password import verify_password


class AuthService:

    @staticmethod
    def login(db: Session, username: str, password: str, ip: str):

        user = UserRepository.get_by_username(db, username)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        SessionRepository.close_active_sessions_by_user(db, user.id)

        session = SessionRepository.create(
            db=db,
            user_id=user.id,
            ip=ip
        )

        user.last_login = datetime.utcnow()
        db.commit()

        token = create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
                "role_id": user.role_id,
                "session_id": session.id
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    @staticmethod
    def logout(db: Session, user_id: int):

        SessionRepository.close_active_sessions_by_user(db, user_id)

        return {"message": "Logout successful"}
