import sys
from pathlib import Path

# Allow script execution from project root when run as standalone
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database.connection import SessionLocal
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.attempt_repository import AttemptRepository
from app.database.repositories.challenge_run_repository import ChallengeRunRepository

"""
Periodic database cleanup script.

This script removes old data generated during gameplay:
- Expired sessions
- Old attempts
- Old challenge runs

It is executed automatically by Windows Task Scheduler
to prevent uncontrolled database growth.
"""


def run():
    """
    Executes database cleanup tasks.

    Deletes data older than 3 days to keep the system lightweight
    and avoid storing unnecessary gameplay telemetry indefinitely.
    """
    db = SessionLocal()  # Create DB session for maintenance operations

    try:
        print("Cleaning database...")

        # Remove expired authentication sessions
        SessionRepository.delete_old_sessions(db, days=30)
        # Remove old SQL attempts history
        AttemptRepository.delete_old_attempts(db, days=30)
        # Remove old challenge runs history
        ChallengeRunRepository.delete_old_runs(db, days=30)

        print("Database cleanup completed")

    finally:
        db.close()  # Ensure DB connection is always closed


if __name__ == "__main__":
    # Entry point when executed as standalone script
    run()
