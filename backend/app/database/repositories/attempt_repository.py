from sqlalchemy.orm import Session
from app.models.attempt import Attempt


class AttemptRepository:

    @staticmethod
    def count_failed_attempts_in_run(db: Session, run_id: int):
        return (
            db.query(Attempt)
            .filter(
                Attempt.challenge_run_id == run_id,
                Attempt.is_correct == False
            )
            .count()
        )

    @staticmethod
    def get_first_attempt_in_run(db: Session, run_id: int):
        return (
            db.query(Attempt)
            .filter(Attempt.challenge_run_id == run_id)
            .order_by(Attempt.created_at.asc())
            .first()
        )
