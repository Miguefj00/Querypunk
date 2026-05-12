import re
import sqlite3

from app.services.challenge_generator_service.game_db_executor import SYSTEM_SQLITE_PATH
from app.services.challenge_generator_service.schema_structured_service import get_structured_schema

"""
Challenge Quality Validators

These validators ensure that generated SQL challenges are:

    - Unique (no duplicates)
    - Pedagogically appropriate
    - Technically valid
    - Immersive in narrative tone

These checks run BEFORE the AI narrative phase.
"""


def is_duplicate_query(sql: str):
    """ Prevents generating identical SQL challenges. """
    conn = sqlite3.connect(SYSTEM_SQLITE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM challenge WHERE solution = ?", (sql,))
    count = cursor.fetchone()[0]
    conn.close()

    return count > 0


def uses_forbidden_columns(sql: str):
    """ Detects usage of technical ID columns in SELECT. """
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


def title_not_immersive(title: str):
    """ Validates that the AI-generated title is immersive. """
    forbidden = ["SQL", "Database", "Query", "Table", "Column"]
    return any(word.lower() in title.lower() for word in forbidden)


def has_type_mismatch(sql: str) -> bool:
    """
    Detects numeric comparisons applied to non-numeric columns.

    Example of invalid SQL:
        name > 5
    """
    schema = get_structured_schema()
    sql_lower = sql.lower()

    pattern = r"(\w+)\s*(>|<|>=|<=)\s*(\d+)"
    matches = re.findall(pattern, sql_lower)

    for column, op, number in matches:
        # If a column is not numeric but used in a numeric comparison,
        # the query is considered invalid.
        for table in schema:
            cols = schema[table]["columns"]
            if column in [c.lower() for c in cols]:
                col_type = cols[next(c for c in cols if c.lower()==column)]

                numeric_types = ["INT","INTEGER","REAL","NUMERIC","FLOAT","DOUBLE"]
                is_numeric = any(t in col_type.upper() for t in numeric_types)

                if not is_numeric:
                    return True  # mismatch real

    return False
