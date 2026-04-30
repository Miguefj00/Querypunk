import sqlglot
from fastapi import HTTPException


class QueryAnalyzer:

    @staticmethod
    def parse(query: str):
        try:
            return sqlglot.parse_one(query)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid SQL syntax"
            )

    @staticmethod
    def has_join(parsed):
        return any(
            isinstance(node, sqlglot.expressions.Join)
            for node in parsed.walk()
        )

    @staticmethod
    def has_aggregate(parsed, func_name: str):
        func_name = func_name.lower()

        aggregates = {
            "avg": sqlglot.expressions.Avg,
            "count": sqlglot.expressions.Count,
            "sum": sqlglot.expressions.Sum,
            "min": sqlglot.expressions.Min,
            "max": sqlglot.expressions.Max,
        }

        target = aggregates.get(func_name)

        if not target:
            return False

        return any(
            isinstance(node, target)
            for node in parsed.walk()
        )

    @staticmethod
    def has_subquery(parsed):
        return any(
            isinstance(node, sqlglot.expressions.Subquery)
            for node in parsed.walk()
        )

    @staticmethod
    def has_literal_numbers(parsed):
        return any(
            isinstance(node, sqlglot.expressions.Literal)
            and node.is_number
            for node in parsed.walk()
        )

    @staticmethod
    def has_limit(parsed):
        return parsed.args.get("limit") is not None

    @staticmethod
    def has_union(parsed):
        return any(
            isinstance(node, sqlglot.expressions.Union)
            for node in parsed.walk()
        )

    @staticmethod
    def has_group_by(parsed):
        return any(
            isinstance(node, sqlglot.expressions.Group)
            for node in parsed.walk()
    )
