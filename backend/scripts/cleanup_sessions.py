from app.database.connection import SessionLocal
from app.database.repositories.session_repository import SessionRepository


def run():

    db = SessionLocal()

    try:
        SessionRepository.delete_old_sessions(db, days=5)
        print("Old sessions cleaned")
    finally:
        db.close()


if __name__ == "__main__":
    run()
