import time
from app.models.attempt import Attempt
from app.database.repositories.challenge_repository import ChallengeRepository
from app.database.game_connection import run_query
from app.utils.sql_validator import compare_results, validate_query


class GameplayService:

    @staticmethod
    def submit_query(db, user_id, challenge_id, query):
        validate_query(query)

        challenge = ChallengeRepository.get_by_id(db, challenge_id)

        if not challenge:
            raise ValueError("Challenge not found")

        start = time.time()

        student_columns, student_rows = run_query(query)

        execution_time = time.time() - start

        solution_columns, solution_rows = run_query(challenge.solution)

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

        return {
            "correct": is_correct,
            "rows_returned": len(student_rows),
            "columns": list(student_columns),
            "rows": [list(row) for row in student_rows]
        }
