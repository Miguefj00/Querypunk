import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database.connection import SessionLocal
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.attempt_repository import AttemptRepository
from app.database.repositories.challenge_run_repository import ChallengeRunRepository


def run():
    db = SessionLocal()

    try:
        print("Cleaning database...")

        SessionRepository.delete_old_sessions(db, days=3)
        AttemptRepository.delete_old_attempts(db, days=3)
        ChallengeRunRepository.delete_old_runs(db, days=3)

        print("Database cleanup completed")

    finally:
        db.close()


if __name__ == "__main__":
    run()
