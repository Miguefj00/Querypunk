from fastapi import HTTPException

from app.services.difficulty_service import DifficultyService
from app.utils.role_utils import ROLE_TEACHER, ROLE_STUDENT
from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.repositories.chapter_repository import ChapterRepository
from app.models import Challenge, User, Session
from app.schemas.challenge import ChallengeUpdate, ChallengeCreate, ChallengePublic, ChallengeWithSolution
from app.services.chapter_service import ChapterService


class ChallengeService:

    @staticmethod
    def check_teacher_owns_challenge(db: Session, challenge: Challenge, user: User):
        chapter = ChapterRepository.get_by_id(db, challenge.chapter_id)

        if user.role_id == ROLE_TEACHER and chapter.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

    @staticmethod
    def get_challenge_in_chapter(db: Session, chapter_id: int, challenge_id: int):
        challenge = ChallengeRepository.get_by_id(db, challenge_id)

        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        if challenge.chapter_id != chapter_id:
            raise HTTPException(status_code=404, detail="Challenge not found")

        return challenge

    @staticmethod
    def get_by_chapter(db: Session, chapter_id: int, current_user: User):

        chapter = ChapterRepository.get_by_id(db, chapter_id)

        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        challenges = ChallengeRepository.get_by_chapter(db, chapter_id)

        if current_user.role_id == ROLE_STUDENT:
            return [ChallengePublic.model_validate(c) for c in challenges]

        return [ChallengeWithSolution.model_validate(c) for c in challenges]

    @staticmethod
    def get_by_id(db: Session, chapter_id: int, challenge_id: int, current_user: User):

        challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        if current_user.role_id == ROLE_STUDENT:
            return ChallengePublic.model_validate(challenge)

        return ChallengeWithSolution.model_validate(challenge)

    @staticmethod
    def create(db: Session, chapter_id: int, data: ChallengeCreate, current_user: User):
        ChapterService.get_owned_chapter(db, chapter_id, current_user)

        challenge = ChallengeRepository.create(
            db,
            chapter_id=chapter_id,
            data=data
        )

        DifficultyService.recalc_challenge_difficulty(db, challenge)
        DifficultyService.recalc_chapter_difficulty(db, chapter_id)

        return challenge

    @staticmethod
    def update(db: Session, chapter_id: int, challenge_id: int, data: ChallengeUpdate, current_user: User):
        challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        ChallengeService.check_teacher_owns_challenge(db, challenge, current_user)

        challenge = ChallengeRepository.update(db, challenge, data)

        DifficultyService.recalc_challenge_difficulty(db, challenge)
        DifficultyService.recalc_chapter_difficulty(db, chapter_id)

        return challenge

    @staticmethod
    def delete(db: Session, chapter_id: int, challenge_id: int, current_user: User):
        challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        ChallengeService.check_teacher_owns_challenge(db, challenge, current_user)

        ChallengeRepository.delete(db, challenge)

        DifficultyService.recalc_chapter_difficulty(db, chapter_id)

        return {"detail": "Challenge deleted successfully"}

