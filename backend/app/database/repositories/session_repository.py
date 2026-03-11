from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.session import Session as UserSession


class SessionRepository:

    @staticmethod
    def create(db: Session, user_id: int, ip: str) -> UserSession:
        session = UserSession(
            user_id=user_id,
            login_time=datetime.utcnow(),
            logout_time=None,
            ip_address=ip
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_by_id(db: Session, session_id: int) -> UserSession | None:
        return db.get(UserSession, session_id)

    @staticmethod
    def get_active_by_user(db: Session, user_id: int) -> UserSession | None:
        stmt = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.logout_time.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

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
    def delete_old_sessions(db: Session, days: int = 10):

        limit_date = datetime.utcnow() - timedelta(days=days)

        deleted = db.query(UserSession).filter(
            UserSession.login_time < limit_date
        ).delete(synchronize_session=False)

        db.commit()

        print(f"{deleted} old sessions deleted")
