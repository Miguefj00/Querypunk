from sqlalchemy import select, literal
from sqlalchemy.orm import Session
from app.models.challenge import Challenge


class ChallengeRepository:

    @staticmethod
    def get_by_id(db: Session, challenge_id: int) -> Challenge | None:
        stmt = select(Challenge).where(Challenge.id == literal(challenge_id))
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(db: Session) -> list[Challenge]:
        stmt = select(Challenge)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_by_chapter(db: Session, chapter_id: int) -> list[Challenge]:
        stmt = select(Challenge).where(Challenge.chapter_id == chapter_id)
        return list(db.execute(stmt).scalars().all())
