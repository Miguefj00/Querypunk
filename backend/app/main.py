from fastapi import FastAPI
from app.api import gameplay_router, auth_router, user_router, chapter_router, challenge_router, group_router, \
    hint_router
from fastapi.responses import RedirectResponse

from app.database.connection import Base, engine, SessionLocal
from app.database.repositories.session_repository import SessionRepository

app = FastAPI(
    title="Querypunk API",
    description="Backend del videojuego serio Querypunk",
    version="0.1.0"
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.on_event("startup")
def cleanup_sessions():

    db = SessionLocal()

    try:
        SessionRepository.delete_old_sessions(db, 5)
        print("Old sessions cleaned")
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(group_router.router)
app.include_router(chapter_router.router)
app.include_router(challenge_router.router)
app.include_router(hint_router.router)
app.include_router(gameplay_router.router)

