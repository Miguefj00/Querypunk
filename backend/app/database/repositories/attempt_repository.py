from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.models.attempt import Attempt


class AttemptRepository:

    @staticmethod
    def count_failed_attempts_in_run(db: Session, run_id: int):
        # Counts incorrect submissions inside a challenge run
        return (
            db.query(Attempt)
            .filter(
                Attempt.challenge_run_id == run_id,
                Attempt.is_correct == False
            )
            .count()
        )

    @staticmethod
    def delete_old_attempts(db: Session, days: int):
        # Removes historical attempts to keep DB size under control
        limit_date = datetime.utcnow() - timedelta(days=days)

        deleted = db.query(Attempt).filter(
            Attempt.created_at < limit_date
        ).delete(synchronize_session=False)

        db.commit()
        print(f"{deleted} old attempts deleted")
