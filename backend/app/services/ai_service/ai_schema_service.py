import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

GAME_SQLITE_PATH = os.getenv("GAME_SQLITE_PATH")


def get_database_schema():
    conn = sqlite3.connect(GAME_SQLITE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """)

    tables = cursor.fetchall()

    schema_text = ""

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        schema_text += f"\nTable {table_name}:\n"
        for col in columns:
            schema_text += f" - {col[1]} ({col[2]})\n"

    conn.close()
    return schema_text
