from app.database.connection import SessionLocal


# Dependency used by FastAPI to provide a DB session per request.
# The session is automatically closed after the request finishes.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
