import random
from app.services.challenge_generator_service.schema_structured_service import get_structured_schema
from app.services.challenge_generator_service.get_recent_tables_usage import get_recent_tables_usage

FORBIDDEN_COLUMNS = {
    "id",
    "Id",
    "_id",
    "created_at",
    "updated_at",
    "timestamp"
}

BOOLEAN_KEYWORDS = [
    "Main",
    "Legality"
]

FORBIDDEN_TABLES = {
    "Corporation_sector",
    "Personnel_implant",
}


def pick_table():
    schema = get_structured_schema()
    most_used, least_used = get_recent_tables_usage()

    all_tables = list(schema.keys())

    allowed_tables = [t for t in all_tables if t not in FORBIDDEN_TABLES]

    candidates = [t for t in least_used if t in allowed_tables] if least_used else allowed_tables

    return random.choice(candidates)


def pick_column(table, numeric_only=False, text_only=False, allow_ids=False):
    schema = get_structured_schema()
    columns = schema[table]["columns"]

    numeric_types = ["INT", "INTEGER", "REAL", "NUMERIC", "FLOAT", "DOUBLE"]
    text_types = ["CHAR", "VARCHAR", "TEXT", "CLOB"]

    valid_cols = []

    for col, col_type in columns.items():
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
        valid_cols = list(columns.keys())

    return random.choice(valid_cols)


def pick_join():
    schema = get_structured_schema()
    tables = [t for t in schema.keys() if t not in FORBIDDEN_TABLES]
    random.shuffle(tables)

    valid_joins = []

    for table in tables:
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
