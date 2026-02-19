from fastapi import HTTPException

from app.core.roles import ROLE_TEACHER, ROLE_ADMIN
from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.repositories.chapter_repository import ChapterRepository
from app.models import Challenge, User, Session
from app.schemas.challenge import ChallengeUpdate, ChallengeCreate
from app.services.chapter_service import ChapterService


class ChallengeService:

    @staticmethod
    def _check_teacher_owns_challenge(db: Session, challenge: Challenge, user: User):
        chapter = ChapterRepository.get_by_id(db, challenge.chapter_id)

        if user.role_id == ROLE_TEACHER and chapter.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

    @staticmethod
    def _get_challenge_in_chapter(db: Session, chapter_id: int, challenge_id: int):
        challenge = ChallengeRepository.get_by_id(db, challenge_id)

        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        if challenge.chapter_id != chapter_id:
            raise HTTPException(status_code=404, detail="Challenge not found")

        return challenge

    @staticmethod
    def get_by_chapter(db: Session, chapter_id: int):
        chapter = ChapterRepository.get_by_id(db, chapter_id)

        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        return ChallengeRepository.get_by_chapter(db, chapter_id)

    @staticmethod
    def create(db: Session, chapter_id: int, data: ChallengeCreate, current_user: User):
        if current_user.role_id not in [ROLE_ADMIN, ROLE_TEACHER]:
            raise HTTPException(status_code=403, detail="Not allowed")

        ChapterService.get_owned_chapter(db, chapter_id, current_user)

        return ChallengeRepository.create(
            db,
            chapter_id=chapter_id,
            data=data
        )

    @staticmethod
    def get_by_id(db: Session, chapter_id: int, challenge_id: int):
        return ChallengeService._get_challenge_in_chapter(db, chapter_id, challenge_id)

    @staticmethod
    def update(db: Session, chapter_id: int, challenge_id: int, data: ChallengeUpdate, current_user: User):
        challenge = ChallengeService._get_challenge_in_chapter(db, chapter_id, challenge_id)

        if current_user.role_id not in [ROLE_ADMIN, ROLE_TEACHER]:
            raise HTTPException(status_code=403, detail="Not allowed")

        ChallengeService._check_teacher_owns_challenge(db, challenge, current_user)

        return ChallengeRepository.update(db, challenge, data)

    @staticmethod
    def delete(db: Session, chapter_id: int, challenge_id: int, current_user: User):
        challenge = ChallengeService._get_challenge_in_chapter(db, chapter_id, challenge_id)

        if current_user.role_id not in [ROLE_ADMIN, ROLE_TEACHER]:
            raise HTTPException(status_code=403, detail="Not allowed")

        ChallengeService._check_teacher_owns_challenge(db, challenge, current_user)

        ChallengeRepository.delete(db, challenge)

        return {"detail": "Challenge deleted successfully"}

