import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

GAME_DATABASE_URL = os.getenv("GAME_DATABASE_URL")

game_engine = create_engine(GAME_DATABASE_URL)


def run_query(query: str):
    with game_engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()

    return columns, rows
