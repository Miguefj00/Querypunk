import time
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from app.database.repositories.attempt_repository import AttemptRepository
from app.models.attempt import Attempt
from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.game_connection import run_query
from app.services.hint_service import HintService
from app.utils.sql_validator import compare_results, validate_query


class GameplayService:

    @staticmethod
    def submit_query(db, user_id, challenge_id, query):
        validate_query(query)

        challenge = ChallengeRepository.get_by_id(db, challenge_id)

        if not challenge:
            raise HTTPException(
                status_code=404,
                detail="Challenge not found"
            )

        start = time.time()

        try:
            student_columns, student_rows = run_query(query)

        except DBAPIError as e:

            message = str(getattr(e, "orig", e))

            raise HTTPException(
                status_code=400,
                detail=f"SQL error: {message}"
            )

        execution_time = time.time() - start

        try:
            solution_columns, solution_rows = run_query(challenge.solution)

        # In case Challenge solution produces error
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Challenge solution is invalid. Contact the instructor."
            )

        is_correct = compare_results(student_rows, solution_rows)

        attempt = Attempt(
            user_id=user_id,
            challenge_id=challenge_id,
            submitted_query=query,
            is_correct=is_correct,
            execution_time=execution_time,
            rows_returned=len(student_rows)
        )

        db.add(attempt)
        db.commit()

        hints = []

        if not is_correct:
            failed_attempts = AttemptRepository.count_failed_attempts(
                db,
                user_id,
                challenge_id
            )

            hints = HintService.get_unlocked_hints(
                db,
                challenge_id,
                failed_attempts
            )

        response = {
            "correct": is_correct,
            "rows_returned": len(student_rows),
            "columns": list(student_columns),
            "rows": [list(row) for row in student_rows]
        }

        if hints:
            response["hints"] = [h.content for h in hints]

        return response
