from sqlalchemy import select, literal
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate


class ChallengeRepository:

    @staticmethod
    def get_by_id(db: Session, challenge_id: int) -> Challenge | None:
        stmt = select(Challenge).where(Challenge.id == literal(challenge_id))
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_chapter(db: Session, chapter_id: int) -> list[Challenge]:
        stmt = select(Challenge).where(Challenge.chapter_id == chapter_id)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def create(db: Session, chapter_id: int, data: ChallengeCreate):
        payload = data.model_dump()
        payload["chapter_id"] = chapter_id

        challenge = Challenge(**payload)

        db.add(challenge)
        db.commit()
        db.refresh(challenge)

        return challenge

    @staticmethod
    def update(db: Session, challenge: Challenge, data: ChallengeUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(challenge, key, value)

        db.commit()
        db.refresh(challenge)

        return challenge

    @staticmethod
    def delete(db: Session, challenge: Challenge):
        db.delete(challenge)
        db.commit()
