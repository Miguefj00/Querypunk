from fastapi import HTTPException

FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "PRAGMA",
    "ATTACH"
]


def validate_query(query: str):

    q = query.upper()

    for word in FORBIDDEN_KEYWORDS:
        if word in q:
            raise HTTPException(
                status_code=400,
                detail="Only SELECT queries are allowed"
            )

    if not q.strip().startswith(("SELECT", "WITH")):
        raise HTTPException(
            status_code=400,
            detail="Query must start with SELECT or WITH"
        )


def compare_results(student_rows, solution_rows):
    return sorted(student_rows) == sorted(solution_rows)
