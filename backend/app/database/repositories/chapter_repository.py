from sqlalchemy.orm import Session
from app.models.chapter import Chapter


class ChapterRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Chapter).all()

    @staticmethod
    def get_by_id(db: Session, chapter_id: int):
        return db.query(Chapter).filter(Chapter.id == chapter_id).first()

    @staticmethod
    def create(db: Session, chapter: Chapter):
        db.add(chapter)
        db.commit()
        db.refresh(chapter)
        return chapter

    @staticmethod
    def delete(db: Session, chapter: Chapter):
        db.delete(chapter)
        db.commit()
