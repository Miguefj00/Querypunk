from fastapi import FastAPI
from app.api import gameplay
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Querypunk API",
    description="Backend del videojuego educativo Querypunk",
    version="0.1.0"
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(gameplay.router)

