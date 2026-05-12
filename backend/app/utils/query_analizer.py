import sqlglot
from fastapi import HTTPException

"""
SQL AST analysis utilities using sqlglot.

Used to validate student queries against challenge requirements.
"""


class QueryAnalyzer:

    @staticmethod
    def parse(query: str):
        """
        Parses SQL into an Abstract Syntax Tree (AST).
        Raises HTTPException if syntax is invalid.
        """
        try:
            return sqlglot.parse_one(query)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid SQL syntax"
            )

    @staticmethod
    def has_join(parsed):
        """ Checks if query contains JOIN clauses. """
        return any(
            isinstance(node, sqlglot.expressions.Join)
            for node in parsed.walk()
        )

    @staticmethod
    def has_aggregate(parsed, func_name: str):
        """ Checks if query uses a specific aggregate function. """
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
        """ Checks if query contains a subquery. """
        return any(
            isinstance(node, sqlglot.expressions.Subquery)
            for node in parsed.walk()
        )

    @staticmethod
    def has_literal_numbers(parsed):
        """ Checks if query uses numeric literals. """
        return any(
            isinstance(node, sqlglot.expressions.Literal)
            and node.is_number
            for node in parsed.walk()
        )

    @staticmethod
    def has_limit(parsed):
        """ Checks if query uses LIMIT. """
        return parsed.args.get("limit") is not None

    @staticmethod
    def has_union(parsed):
        """ Checks if query contains UNION. """
        return any(
            isinstance(node, sqlglot.expressions.Union)
            for node in parsed.walk()
        )

    @staticmethod
    def has_group_by(parsed):
        """ Checks if query contains GROUP BY. """
        return any(
            isinstance(node, sqlglot.expressions.Group)
            for node in parsed.walk()
        )
