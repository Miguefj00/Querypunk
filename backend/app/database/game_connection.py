import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Separate database used to run SQL challenges safely
GAME_DATABASE_URL = os.getenv("GAME_DATABASE_URL")

# Independent engine to avoid mixing game queries with system DB
game_engine = create_engine(GAME_DATABASE_URL)


def run_query(query: str):
    """
   Executes raw SQL queries against the game database.
   Used by the SQL challenge engine to validate user answers.

   Returns:
       columns -> column names of the result
       rows -> query result rows
   """
    with game_engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()

    return columns, rows
