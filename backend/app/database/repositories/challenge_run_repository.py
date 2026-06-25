from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.challenge_run import ChallengeRun


class ChallengeRunRepository:

    @staticmethod
    def get_active_run(db: Session, user_id: int, challenge_id: int) -> ChallengeRun | None:
        # Returns the current run of a user in a challenge
        return (
            db.query(ChallengeRun)
            .filter(
                ChallengeRun.user_id == user_id,
                ChallengeRun.challenge_id == challenge_id,
                ChallengeRun.finished_at.is_(None)
            )
            .first()
        )

    @staticmethod
    def get_user_active_run(db: Session, user_id: int) -> ChallengeRun | None:
        # Returns the active run of a user across ALL challenges.
        return (
            db.query(ChallengeRun)
            .filter(
                ChallengeRun.user_id == user_id,
                ChallengeRun.finished_at.is_(None)
            )
            .first()
        )

    @staticmethod
    def create_run(db: Session, user_id: int, challenge_id: int) -> ChallengeRun:
        # Creates and starts a new challenge run
        run = ChallengeRun(
            user_id=user_id,
            challenge_id=challenge_id,
            is_successful=None
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def close_active_run(db: Session, user_id: int, challenge_id: int):
        # Closes an incomplete/active run
        run = (
            db.query(ChallengeRun)
            .filter(
                ChallengeRun.user_id == user_id,
                ChallengeRun.challenge_id == challenge_id,
                ChallengeRun.finished_at.is_(None)
            )
            .first()
        )

        if run:
            run.finished_at = datetime.utcnow()
            run.is_successful = False
            db.commit()

        return run

    @staticmethod
    def complete_run(db: Session, run_id: int, score: int):
        # Mark a run as completed
        run = db.query(ChallengeRun).filter(
            ChallengeRun.id == run_id
        ).first()

        if run:
            run.finished_at = datetime.utcnow()
            run.is_successful = True
            run.score = score
            db.commit()

    @staticmethod
    def delete_old_runs(db: Session, days: int = 30):
        # Cleanup old gameplay runs for DB size control
        limit_date = datetime.utcnow() - timedelta(days=days)

        deleted = db.query(ChallengeRun).filter(
            ChallengeRun.started_at < limit_date
        ).delete(synchronize_session=False)

        db.commit()
        print(f"{deleted} old runs deleted")
