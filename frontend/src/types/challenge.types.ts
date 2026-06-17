export type ValidationRules = {
    must_use_avg: boolean;
    must_use_subquery: boolean;
    forbid_literals: boolean;
    no_group_by: boolean;
    must_use_group_by: boolean;
    must_use_join: boolean;
    forbid_select_all: boolean;
};

export type Challenge = {
    id: number;
    title: string;
    description: string;
    solution: string;
    validation_rules: ValidationRules;
};