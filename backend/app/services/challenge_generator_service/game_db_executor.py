import os
import sqlite3
from dotenv import load_dotenv
import json

from app.services.chapter_service import ChapterService

load_dotenv()

GAME_SQLITE_PATH = os.getenv("GAME_SQLITE_PATH")
SYSTEM_SQLITE_PATH = os.getenv("SYSTEM_SQLITE_PATH")

"""
Game Database Executor

This module acts as the bridge between:
    - Game SQLite database (read-only gameplay data)
    - System SQLite database (challenges, hints, metadata)

Separation of databases is intentional:
    GAME DB   → student queries run here
    SYSTEM DB → platform data lives here
"""


def execute_query_and_get_expected(sql_query:str):
    """ Executes generated SQL on the GAME database to obtain expected results. """
    conn = sqlite3.connect(GAME_SQLITE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        return None


def save_challenge_to_db(chapter:int, challenge, expected_rows, hints, difficulty):
    """
    Persists generated challenge and hints into the SYSTEM database.
    Also triggers chapter difficulty recalculation.
    """
    conn = sqlite3.connect(SYSTEM_SQLITE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO challenge (
            chapter_id, title, description, solution,
            expected_result, validation_rules, difficulty, generated_by_system
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """, (
        chapter,
        challenge["title"],
        challenge["description"],
        challenge["sql_query"],
        json.dumps(expected_rows),
        None,
        difficulty
    ))

    challenge_id = cursor.lastrowid

    for i, hint in enumerate(hints):
        cursor.execute("""
            INSERT INTO hint (challenge_id, content, order_index, unlock_after_attempts)
            VALUES (?, ?, ?, ?)
        """, (challenge_id, hint, i+1, i+2))

    conn.commit()

    ChapterService.recalculate_chapter_difficulty_sqlite(conn, chapter)

    conn.commit()
    conn.close()


def run_solution_and_get_result(_, sql: str):
    """ Executes student SQL in read-only mode. """
    try:
        conn = sqlite3.connect(f"file:{GAME_SQLITE_PATH}?mode=ro", uri=True)
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        return [list(row) for row in rows]

    except Exception:
        return None


def get_column_numeric_range(table: str, column: str):
    """
    Returns real MIN/MAX values from the game database.
    This prevents generating unrealistic conditions.
    """
    conn = sqlite3.connect(GAME_SQLITE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT MIN({column}), MAX({column}) FROM {table}")
        result = cursor.fetchone()
        conn.close()

        if not result or result[0] is None or result[1] is None:
            return None

        return result
    except:
        conn.close()
        return None


def get_random_existing_value(table: str, column: str):
    """ Returns a random existing value from the DB. """
    conn = sqlite3.connect(GAME_SQLITE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT {column}
            FROM {table}
            WHERE {column} IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()

        if not result:
            return None

        return result[0]
    except:
        conn.close()
        return None