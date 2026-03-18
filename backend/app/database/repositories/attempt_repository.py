from sqlalchemy.orm import Session
from app.models.attempt import Attempt


class AttemptRepository:

    @staticmethod
    def count_failed_attempts(db: Session, user_id: int, challenge_id: int):

        return db.query(Attempt).filter(
            Attempt.user_id == user_id,
            Attempt.challenge_id == challenge_id,
            Attempt.is_correct == False
        ).count()
