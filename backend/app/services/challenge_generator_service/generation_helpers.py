import random

from app.services.challenge_generator_service.sql_randomizer import pick_any_column_safe

"""
Helper utilities for SQL generation.
"""


def build_select_list(table: str, alias: str | None = None, allow_two_cols_prob: float = 0.3):
    """
    Builds a safe SELECT clause using real columns.

    Guarantees:
        - Existing columns only
        - No duplicates
        - 1–2 columns max (difficulty control)
    """

    prefix = f"{alias}." if alias else ""

    col1 = pick_any_column_safe(table)
    if not col1:
        return None

    if random.random() > allow_two_cols_prob:
        return f"{prefix}{col1}"

    col2 = pick_any_column_safe(table)
    if not col2 or col2 == col1:
        return f"{prefix}{col1}"

    return f"{prefix}{col1}, {prefix}{col2}"
