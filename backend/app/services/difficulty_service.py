from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.repositories.chapter_repository import ChapterRepository
from app.models import Challenge, Session
from app.schemas.challenge import ValidationRules
from app.utils.difficulty_utils import evaluate_sql_difficulty
from app.utils.difficulty_utils import (
    VALUE_TO_DIFFICULTY,
    DIFFICULTY_TO_VALUE,
)


class DifficultyService:

    @staticmethod
    def recalc_challenge_difficulty(db: Session, challenge: Challenge):
        rules = ValidationRules.model_validate(challenge.validation_rules)

        difficulty = evaluate_sql_difficulty(
            challenge.solution,
            rules
        )

        challenge.difficulty = difficulty
        db.flush()

    @staticmethod
    def recalc_chapter_difficulty(db: Session, chapter_id: int):
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
