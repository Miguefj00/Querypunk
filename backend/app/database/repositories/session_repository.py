from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.session import Session as UserSession


class SessionRepository:

    @staticmethod
    def create(db: Session, user_id: int, ip: str) -> UserSession:
        # Creates a new login session
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
        # Retrieves session by id
        return db.get(UserSession, session_id)

    @staticmethod
    def close_session(
            db: Session,
            session_id: int
    ):
        # Close user active session
        session = (
            db.query(UserSession)
            .filter(UserSession.id == session_id)
            .first()
        )

        if session and session.logout_time is None:

            session.logout_time = datetime.utcnow()

            db.commit()

    @staticmethod
    def delete_old_sessions(db: Session, days: int = 30):
        # Cleanup of historical login sessions for DB size control
        limit_date = datetime.utcnow() - timedelta(days=days)

        deleted = db.query(UserSession).filter(
            UserSession.login_time < limit_date
        ).delete(synchronize_session=False)

        db.commit()

        print(f"{deleted} old sessions deleted")
