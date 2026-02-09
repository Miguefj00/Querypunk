from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.chapter import Chapter


class ChapterRepository:

    @staticmethod
    def get_all(db: Session) -> list[Chapter]:
        stmt = select(Chapter).order_by(Chapter.id)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_by_id(db: Session, chapter_id: int) -> Chapter | None:
        stmt = select(Chapter).where(Chapter.id == chapter_id)
        return db.execute(stmt).scalar_one_or_none()
