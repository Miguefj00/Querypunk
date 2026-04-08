from sqlalchemy import inspect
from app.database.game_connection import game_engine


def get_database_schema() -> str:
    inspector = inspect(game_engine)
    conn = game_engine.raw_connection()
    cursor = conn.cursor()

    blocks = []

    for table in inspector.get_table_names():

        columns = inspector.get_columns(table)

        col_lines = []
        for col in columns:
            col_lines.append(f"- {col['name']} ({col['type']})")

        columns_text = "\n".join(col_lines)

        fks = inspector.get_foreign_keys(table)

        if fks:
            fk_lines = []
            for fk in fks:
                local_cols = ", ".join(fk["constrained_columns"])
                remote_cols = ", ".join(fk["referred_columns"])
                fk_lines.append(
                    f"- {local_cols} → {fk['referred_table']}.{remote_cols}"
                )
            fk_text = "\n".join(fk_lines)
        else:
            fk_text = "Sin claves foráneas"

        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            rows = cursor.fetchall()
            rows_text = "\n".join([str(r) for r in rows]) if rows else "Tabla vacía"
        except:
            rows_text = "No disponible"

        block = f"""
            TABLA: {table}
            
            COLUMNAS:
            {columns_text}
            
            FOREIGN KEYS:
            {fk_text}
            
            EJEMPLOS DE FILAS:
            {rows_text}
        """
        blocks.append(block)

    conn.close()
    return "\n\n".join(blocks)