from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.attempt import Attempt

class AttemptRepository:

    @staticmethod
    def count_attempts(db: Session, user_id: int, challenge_id: int) -> int:
        stmt = select(func.count()).where(
            Attempt.User_id == user_id,
            Attempt.Challenge_id == challenge_id
        )
        return db.execute(stmt).scalar_one()

    @staticmethod
    def save(db: Session, attempt: Attempt) -> None:
        db.add(attempt)
        db.commit()
