from fastapi import HTTPException

from app.database.repositories.hint_repository import HintRepository
from app.services.challenge_service import ChallengeService
from app.models import User, Session
from app.schemas.hint import HintCreate, HintUpdate
from app.utils.role_utils import ROLE_ADMIN, ROLE_TEACHER


class HintService:

    @staticmethod
    def _get_hint_in_challenge(db: Session, challenge_id: int, hint_id: int):

        hint = HintRepository.get_by_id(db, hint_id)

        if not hint:
            raise HTTPException(status_code=404, detail="Hint not found")

        if hint.challenge_id != challenge_id:
            raise HTTPException(status_code=404, detail="Hint not found")

        return hint

    @staticmethod
    def get_by_id(db: Session, chapter_id: int, challenge_id: int, hint_id: int, current_user: User):

        ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        if current_user.role_id not in [ROLE_ADMIN, ROLE_TEACHER]:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return HintService._get_hint_in_challenge(db, challenge_id, hint_id)

    @staticmethod
    def get_by_challenge(db: Session, chapter_id: int, challenge_id: int, current_user: User):

        ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        if current_user.role_id not in [ROLE_ADMIN, ROLE_TEACHER]:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return HintRepository.get_by_challenge(db, challenge_id)

    @staticmethod
    def get_unlocked_hints(db: Session, challenge_id: int, attempts: int):

        hints = HintRepository.get_by_challenge(db, challenge_id)

        unlocked = []

        for hint in hints:

            if hint.unlock_after_attempts is None:
                unlocked.append(hint)

            elif attempts >= hint.unlock_after_attempts:
                unlocked.append(hint)

        return unlocked

    @staticmethod
    def create(db: Session, chapter_id: int, challenge_id: int, data: HintCreate, current_user: User):

        challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        ChallengeService.check_teacher_owns_challenge(db, challenge, current_user)

        return HintRepository.create(db, challenge_id, data)

    @staticmethod
    def update(db: Session, chapter_id: int, challenge_id: int, hint_id: int, data: HintUpdate, current_user: User):

        challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        ChallengeService.check_teacher_owns_challenge(db, challenge, current_user)

        hint = HintService._get_hint_in_challenge(db, challenge_id, hint_id)

        return HintRepository.update(db, hint, data)

    @staticmethod
    def delete(db: Session, chapter_id: int, challenge_id: int, hint_id: int, current_user: User):

        challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        ChallengeService.check_teacher_owns_challenge(db, challenge, current_user)

        hint = HintService._get_hint_in_challenge(db, challenge_id, hint_id)

        HintRepository.delete(db, hint)

        return {"detail": "Hint deleted successfully"}
