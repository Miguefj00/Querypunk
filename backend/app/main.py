from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import gameplay_router, auth_router, user_router, chapter_router, challenge_router, group_router, \
    hint_router, leaderboard_router, generator_and_ai_router, analytics_router, game_settings_router
from fastapi.responses import RedirectResponse

from app.database.connection import Base, engine

"""
Querypunk Backend Application Entry Point.

Initializes the FastAPI app, database and registers all routers.
"""

app = FastAPI(
    title="Querypunk API",
    description="Backend del videojuego serio Querypunk",
    openapi_tags=[
        {"name": "Auth", "description": "Responsible for authentication and session management"},
        {"name": "Users", "description": "CRUD operations for users and password management"},
        {"name": "Groups", "description": "CRUD operations for groups and students groups/classes management"},
        {"name": "Chapters", "description": "CRUD operations for chapters"},
        {"name": "Challenges", "description": "CRUD operations for challenges"},
        {"name": "Hints", "description": "CRUD operations for hints"},
        {"name": "Gameplay", "description": "Entry point for the SQL gameplay engine"},
        {"name": "Leaderboard", "description": "Game ranking endpoints"},
        {"name": "Analytics", "description": "Responsible for exposing learning analytics"},
        {"name": "Challenges_generator", "description": "Automatic challenge generation and AI narrative endpoint"},
    ],
    version="0.1.0"
)


@app.get("/", include_in_schema=False)
def root():
    """ Redirects base URL to interactive Swagger documentation. """
    return RedirectResponse(url="/docs")


# React frontend Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# API routers grouped by domain
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(group_router.router)
app.include_router(chapter_router.router)
app.include_router(challenge_router.router)
app.include_router(hint_router.router)
app.include_router(generator_and_ai_router.router)
app.include_router(gameplay_router.router)
app.include_router(leaderboard_router.router)
app.include_router(analytics_router.router)
app.include_router(game_settings_router.router)

