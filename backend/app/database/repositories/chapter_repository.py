from sqlalchemy.orm import Session

from app.database.repositories.challenge_repository import ChallengeRepository
from app.models import User
from app.models.chapter import Chapter
from app.utils.difficulty_utils import DIFFICULTY_TO_VALUE, VALUE_TO_DIFFICULTY


class ChapterRepository:

    @staticmethod
    def get_all(db: Session):
        # Retrieves all chapters with username's creator
        return (
            db.query(
                Chapter,
                User.username.label("creator_username")
            )
            .join(User, Chapter.user_id == User.id)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, chapter_id: int):
        # Retrieves a chapter by id
        return db.query(Chapter).filter(Chapter.id == chapter_id).first()

    @staticmethod
    def update_difficulty(db: Session, chapter_id: int, difficulty: str):
        # Updates computed chapter difficulty
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if chapter:
            chapter.difficulty = difficulty
            db.flush()

    @staticmethod
    def update_difficulty_sqlite(conn, chapter_id: int, difficulty: str):
        # Raw SQLite version that updates chapter difficulty
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Chapter SET difficulty = ? WHERE id = ?",
            (difficulty, chapter_id)
        )

    @staticmethod
    def create(db: Session, chapter: Chapter):
        # Creates a new chapter
        db.add(chapter)
        db.commit()
        db.refresh(chapter)
        return chapter

    @staticmethod
    def delete(db: Session, chapter: Chapter):
        # Deletes chapter in cascade
        db.delete(chapter)
        db.commit()

    @staticmethod
    def recalc_chapter_difficulty(db: Session, chapter_id: int):
        # Update chapter difficulty after evaluation
        difficulties = ChallengeRepository.get_difficulties_by_chapter(db, chapter_id)

        if not difficulties:
            ChapterRepository.update_difficulty(db, chapter_id, "")
            return

        numeric_values = [
            DIFFICULTY_TO_VALUE[d.value] for d in difficulties
        ]

        avg_value = round(sum(numeric_values) / len(numeric_values))
        chapter_difficulty = VALUE_TO_DIFFICULTY[avg_value]

        ChapterRepository.update_difficulty(
            db,
            chapter_id,
            chapter_difficulty
        )
