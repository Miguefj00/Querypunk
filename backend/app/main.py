from fastapi import FastAPI
from app.api import gameplay

app = FastAPI(title="Querypunk API")

@app.get("/")
def health_check():
    return {"status": "Querypunk backend running"}

app.include_router(gameplay.router)

