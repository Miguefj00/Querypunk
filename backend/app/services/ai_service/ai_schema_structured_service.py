from sqlalchemy import inspect
from app.database.game_connection import game_engine


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
