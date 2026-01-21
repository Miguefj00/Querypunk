from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.session_repository import SessionRepository

class AuthService:

    @staticmethod
    def login(db, username, password, request):
        user = UserRepository.get_by_username(db, username)

        if not user or user.Password_hash != password:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        # Check active session
        active_session = SessionRepository.get_active_by_user(db, user.Id)
        if active_session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has an active session"
            )

        # Update last login
        user.Last_login = datetime.now(timezone.utc).isoformat()
        db.add(user)

        # Create session
        ip = request.client.host
        session = SessionRepository.create(db, user.Id, ip)

        db.commit()
        db.refresh(user)
        db.refresh(session)

        return user, session

    @staticmethod
    def logout(
            db: Session,
            session
    ):
        SessionRepository.close(db, session)
