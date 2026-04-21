from datetime import datetime
from sqlalchemy.orm import Session
from app.models.challenge_run import ChallengeRun


def get_active_run(db: Session, user_id: int, challenge_id: int) -> ChallengeRun | None:
    return (
        db.query(ChallengeRun)
        .filter(
            ChallengeRun.user_id == user_id,
            ChallengeRun.challenge_id == challenge_id,
            ChallengeRun.finished_at.is_(None)
        )
        .first()
    )


def create_run(db: Session, user_id: int, challenge_id: int) -> ChallengeRun:
    run = ChallengeRun(
        user_id=user_id,
        challenge_id=challenge_id
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def complete_run(db: Session, run_id: int):
    run = db.query(ChallengeRun).filter(ChallengeRun.id == run_id).first()
    if run:
        run.finished_at = datetime.utcnow()
        db.commit()
