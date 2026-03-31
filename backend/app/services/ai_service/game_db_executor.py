import os
import sqlite3
from dotenv import load_dotenv
import json

load_dotenv()

GAME_SQLITE_PATH = os.getenv("GAME_SQLITE_PATH")
SYSTEM_SQLITE_PATH = os.getenv("SYSTEM_SQLITE_PATH")


def execute_query_and_get_expected(sql_query:str):
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


def save_challenge_to_db(chapter:int, challenge, expected_rows, hints):

    conn = sqlite3.connect(SYSTEM_SQLITE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO challenge (chapter_id, title, description, solution, validation_rules, generated_by_ai)
        VALUES (?, ?, ?, ?, ?, 1)
    """, (
        chapter,
        challenge["title"],
        challenge["description"],
        challenge["sql_query"],
        json.dumps(expected_rows)
    ))

    challenge_id = cursor.lastrowid

    for i, hint in enumerate(hints):
        cursor.execute("""
            INSERT INTO hint (challenge_id, content, order_index, unlock_after_attempts)
            VALUES (?, ?, ?, ?)
        """, (challenge_id, hint, i+1, 3))

    conn.commit()
    conn.close()

