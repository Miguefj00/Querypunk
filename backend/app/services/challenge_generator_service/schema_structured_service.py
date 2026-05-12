from sqlalchemy import inspect
from app.database.game_connection import game_engine
from app.utils.ai_utils import COLUMN_TYPE_GUIDE, SCHEMA_SEMANTICS

"""
Schema Structured Service

This module exposes the database schema in two different formats:

1) Structured schema (technical)
   → Used internally by the SQL generators and validators.

2) Semantic schema (human-readable)
   → Used in LLM prompts so the AI understands the meaning of the data.
"""


def get_structured_schema():
    """
    Returns a dictionary structure:
    {
        table_name: {
            "columns": { column_name: column_type },
            "foreign_keys": [...]
        }
    }

    This structure is used by:
        - SQL random generator
        - Validators
        - Join discovery logic
    """
    inspector = inspect(game_engine)
    schema = {}

    for table in inspector.get_table_names():
        # SQLAlchemy inspector provides runtime DB introspection.
        # This allows the generator to adapt automatically if the schema changes.
        columns = inspector.get_columns(table)
        fks = inspector.get_foreign_keys(table)

        schema[table] = {
            "columns": {col["name"]: str(col["type"]) for col in columns},
            "foreign_keys": fks
        }

    return schema


def format_schema_for_llm() -> str:
    """
    Builds a semantic description of the database schema for LLM prompts.

    It focuses on:
        - Meaning of the tables
        - Meaning of the columns
        - Column data types in human language
    """
    lines = []
    lines.append("DATABASE SEMANTIC SCHEMA")
    lines.append(COLUMN_TYPE_GUIDE)
    lines.append("")

    for table, table_data in SCHEMA_SEMANTICS.items():
        # SCHEMA_SEMANTICS is manually curated to describe
        # the *meaning* of the data instead of its structure.
        lines.append(f"TABLE: {table}")
        lines.append(f"Description: {table_data['description']}")

        for col, col_data in table_data["columns"].items():
            col_type = col_data["type"]
            col_desc = col_data["description"]
            lines.append(f"- {col} ({col_type}): {col_desc}")

        lines.append("")

    return "\n".join(lines)
