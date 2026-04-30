from sqlalchemy import inspect
from app.database.game_connection import game_engine
from app.utils.ai_utils import COLUMN_TYPE_GUIDE, SCHEMA_SEMANTICS


def get_structured_schema():
    inspector = inspect(game_engine)
    schema = {}

    for table in inspector.get_table_names():
        columns = inspector.get_columns(table)
        fks = inspector.get_foreign_keys(table)

        schema[table] = {
            "columns": {col["name"]: str(col["type"]) for col in columns},
            "foreign_keys": fks
        }

    return schema


def format_schema_for_llm() -> str:
    """
    Returns a semantic description of the database schema for LLM prompts.
    This version is HUMAN-READABLE and focuses on meaning, not SQL structure.
    """
    lines = []
    lines.append("DATABASE SEMANTIC SCHEMA")
    lines.append(COLUMN_TYPE_GUIDE)
    lines.append("")

    for table, table_data in SCHEMA_SEMANTICS.items():
        lines.append(f"TABLE: {table}")
        lines.append(f"Description: {table_data['description']}")

        for col, col_data in table_data["columns"].items():
            col_type = col_data["type"]
            col_desc = col_data["description"]
            lines.append(f"- {col} ({col_type}): {col_desc}")

        lines.append("")

    return "\n".join(lines)
