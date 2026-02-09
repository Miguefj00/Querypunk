from sqlalchemy.orm import Session
from app.models.attempt import Attempt
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.repositories.attempt_repository import AttemptRepository
from app.database.repositories.hint_repository import HintRepository


class GameplayService:

    @staticmethod
    def process_attempt(
            db: Session,
            user_id: int,
            data: AttemptCreate
    ) -> AttemptResponse:

        # Find challenge
        challenge = ChallengeRepository.get_by_id(db, data.challenge_id)
        if not challenge:
            raise ValueError("Challenge not found")

        # Count previous attempts
        attempt_number = (
                AttemptRepository.count_by_user_and_challenge(
                    db, user_id, challenge.id
                ) + 1
        )

        # Check solution
        is_correct = (
                data.submitted_query.strip().lower()
                == challenge.expected_query.strip().lower()
        )

        # Calculate score
        score = challenge.max_score if is_correct else 0

        # Create attempt
        attempt = Attempt(
            user_id=user_id,
            challenge_id=challenge.Id,
            submitted_query=data.submitted_query,
            is_correct=is_correct,
            score_awarded=score,
            attempt_number=attempt_number,
            execution_time=0.0
        )

        AttemptRepository.create(db, attempt)

        # Get hint if its necessary
        hint = HintRepository.get_unlocked_hint(
            db, challenge.id, attempt_number
        )

        # Answer
        return AttemptResponse(
            is_correct=is_correct,
            score_awarded=score,
            attempt_number=attempt_number,
            hint_unlocked=hint.Content if hint else None
        )
