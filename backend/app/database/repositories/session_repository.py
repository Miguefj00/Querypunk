from datetime import datetime

from sqlalchemy.orm import Session
from app.models.session import Session as UserSession

class SessionRepository:

    @staticmethod
    def create(db: Session, session: UserSession) -> UserSession:
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def close(db: Session, session: UserSession):
        session.Logout_time = datetime.utcnow().isoformat()
        db.commit()
