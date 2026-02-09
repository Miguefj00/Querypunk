from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.session import Session as UserSession


class SessionRepository:

    @staticmethod
    def create(db: Session, user_id: int, ip: str) -> UserSession:
        session = UserSession(
            user_id=user_id,
            login_time=datetime.utcnow().isoformat(),
            logout_time=None,
            ip_address=ip
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_active_by_id(db: Session, session_id: int):
        return (
            db.query(UserSession)
            .filter(
                UserSession.id == session_id,
                UserSession.logout_time.is_(None)
            )
            .first()
        )

    @staticmethod
    def get_active_by_user(db: Session, user_id: int) -> UserSession | None:
        stmt = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.logout_time.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def close_by_id(db, session_id: int):
        session = db.get(UserSession, session_id)

        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        session.logout_time = datetime.utcnow().isoformat()
        db.commit()

    @staticmethod
    def close(db: Session, session: UserSession) -> None:
        session.logout_time = datetime.utcnow().isoformat()
        db.commit()

    @staticmethod
    def close_active_sessions_by_user(db: Session, user_id: int) -> None:
        sessions = (
            db.query(UserSession)
            .filter(
                UserSession.user_id == user_id,
                UserSession.logout_time.is_(None)
            )
            .all()
        )

        for session in sessions:
            session.logout_time = datetime.utcnow()

        db.commit()

    @staticmethod
    def get_by_id(db: Session, session_id: int) -> UserSession | None:
        return db.get(UserSession, session_id)

