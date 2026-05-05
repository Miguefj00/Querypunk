import os
import sqlite3
import json
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("GAME_SQLITE_PATH")


def generate_semantics_template():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]

    schema_semantics = {}

    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        columns = cur.fetchall()

        schema_semantics[table] = {
            "description": f"TODO: describe the role of {table} in the cyberpunk world.",
            "columns": {}
        }

        for col in columns:
            col_name = col[1]
            schema_semantics[table]["columns"][col_name] = "TODO: describe column meaning."

    print(json.dumps(schema_semantics, indent=4, ensure_ascii=False))

generate_semantics_template()


