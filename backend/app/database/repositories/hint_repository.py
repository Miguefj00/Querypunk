from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.hint import Hint


class HintRepository:

    @staticmethod
    def get_unlocked_hint(
            db: Session,
            challenge_id: int,
            attempt_number: int
    ) -> Hint | None:

        stmt = (
            select(Hint)
            .where(
                Hint.Challenge_id == challenge_id,
                Hint.Unlock_attempt <= attempt_number
            )
            .order_by(Hint.Hint_number.desc())
        )

        return db.execute(stmt).scalar_one_or_none()
