import random

from app.services.challenge_generator_service.sql_randomizer import pick_column


def random_numeric_condition(table, alias=""):
    col = pick_column(table, numeric_only=True, allow_ids=False)
    number = random.randint(1, 10)
    op = random.choice([">", "<", ">=", "<="])
    prefix = f"{alias}." if alias else ""
    return f"{prefix}{col} {op} {number}"


def random_text_condition(table, alias=""):
    col = pick_column(table, text_only=True, allow_ids=False)
    letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    prefix = f"{alias}." if alias else ""
    return f"{prefix}{col} LIKE '{letter}%'"


def random_where_clause(table, alias=""):
    if random.random() < 0.5:
        return random_numeric_condition(table, alias)
    return random_text_condition(table, alias)
