from datetime import datetime, timedelta

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

    @staticmethod
    def delete_old_attempts(db: Session, days: int = 180):
        limit_date = datetime.utcnow() - timedelta(days=days)

        deleted = db.query(Attempt).filter(
            Attempt.created_at < limit_date
        ).delete(synchronize_session=False)

        db.commit()
        print(f"{deleted} old attempts deleted")
