import random
from app.services.challenge_generator_service.schema_structured_service import get_structured_schema
from app.services.challenge_generator_service.get_recent_tables_usage import get_recent_tables_usage

"""
SQL Randomizer

This module is responsible for selecting tables, columns and joins
in a SAFE and CONTROLLED way.

The goal is to generate realistic SQL queries while avoiding:
    - Technical/internal columns (IDs, timestamps)
    - Boolean-like fields used incorrectly
    - Overused tables (to improve content variety)
"""

# Columns that should never appear in generated challenges.
FORBIDDEN_COLUMNS = {
    "id",
    "Id",
    "_id",
    "created_at",
    "updated_at",
    "timestamp"
}

# Column names that usually represent booleans.
BOOLEAN_KEYWORDS = [
    "main",
    "legality"
]

# Tables excluded from generation.
FORBIDDEN_TABLES = {
    "Corporation_sector",
    "Personnel_implant",
}

# For AVG/MAX/MIN
AGGREGABLE_COLUMNS = {
    "Corporation": [
        "Net_worth",
        "Influence_lvl"
    ],

    "Data_leak": [
        "Files_number",
        "Confidentiality_lvl"
    ],

    "District": [
        "Population",
        "Danger_lvl"
    ],

    "Headquarter": [
        "Employees",
        "Security_lvl"
    ],

    "Implant": [
        "Power_consumption"
    ],

    "Security_incident": [
        "Severity"
    ],

    "Personnel": [
        "Salary"
    ],

    "Sector": [
        "Budget"
    ]
}


def pick_table():
    """
   Selects a table with variety bias.

   Strategy:
       - Avoid forbidden tables
       - Prefer tables that were NOT recently used
       - Fall back to all allowed tables if needed

   This keeps the generated challenges diverse.
   """
    schema = get_structured_schema()
    most_used, least_used = get_recent_tables_usage()

    all_tables = list(schema.keys())

    allowed_tables = [t for t in all_tables if t not in FORBIDDEN_TABLES]

    candidates = [t for t in least_used if t in allowed_tables] if least_used else allowed_tables

    return random.choice(candidates)


def pick_column(table, numeric_only=False, text_only=False, allow_ids=False):
    """
    Selects a valid column from a table applying multiple filters:

    Filters applied:
        - Remove technical columns (ids, timestamps)
        - Optional numeric-only / text-only filtering
        - Avoid boolean-like columns in numeric comparisons
    """
    schema = get_structured_schema()
    columns = schema[table]["columns"]

    numeric_types = ["INT", "INTEGER", "REAL", "NUMERIC", "FLOAT", "DOUBLE"]
    text_types = ["CHAR", "VARCHAR", "TEXT", "CLOB"]

    valid_cols = []

    for col, col_type in columns.items():
        # Boolean-like columns are excluded from numeric comparisons
        # to prevent unrealistic conditions.
        col_lower = col.lower()

        is_boolean = any(k in col_lower for k in BOOLEAN_KEYWORDS)

        if not allow_ids:
            col_lower = col.lower()
            if col_lower in FORBIDDEN_COLUMNS or col_lower.endswith("_id"):
                continue

        if numeric_only:
            if not any(t in col_type for t in numeric_types):
                continue
            if is_boolean:
                continue

        if text_only and not any(t in col_type for t in text_types):
            continue

        valid_cols.append(col)

    if not valid_cols:
        return None

    return random.choice(valid_cols) if valid_cols else None


def pick_numeric_column_safe(table, tries=15):
    """ Retries numeric column selection multiple times for robustness. """
    for _ in range(tries):
        col = pick_column(table, numeric_only=True, allow_ids=False)
        if col:
            return col
    return None


def get_numeric_columns(table):
    """
    Returns all numeric columns of a table,
    excluding ids and boolean-like columns.
    """

    schema = get_structured_schema()

    columns = schema[table]["columns"]

    numeric_types = [
        "INT",
        "INTEGER",
        "REAL",
        "NUMERIC",
        "FLOAT",
        "DOUBLE",
        "DECIMAL"
    ]

    valid = []

    for col, col_type in columns.items():

        col_lower = col.lower()

        if (
                col_lower in FORBIDDEN_COLUMNS
                or col_lower.endswith("_id")
        ):
            continue

        if is_boolean_like(col):
            continue

        if any(t in col_type.upper() for t in numeric_types):
            valid.append(col)

    return valid


def pick_avg_column_safe(table):

    allowed = AGGREGABLE_COLUMNS.get(table)

    if not allowed:
        return None

    cols = get_numeric_columns(table)

    allowed_lower = {
        c.lower()
        for c in allowed
    }

    valid = [
        c
        for c in cols
        if c.lower() in allowed_lower
    ]

    if not valid:
        return None

    return random.choice(valid)


def is_boolean_like(col):

    name = col.lower()

    return any(x in name for x in BOOLEAN_KEYWORDS)


def pick_text_column_safe(table, tries=15):
    """ Retries text column selection multiple times for robustness. """
    for _ in range(tries):
        col = pick_column(table, text_only=True, allow_ids=False)
        if col:
            return col
    return None


def pick_any_column_safe(table, tries=15):
    """ Retries generic column selection multiple times for robustness. """
    for _ in range(tries):
        col = pick_column(table, allow_ids=False)
        if col:
            return col
    return None


def pick_join():
    """
   Automatically discovers valid JOIN relationships using FK metadata.

   Returns:
       (table_a, table_b, column_a, column_b)

   This ensures all generated joins are valid and executable.
   """
    schema = get_structured_schema()
    tables = [t for t in schema.keys() if t not in FORBIDDEN_TABLES]
    random.shuffle(tables)

    valid_joins = []

    for table in tables:
        # We only accept joins backed by real foreign keys.
        fks = schema[table]["foreign_keys"]

        for fk in fks:
            ref_table = fk.get("referred_table")

            if ref_table in FORBIDDEN_TABLES:
                continue

            if not ref_table:
                continue

            if not fk.get("constrained_columns"):
                continue

            if not fk.get("referred_columns"):
                continue

            valid_joins.append((
                table,
                ref_table,
                fk["constrained_columns"][0],
                fk["referred_columns"][0]
            ))

    if not valid_joins:
        return None

    return random.choice(valid_joins)


def is_parent_child_join(join):
    """
    Returns True if join:

    parent.id -> child.parent_id
    """
    t1, t2, col1, col2 = join

    return (
            col1.lower() == "id"
            and col2.lower().endswith("_id")
    )