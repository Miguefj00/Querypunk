from fastapi import FastAPI
import app.models
from app.api import gameplay, auth, user
from fastapi.responses import RedirectResponse

from app.database.connection import Base, engine

app = FastAPI(
    title="Querypunk API",
    description="Backend del videojuego educativo Querypunk",
    version="0.1.0"
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(gameplay.router)

