from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.repositories.challenge_repository import ChallengeRepository
from app.utils.difficulty_utils import DIFFICULTY_TO_VALUE, VALUE_TO_DIFFICULTY
from app.utils.role_utils import ROLE_ADMIN
from app.models import User
from app.models.chapter import Chapter
from app.database.repositories.chapter_repository import ChapterRepository


class ChapterService:

    @staticmethod
    def get_owned_chapter(db: Session, chapter_id: int, user: User):
        """ Retrieves a chapter ensuring ownership or admin permissions. """
        chapter = ChapterRepository.get_by_id(db, chapter_id)

        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        if user.role_id != ROLE_ADMIN and chapter.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        return chapter

    @staticmethod
    def recalculate_chapter_difficulty_sqlite(conn, chapter_id: int):
        """ Recalculates average chapter difficulty (SQLite generator mode). """
        difficulties = ChallengeRepository.get_difficulties_by_chapter_sqlite(conn, chapter_id)

        if not difficulties:
            return

        numeric_values = [DIFFICULTY_TO_VALUE[d] for d in difficulties]
        avg_value = sum(numeric_values) / len(numeric_values)
        new_difficulty = VALUE_TO_DIFFICULTY[round(avg_value)]

        ChapterRepository.update_difficulty_sqlite(conn, chapter_id, new_difficulty)

    @staticmethod
    def create(db: Session, data, current_user):
        """ Creates a new chapter assigned to the teacher. """
        chapter = Chapter(
            title=data.title,
            description=data.description,
            user_id=current_user.id
        )
        return ChapterRepository.create(db, chapter)

    @staticmethod
    def get_all(db: Session, current_user):
        """ Return all chapters with owner's username. """
        chapters = ChapterRepository.get_all(db)

        return [
            {
                "id": chapter.id,
                "title": chapter.title,
                "description": chapter.description,
                "user_id": chapter.user_id,
                "difficulty": chapter.difficulty,
                "creator_username": creator_username
            }
            for chapter, creator_username in chapters
    ]

    @staticmethod
    def get_by_id(db: Session, chapter_id: int):
        """ Retrieves a chapter by ID. """
        chapter = ChapterRepository.get_by_id(db, chapter_id)

        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        return chapter

    @staticmethod
    def update(db: Session, chapter_id: int, data, current_user):
        """ Updates chapter title and description. """
        chapter = ChapterService.get_owned_chapter(db, chapter_id, current_user)

        if data.title is not None:
            chapter.title = data.title
        if data.description is not None:
            chapter.description = data.description

        db.commit()
        db.refresh(chapter)
        return chapter

    @staticmethod
    def delete(db: Session, chapter_id: int, current_user):
        """ Deletes a chapter. """
        chapter = ChapterService.get_owned_chapter(db, chapter_id, current_user)

        ChapterRepository.delete(db, chapter)
