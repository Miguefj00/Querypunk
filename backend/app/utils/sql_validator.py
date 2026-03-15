from fastapi import HTTPException

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


def validate_query(query: str):

    q = query.upper().strip()

    if not q.startswith(("SELECT", "WITH")):
        raise HTTPException(
            status_code=400,
            detail="Query must start with SELECT or WITH"
        )

    for word in FORBIDDEN_KEYWORDS:
        if word in q:
            raise HTTPException(
                status_code=400,
                detail="Only SELECT queries are allowed"
            )

    if ";" in q[:-1]:
        raise HTTPException(
            status_code=400,
            detail="Multiple SQL statements are not allowed"
        )


def compare_results(student_rows, solution_rows):
    return sorted(student_rows) == sorted(solution_rows)
