from sqlalchemy.orm import Session

from app.database.repositories.attempt_repository import AttemptRepository
from app.database.repositories.challenge_repository import ChallengeRepository
from app.models.attempt import Attempt
from app.schemas.attempt import AttemptCreate, AttemptResponse

def process_attempt(db: Session, user, data: AttemptCreate) -> AttemptResponse:
    challenge = ChallengeRepository.get_by_id(db, data.challenge_id)

    if challenge is None:
        raise ValueError("Challenge not found")

    # ⚠️ Lógica provisional
    is_correct = data.submitted_query.strip().lower() == challenge.Expected_query.strip().lower()

    attempt_number = (
            AttemptRepository.count_attempts(db, user.Id, challenge.Id) + 1
    )

    score = challenge.Max_score if is_correct else 0

    attempt = Attempt(
        User_id=user.Id,
        Challenge_id=challenge.Id,
        Submitted_query=data.submitted_query,
        Is_correct=is_correct,
        Score_awarded=score,
        Attempt_number=attempt_number,
        Execution_time=0.0
    )

    db.add(attempt)
    db.commit()

    return AttemptResponse(
        is_correct=is_correct,
        score_awarded=score,
        attempt_number=attempt_number,
        hint_unlocked=None
    )
