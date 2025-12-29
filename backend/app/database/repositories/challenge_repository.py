from sqlalchemy import select, literal
from sqlalchemy.orm import Session
from app.models.challenge import Challenge

class ChallengeRepository:

    @staticmethod
    def get_by_id(db: Session, challenge_id: int) -> Challenge | None:
        stmt = select(Challenge).where(Challenge.Id == literal(challenge_id))
        return db.execute(stmt).scalar_one_or_none()
