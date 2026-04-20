import re

from app.schemas.challenge import ValidationRules

DIFFICULTY_TO_VALUE = {
    "VERY_EASY": 1,
    "EASY": 2,
    "MEDIUM": 3,
    "HARD": 4,
    "EXPERT": 5,
}

DIFFICULTY_SCORE = {
    "VERY_EASY": 50,
    "EASY": 100,
    "MEDIUM": 200,
    "HARD": 350,
    "EXPERT": 500,
}

VALUE_TO_DIFFICULTY = {v: k for k, v in DIFFICULTY_TO_VALUE.items()}


def get_time_factor(seconds: float) -> float:
    if seconds < 60:
        return 1.3
    if seconds < 180:
        return 1.15
    if seconds < 300:
        return 1.0
    if seconds < 600:
        return 0.9
    if seconds < 1200:
        return 0.75
    return 0.6


def evaluate_sql_difficulty(sql: str, rules: ValidationRules) -> str:
    sql = sql.lower().strip()

    score = 1

    # ----------------------
    #     SQL Complexity
    # ----------------------
    if "where" in sql:
        score += 1

    if re.search(r"\b(and|or)\b", sql):
        score += 1

    if "join" in sql:
        score += 2

    if "group by" in sql:
        score += 2

    if "having" in sql:
        score += 1

    if any(func in sql for func in ["avg(", "count(", "sum(", "min(", "max("]):
        score += 1

    if "order by" in sql:
        score += 1

    if "limit" in sql:
        score += 1

    if "select distinct" in sql:
        score += 1

    if "case" in sql:
        score += 2

    if re.search(r"select .*select", sql):
        score += 3

    # ----------------------
    #    VALIDATION RULES
    # ----------------------
    if rules.must_use_join:
        score += 2

    if rules.must_use_group_by:
        score += 2

    if rules.must_use_avg:
        score += 1

    if rules.must_use_subquery:
        score += 3

    if rules.forbid_literals:
        score += 1

    if rules.no_group_by:
        score -= 1

    # ----------------------
    #       NORMALIZE
    # ----------------------
    score = max(1, min(score, 5))
    return VALUE_TO_DIFFICULTY[score]

