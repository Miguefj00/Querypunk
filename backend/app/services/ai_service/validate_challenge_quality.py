import sqlite3

from app.services.ai_service.game_db_executor import SYSTEM_SQLITE_PATH


def is_duplicate_query(sql: str):
    conn = sqlite3.connect(SYSTEM_SQLITE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM challenge WHERE solution = ?", (sql,))
    count = cursor.fetchone()[0]
    conn.close()

    return count > 0


def validate_language(challenge):
    title = challenge["title"]
    desc = challenge["description"]

    if any(c in title for c in "ñáéíóú"):
        return False

    spanish_markers = [" el ", " la ", " los ", " las ", " obtiene ", " lista "]
    if not any(w in desc.lower() for w in spanish_markers):
        return False

    return True


def uses_forbidden_columns(sql: str):
    sql_lower = sql.lower()

    forbidden_patterns = [
        "select id ",
        "select id,",
        "select id\n",
        "select id\t",
        "_id from",
        "_id,",
    ]

    return any(pattern in sql_lower for pattern in forbidden_patterns)