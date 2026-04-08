import random
from app.services.ai_service.ai_schema_structured_service import get_structured_schema
from app.services.ai_service.get_recent_tables_usage import get_recent_tables_usage

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


def pick_table():
    schema = get_structured_schema()
    most_used, least_used = get_recent_tables_usage()

    candidates = least_used if least_used else list(schema.keys())

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
    tables = list(schema.keys())
    random.shuffle(tables)

    valid_joins = []

    for table in tables:
        fks = schema[table]["foreign_keys"]

        for fk in fks:
            if not fk.get("referred_table"):
                continue

            if not fk.get("constrained_columns"):
                continue

            if not fk.get("referred_columns"):
                continue

            if len(fk["constrained_columns"]) == 0:
                continue

            if len(fk["referred_columns"]) == 0:
                continue

            valid_joins.append((
                table,
                fk["referred_table"],
                fk["constrained_columns"][0],
                fk["referred_columns"][0]
            ))

    if not valid_joins:
        return None

    return random.choice(valid_joins)
