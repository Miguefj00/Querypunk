from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.hint import Hint
from app.schemas.hint import HintCreate, HintUpdate


class HintRepository:

    @staticmethod
    def create(db: Session, challenge_id: int, data: HintCreate):
        # Creates a new hint for a challenge
        hint = Hint(
            challenge_id=challenge_id,
            order_index=data.order_index,
            content=data.content,
            unlock_after_attempts=data.unlock_after_attempts
        )

        db.add(hint)
        db.commit()
        db.refresh(hint)

        return hint

    @staticmethod
    def get_by_id(db: Session, hint_id: int):
        # Retrieves a single hint by id
        stmt = select(Hint).where(Hint.id == hint_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_challenge(db: Session, challenge_id: int):
        # Returns hints in a challenge
        stmt = select(Hint).where(Hint.challenge_id == challenge_id).order_by(Hint.order_index)
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update(db: Session, hint: Hint, data: HintUpdate):
        # Updates hint
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(hint, field, value)

        db.commit()
        db.refresh(hint)

        return hint

    @staticmethod
    def delete(db: Session, hint: Hint):
        # Deletes hint
        db.delete(hint)
        db.commit()
