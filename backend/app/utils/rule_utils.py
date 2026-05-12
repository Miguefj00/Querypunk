"""
Default SQL validation rules used by generated challenges.

Each rule toggles a constraint enforced during query validation.
These rules are stored as JSON inside the Challenge model.
"""

DEFAULT_RULES = {
    "must_use_avg": False,
    "must_use_subquery": False,
    "forbid_literals": False,
    "no_group_by": False,
    "must_use_group_by": False,
    "must_use_join": False,
    "forbid_select_all": False,
}
