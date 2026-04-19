from fastapi import HTTPException
import json

from app.services.challenge_generator_service.game_db_executor import run_solution_and_get_result
from app.services.difficulty_service import DifficultyService
from app.utils.role_utils import ROLE_TEACHER, ROLE_STUDENT
from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.repositories.chapter_repository import ChapterRepository
from app.models import Challenge, User, Session
from app.schemas.challenge import ChallengeUpdate, ChallengeCreate, ChallengePublic, ChallengeWithSolution
from app.services.chapter_service import ChapterService
from app.utils.rule_utils import DEFAULT_RULES


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
        try:
            ChapterService.get_owned_chapter(db, chapter_id, current_user)

            challenge = ChallengeRepository.create(db, chapter_id, data)

            expected = run_solution_and_get_result(db, challenge.solution)

            if expected is None:
                raise HTTPException(
                    status_code=400,
                    detail="SQL inválido o tablas inexistentes en la BD del juego"
                )

            challenge.expected_result = json.dumps(expected)

            if not challenge.validation_rules:
                challenge.validation_rules = DEFAULT_RULES

            DifficultyService.recalc_challenge_difficulty(db, challenge)

            db.add(challenge)
            db.commit()
            db.refresh(challenge)

            DifficultyService.recalc_chapter_difficulty(db, chapter_id)
            db.commit()

            return challenge

        except:
            db.rollback()
            raise

    @staticmethod
    def update(db: Session, chapter_id: int, challenge_id: int, data: ChallengeUpdate, current_user: User):
        challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)

        ChallengeService.check_teacher_owns_challenge(db, challenge, current_user)

        challenge = ChallengeRepository.update(db, challenge, data)

        expected = run_solution_and_get_result(db, challenge.solution)

        if expected is None:
            raise HTTPException(
                status_code=400,
                detail="SQL inválido o tablas inexistentes en la BD del juego"
            )

        challenge.expected_result = json.dumps(expected)

        DifficultyService.recalc_challenge_difficulty(db, challenge)

        db.add(challenge)
        db.commit()
        db.refresh(challenge)

        DifficultyService.recalc_chapter_difficulty(db, chapter_id)
        db.commit()

        return challenge

    @staticmethod
    def delete(db: Session, chapter_id: int, challenge_id: int, current_user: User):
        try:
            challenge = ChallengeService.get_challenge_in_chapter(db, chapter_id, challenge_id)
            ChallengeService.check_teacher_owns_challenge(db, challenge, current_user)

            ChallengeRepository.delete(db, challenge)

            db.flush()

            DifficultyService.recalc_chapter_difficulty(db, chapter_id)

            db.commit()

            return {"detail": "Challenge deleted successfully"}
        except:
            db.rollback()
            raise

