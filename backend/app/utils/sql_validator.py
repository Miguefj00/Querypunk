from fastapi import HTTPException

from app.utils.query_analizer import QueryAnalyzer

"""
Student SQL query validation and result comparison utilities.

Ensures queries are safe, read-only and respect challenge constraints.
"""

# Prevent any data modification or schema manipulation
FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "PRAGMA",
    "ATTACH",
    "DETACH",
    "REPLACE",
    "CREATE"
}


def validate_query(query: str, challenge=None):
    """
    Validates a student SQL query before execution.

    Validation layers:
    1. Security validation (read-only SQL only)
    2. Global platform rules (no LIMIT, UNION, comments…)
    3. Challenge-specific rules (aggregates, subqueries, literals…)

    Raises HTTPException if validation fails.
    """
    q = query.upper().strip()

    # Basic validation
    if not q.startswith(("SELECT", "WITH")):
        raise HTTPException(400, "Query must start with SELECT or WITH")

    for word in FORBIDDEN_KEYWORDS:
        if word in q:
            raise HTTPException(400, "Only SELECT queries are allowed")

    if ";" in q[:-1]:
        raise HTTPException(400, "Multiple SQL statements are not allowed")

    if "--" in q or "/*" in q:
        raise HTTPException(400, "Comments are not allowed")

    # Parse
    parsed = QueryAnalyzer.parse(query)

    # Global rules
    if QueryAnalyzer.has_limit(parsed):
        raise HTTPException(400, "LIMIT not allowed")

    if QueryAnalyzer.has_union(parsed):
        raise HTTPException(400, "UNION not allowed")

    # Challenge rules
    if not challenge:
        return

    rules = getattr(challenge, "validation_rules", None)
    if not rules:
        return

    # Mandatory AVG
    if rules.get("must_use_avg"):
        if not QueryAnalyzer.has_aggregate(parsed, "avg"):
            raise HTTPException(400, "You must use AVG()")

    # Mandatory subquery
    if rules.get("must_use_subquery"):
        if not QueryAnalyzer.has_subquery(parsed):
            raise HTTPException(400, "You must use a subquery")

    # Forbidden number hardcode
    if rules.get("forbid_literals"):
        if QueryAnalyzer.has_literal_numbers(parsed):
            raise HTTPException(400, "Hardcoded values are not allowed")

    # Forbidden GROUP_BY in case challenge doesn't ask for it
    if rules.get("no_group_by"):
        if QueryAnalyzer.has_group_by(parsed):
            raise HTTPException(400, "GROUP BY not allowed")


def compare_results(student_rows, solution_rows):
    """
    Compares query results ignoring row order.

    Sorting ensures that equivalent result sets
    are considered correct even if ordering differs.
    """
    return sorted(student_rows) == sorted(solution_rows)
