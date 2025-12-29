from fastapi import FastAPI
from app.api import gameplay

app = FastAPI(
    title="Querypunk API",
    description="Backend del videojuego educativo Querypunk",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "Querypunk backend running"}

app.include_router(gameplay.router)

