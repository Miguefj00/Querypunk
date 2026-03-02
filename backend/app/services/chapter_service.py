from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.utils.role_utils import ROLE_ADMIN
from app.models import User
from app.models.chapter import Chapter
from app.database.repositories.chapter_repository import ChapterRepository


class ChapterService:

    @staticmethod
    def get_owned_chapter(db: Session, chapter_id: int, user: User):
        chapter = ChapterRepository.get_by_id(db, chapter_id)

        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        if user.role_id != ROLE_ADMIN and chapter.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        return chapter

    @staticmethod
    def create(db: Session, data, current_user):
        chapter = Chapter(
            title=data.title,
            description=data.description,
            user_id=current_user.id
        )
        return ChapterRepository.create(db, chapter)

    @staticmethod
    def get_all(db: Session, current_user):
        return ChapterRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, chapter_id: int):
        chapter = ChapterRepository.get_by_id(db, chapter_id)

        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        return chapter

    @staticmethod
    def update(db: Session, chapter_id: int, data, current_user):
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
        chapter = ChapterService.get_owned_chapter(db, chapter_id, current_user)

        ChapterRepository.delete(db, chapter)
