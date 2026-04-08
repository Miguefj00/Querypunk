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
    def update_difficulty(conn, chapter_id: int, difficulty: str):
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE chapter SET difficulty = ? WHERE id = ?
        """, (difficulty, chapter_id))

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
