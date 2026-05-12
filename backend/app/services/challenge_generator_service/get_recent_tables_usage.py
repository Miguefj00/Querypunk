import re
import sqlite3

from sqlalchemy import inspect
from typing_extensions import Counter

from app.database.game_connection import game_engine
from app.services.challenge_generator_service.game_db_executor import SYSTEM_SQLITE_PATH

"""
Table Usage Analyzer

Tracks which tables were recently used in generated challenges.
Used to promote variety and avoid repetitive content.
"""


def get_all_table_names():
    """ Returns all table names from the game database schema. """
    inspector = inspect(game_engine)
    return inspector.get_table_names()


def get_recent_tables_usage(limit=20):
    """
    Analyzes the most recently generated challenges and extracts
    which tables were used in their SQL solutions.

    Returns:
        - Most used tables
        - Least used tables (never used recently)
    """
    all_game_tables = get_all_table_names()
    conn = sqlite3.connect(SYSTEM_SQLITE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT solution FROM challenge
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    sqls = [r[0].lower() for r in rows]

    tables = []
    for sql in sqls:
        tables += re.findall(r"from\s+([a-z_]+)", sql)
        tables += re.findall(r"join\s+([a-z_]+)", sql)

    counter = Counter(tables)

    most_used = [t for t, _ in counter.most_common(5)]
    least_used = [t for t in all_game_tables if t not in counter]

    return most_used, least_used

