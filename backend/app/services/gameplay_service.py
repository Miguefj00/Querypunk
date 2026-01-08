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
                    db, user_id, challenge.Id
                ) + 1
        )

        # Check solution
        is_correct = (
                data.submitted_query.strip().lower()
                == challenge.Expected_query.strip().lower()
        )

        # Calculate score
        score = challenge.Max_score if is_correct else 0

        # Create attempt
        attempt = Attempt(
            User_id=user_id,
            Challenge_id=challenge.Id,
            Submitted_query=data.submitted_query,
            Is_correct=is_correct,
            Score_awarded=score,
            Attempt_number=attempt_number,
            Execution_time=0.0
        )

        AttemptRepository.create(db, attempt)

        # Get hint if its necessary
        hint = HintRepository.get_unlocked_hint(
            db, challenge.Id, attempt_number
        )

        # Answer
        return AttemptResponse(
            is_correct=is_correct,
            score_awarded=score,
            attempt_number=attempt_number,
            hint_unlocked=hint.Content if hint else None
        )
