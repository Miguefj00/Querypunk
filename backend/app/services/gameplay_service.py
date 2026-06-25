import time
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from app.database.repositories.challenge_run_repository import ChallengeRunRepository
from app.database.repositories.attempt_repository import AttemptRepository
from app.models.attempt import Attempt
from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.game_connection import run_query
from app.services.hint_service import HintService
from app.database.repositories.leaderboard_repository import LeaderboardRepository
from app.utils.difficulty_utils import DIFFICULTY_SCORE, get_time_factor
from app.utils.sql_validator import compare_results, validate_query


class GameplayService:

    @staticmethod
    def submit_query(db, user_id, challenge_id, query):
        """
        Main gameplay entrypoint.
        Executes the student's SQL query, compares results with the solution,
        stores the attempt, calculates score, unlocks hints and completes the run if correct.
        """
        challenge = ChallengeRepository.get_by_id(db, challenge_id)

        if not challenge:
            raise HTTPException(
                status_code=404,
                detail="Challenge not found"
            )

        validate_query(query, challenge)

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

        active_run = ChallengeRunRepository.get_user_active_run(
            db,
            user_id
        )

        if active_run:

            if active_run.challenge_id != challenge_id:

                raise HTTPException(
                    status_code=409,
                    detail=(
                        "You already have an active run in another challenge. "
                        "Cancel or finish it before starting a new one."
                    )
                )

            challenge_run = active_run

        else:

            challenge_run = ChallengeRunRepository.create_run(
                db,
                user_id,
                challenge_id
            )

        try:
            solution_columns, solution_rows = run_query(challenge.solution)

        # In case Challenge solution produces error
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Challenge solution is invalid. Contact the instructor."
            )

        is_correct = compare_results(student_rows, solution_rows)

        resolution_time = None
        run_score = None
        best_score = None

        if is_correct:
            resolution_time = (
                    datetime.utcnow() - challenge_run.started_at
            ).total_seconds()

        attempt = Attempt(
            challenge_run_id=challenge_run.id,
            user_id=user_id,
            challenge_id=challenge_id,
            submitted_query=query,
            is_correct=is_correct,
            execution_time=execution_time,
            resolution_time=resolution_time,
            rows_returned=len(student_rows)
        )

        db.add(attempt)
        db.commit()

        if is_correct:

            failed_attempts = AttemptRepository.count_failed_attempts_in_run(db, challenge_run.id)

            base_points = DIFFICULTY_SCORE[challenge.difficulty]

            performance_factor = max(1 - (failed_attempts * 0.1), 0.1)

            time_factor = get_time_factor(resolution_time)

            run_score = int(base_points * performance_factor * time_factor)

            entry = LeaderboardRepository.upsert_score(
                db,
                user_id=user_id,
                challenge_id=challenge_id,
                score=run_score
            )

            best_score = entry.score
            ChallengeRunRepository.complete_run(
                db,
                challenge_run.id,
                run_score
            )

        hints = []

        if not is_correct:
            failed_attempts = AttemptRepository.count_failed_attempts_in_run(
                db,
                challenge_run.id
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
            "rows": [list(row) for row in student_rows],
        }

        if run_score is not None:
            response["run_score"] = run_score
            response["best_score"] = best_score

        if hints:
            response["hints"] = [h.content for h in hints]

        return response

    @staticmethod
    def reset_run(db, user_id, challenge_id):
        """
        Resets an already started run by closing the current one
        and immediately creating a new run.
        Used when the player wants to restart the challenge.
        """
        challenge = ChallengeRepository.get_by_id(db, challenge_id)

        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        active_run = ChallengeRunRepository.get_active_run(db, user_id, challenge_id)

        if not active_run:
            raise HTTPException(
                status_code=404,
                detail="No active run to reset"
        )

        ChallengeRunRepository.close_active_run(db, user_id, challenge_id)

        new_run = ChallengeRunRepository.create_run(
            db, user_id, challenge_id
        )

        return {
            "message": "Run reset successfully",
            "new_run_id": new_run.id
        }

    @staticmethod
    def cancel_run(db, user_id, challenge_id):
        """ Cancels the current run. """
        challenge = ChallengeRepository.get_by_id(db, challenge_id)

        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        run = ChallengeRunRepository.close_active_run(db, user_id, challenge_id)

        if not run:
            raise HTTPException(
                status_code=404,
                detail="No active run to cancel"
            )

        return {
            "message": "Run cancelled successfully"
        }
