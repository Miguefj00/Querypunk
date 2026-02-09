from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.attempt import Attempt


class AttemptRepository:

    @staticmethod
    def count_attempts(db: Session, user_id: int, challenge_id: int) -> int:
        stmt = select(func.count()).where(
            Attempt.user_id == user_id,
            Attempt.challenge_id == challenge_id
        )
        return db.execute(stmt).scalar_one()

    @staticmethod
    def count_by_user_and_challenge(
            db: Session, user_id: int, challenge_id: int
    ) -> int:
        stmt = (
            select(func.count())
            .where(
                Attempt.user_id == user_id,
                Attempt.challenge_id == challenge_id
            )
        )
        return db.execute(stmt).scalar_one()

    @staticmethod
    def create(db: Session, attempt: Attempt) -> Attempt:
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

    @staticmethod
    def get_last_attempt(db: Session, user_id: int, challenge_id: int) -> Attempt | None:
        stmt = (
            select(Attempt)
            .where(
                Attempt.user_id == user_id,
                Attempt.challenge_id == challenge_id
            )
            .order_by(Attempt.attempt_number.desc())
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def save(db: Session, attempt: Attempt) -> None:
        db.add(attempt)
        db.commit()
