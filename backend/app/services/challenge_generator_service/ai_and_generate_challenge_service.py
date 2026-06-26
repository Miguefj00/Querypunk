import ollama
import json

import random

from app.services.challenge_generator_service.ai_hint_service import generate_hints
from app.services.challenge_generator_service.generation_helpers import build_select_list
from app.services.challenge_generator_service.schema_structured_service import format_schema_for_llm
from app.services.challenge_generator_service.sql_randomizer import (pick_table, pick_join,
                                                                     pick_numeric_column_safe, pick_text_column_safe,
                                                                     pick_any_column_safe)
from app.services.challenge_generator_service.validate_challenge_quality import (is_duplicate_query,
                                                                                 uses_forbidden_columns,
                                                                                 title_not_immersive, has_type_mismatch,
                                                                                 uses_forbidden_constructs)
from app.services.chapter_service import ChapterService
from app.utils.ai_utils import clean_llm_json, GAME_WORLD_CONTEXT, COLUMN_TYPE_GUIDE, SCHEMA_SEMANTICS
from dotenv import load_dotenv

from app.services.challenge_generator_service.game_db_executor import (execute_query_and_get_expected,
                                                                       save_challenge_to_db, get_column_numeric_range,
                                                                       get_random_existing_value)
from app.utils.difficulty_utils import DIFFICULTY_TO_VALUE
from app.utils.query_analizer import QueryAnalyzer

load_dotenv()

MODEL = "llama3"


"""
AI + Procedural SQL Challenge Generator

This module is the core of the automatic challenge generation pipeline.

The generation pipeline has TWO major phases:

PHASE 1 — Procedural SQL generation (NO AI)
------------------------------------------
We generate a valid SQL query using deterministic + random rules.
The query must pass strict validators:
    - Not duplicated
    - Executable against the game DB
    - Returns rows
    - No forbidden columns
    - No type mismatches

PHASE 2 — AI narrative generation (LLM)
---------------------------------------
Once a valid SQL exists, the LLM generates:
    - Immersive title
    - Natural language description
    - Progressive hints

AI narrative is in testing phase, it becomes less accurate as the challenge difficulty increases
"""


def alias(table: str):
    """ Returns a short alias for a table (first letter). Used in JOIN queries. """
    return table[0]


def generate_very_easy_sql():
    """
    Generates the simplest possible SQL query.

    Characteristics:
    - Single table
    - No WHERE clause
    - No joins
    - No aggregation

    This difficulty is meant for learning SELECT.
    """
    table = pick_table()

    select_list = build_select_list(table, allow_two_cols_prob=0.5)
    if not select_list:
        return None

    return f"SELECT {select_list} FROM {table}"


def generate_easy_sql():
    """
    Generates single-table queries with a WHERE clause.

    Two main patterns:
        • Numeric filtering (>, <, =, BETWEEN, !=)
        • Text filtering (LIKE, =, prefix matching)

    Real DB statistics are used when possible to avoid unrealistic values.
    """
    table = pick_table()
    select_list = build_select_list(table, allow_two_cols_prob=0.35)
    if not select_list:
        return None

    mode = random.choice(["numeric", "text"])

    # ───────────── NUMERIC ─────────────
    # We use real MIN/MAX values from the DB when possible.
    # This prevents nonsense conditions like "salary > 3".
    if mode == "numeric":
        col = pick_numeric_column_safe(table)
        if not col:
            return None

        range_vals = get_column_numeric_range(table, col)

        if not range_vals:
            number = random.randint(1, 10)
            return f"SELECT {select_list} FROM {table} WHERE {col} > {number}"

        min_val, max_val = range_vals
        pattern = random.choice(["greater","lower","equal","between","not_equal"])

        if pattern == "greater":
            value = random.randint(int(min_val), int(max_val))
            return f"SELECT {select_list} FROM {table} WHERE {col} > {value}"

        if pattern == "lower":
            value = random.randint(int(min_val), int(max_val))
            return f"SELECT {select_list} FROM {table} WHERE {col} < {value}"

        if pattern == "equal":
            value = random.randint(int(min_val), int(max_val))
            return f"SELECT {select_list} FROM {table} WHERE {col} = {value}"

        if pattern == "not_equal":
            value = random.randint(int(min_val), int(max_val))
            return f"SELECT {select_list} FROM {table} WHERE {col} != {value}"

        v1 = random.randint(int(min_val), int(max_val))
        v2 = random.randint(int(min_val), int(max_val))
        low, high = min(v1, v2), max(v1, v2)

        return f"SELECT {select_list} FROM {table} WHERE {col} BETWEEN {low} AND {high}"

    # ───────────── TEXT ─────────────
    # We try to reuse real values from the DB.
    # If unavailable, we fallback to realistic LIKE patterns.
    col = pick_text_column_safe(table)
    if not col:
        return None

    value = get_random_existing_value(table, col)

    if not value:
        letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"SELECT {select_list} FROM {table} WHERE {col} LIKE '{letter}%'"

    pattern = random.choice(["starts","equal","contains"])

    if pattern == "starts":
        return f"SELECT {select_list} FROM {table} WHERE {col} LIKE '{value[0]}%'"

    if pattern == "equal":
        return f"SELECT {select_list} FROM {table} WHERE {col} = '{value}'"

    return f"SELECT {select_list} FROM {table} WHERE {col} LIKE '%{value[:3]}%'"


def generate_medium_sql():
    """
    Generates JOIN queries without aggregation.

    Skills introduced:
        - Basic JOIN
        - Optional filtering
        - ORDER BY / DISTINCT

    Still avoids GROUP BY to keep complexity moderate.
    """
    join = pick_join()
    if not join:
        return None

    t1, t2, col1, col2 = join

    total_cols = random.choice([1, 2])

    if total_cols == 1:
        table_choice = random.choice([t1, t2])
        select_list = build_select_list(
            table_choice,
            table_choice,
            allow_two_cols_prob=0.0
        )
    else:
        col_t1 = build_select_list(t1, t1, allow_two_cols_prob=0.0)
        col_t2 = build_select_list(t2, t2, allow_two_cols_prob=0.0)

        if not col_t1 or not col_t2:
            return None

        select_list = f"{col_t1}, {col_t2}"

    query = f"""
    SELECT {select_list}
    FROM {t1}
    JOIN {t2} ON {t1}.{col1} = {t2}.{col2}
    """

    pattern = random.choice([
        "simple_join",
        "where_t1",
        "where_t2",
        "double_where",
        "order_by",
        "distinct"
    ])

    if pattern == "where_t1":
        cond = generate_realistic_condition(t1, t1)
        if cond:
            query += f"\nWHERE {cond}"

    elif pattern == "where_t2":
        cond = generate_realistic_condition(t2, t2)
        if cond:
            query += f"\nWHERE {cond}"

    elif pattern == "double_where":
        cond1 = generate_realistic_condition(t1, t1)
        cond2 = generate_realistic_condition(t2, t2)
        if cond1 and cond2:
            query += f"\nWHERE {cond1} AND {cond2}"

    elif pattern == "order_by":
        first_col = select_list.split(",")[0].strip()
        direction = random.choice(["ASC", "DESC"])
        query += f"\nORDER BY {first_col} {direction}"

    elif pattern == "distinct":
        query = query.replace("SELECT", "SELECT DISTINCT")

    return query


def generate_hard_sql():
    """
   Generates JOIN + AGGREGATION queries.

   Skills introduced:
       - GROUP BY
       - HAVING
       - Aggregations (COUNT, SUM, AVG, MIN, MAX)

   These queries represent real analytical tasks.
   """
    agg = random.choices(
        ["COUNT", "AVG", "SUM", "MAX", "MIN"],
        weights=[40, 15, 15, 15, 15]
    )[0]

    join = pick_join()
    if not join or random.random() >= 0.8:
        return None

    t1, t2, col1, col2 = join
    a1, a2 = alias(t1), alias(t2)

    num_col = pick_numeric_column_safe(t1)
    if agg != "COUNT" and not num_col:
        return None

    agg_expr = "COUNT(*)" if agg == "COUNT" else f"{agg}({a1}.{num_col})"

    total_cols = random.choice([1, 2])

    if total_cols == 1:

        query = f"""
        SELECT {agg_expr}
        FROM {t1} {a1}
        JOIN {t2} {a2} ON {a1}.{col1} = {a2}.{col2}
        """

        if random.random() < 0.6:
            cond = generate_realistic_condition(t1, a1)
            if cond:
                query += f"\nWHERE {cond}"

        return query

    dimension_table = random.choice([t1, t2])
    dim_alias = a1 if dimension_table == t1 else a2

    dim_col = pick_any_column_safe(dimension_table)
    if not dim_col:
        return None

    query = f"""
    SELECT {dim_alias}.{dim_col}, {agg_expr}
    FROM {t1} {a1}
    JOIN {t2} {a2} ON {a1}.{col1} = {a2}.{col2}
    """

    if random.random() < 0.6:
        cond = generate_realistic_condition(t1, a1)
        if cond:
            query += f"\nWHERE {cond}"

    query += f"\nGROUP BY {dim_alias}.{dim_col}"

    if random.random() < 0.6:
        if agg == "COUNT":
            query += "\nHAVING COUNT(*) >= 1"
        else:
            query += f"\nHAVING {agg_expr} IS NOT NULL"

    if random.random() < 0.7:
        query += "\nORDER BY 2 DESC"

    # LIMIT disabled because gameplay validator forbids it
    pass

    return query


def generate_expert_sql():
    """
   Generates advanced SQL using subqueries.

   Skills introduced:
       - EXISTS / NOT EXISTS
       - Correlated subqueries
       - Comparisons against averages
       - Nested logic

   This is the highest difficulty level.
   """
    join = pick_join()
    if not join:
        return None

    t1, t2, col1, col2 = join
    a1, a2 = alias(t1), alias(t2)

    col_t1 = pick_any_column_safe(t1)
    if not col_t1:
        return None

    num_col_t2 = pick_numeric_column_safe(t2)

    pattern = random.choice(["EXISTS", "NOT_EXISTS", "COUNT_COMPARE", "ABOVE_AVG"])

    total_cols = random.choice([1, 2])

    select_cols = [f"{a1}.{col_t1}"]

    if total_cols == 2:
        second_col = pick_any_column_safe(t2)
        if second_col:
            select_cols.append(f"{a2}.{second_col}")

    use_join = random.random() < 0.8

    from_clause = f"FROM {t1} {a1}"
    if use_join:
        from_clause += f"\nJOIN {t2} {a2} ON {a1}.{col1} = {a2}.{col2}"

    query = f"SELECT {', '.join(select_cols)}\n{from_clause}\nWHERE "

    if pattern == "EXISTS":
        query += f"""
        EXISTS (
            SELECT 1
            FROM {t2} sub
            WHERE sub.{col2} = {a1}.{col1}
        )
        """

    elif pattern == "NOT_EXISTS":
        query += f"""
        NOT EXISTS (
            SELECT 1
            FROM {t2} sub
            WHERE sub.{col2} = {a1}.{col1}
        )
        """

    elif pattern == "COUNT_COMPARE":
        query += f"""
        (
            SELECT COUNT(*)
            FROM {t2} sub
            WHERE sub.{col2} = {a1}.{col1}
        ) >= 1
        """

    elif pattern == "ABOVE_AVG" and num_col_t2:
        query += f"""
        {a2}.{num_col_t2} > (
            SELECT AVG(sub.{num_col_t2})
            FROM {t2} sub
            WHERE sub.{col2} = {a1}.{col1}
        )
        """
    else:
        return None

    if random.random() < 0.4:
        cond = generate_realistic_condition(t1, a1)
        if cond:
            query += f"\nAND {cond}"

    if random.random() < 0.6:
        query += f"\nORDER BY 1"

    # LIMIT disabled because gameplay validator forbids it
    pass

    return query


def generate_ai_backstory_challenge(sql_query, previous_attempt=None, feedback=None):
    """
    Uses the LLM to transform SQL into an immersive narrative challenge.

    IMPORTANT:
    The AI NEVER sees the expected results.
    It only sees:
        - Database schema
        - SQL analysis metadata
        - Strict rules to avoid hallucinations

    If the AI output fails validation, we retry with feedback.
    This creates a self-correcting generation loop.
    """
    schema_text = format_schema_for_llm()

    parsed = QueryAnalyzer.parse(sql_query)

    analysis = {
        "has_join": QueryAnalyzer.has_join(parsed),
        "has_group_by": QueryAnalyzer.has_group_by(parsed),
        "has_subquery": QueryAnalyzer.has_subquery(parsed),
        "has_aggregation": any(
            QueryAnalyzer.has_aggregate(parsed, fn)
            for fn in ["avg", "count", "sum", "min", "max"]
        )
    }

    verbs = [
        "Busca", "Encuentra", "Localiza", "Extrae",
        "Identifica", "Recupera", "Obtén", "Analiza"
    ]
    verb = random.choice(verbs)

    if previous_attempt:
        correction_block = f"""
            PREVIOUS ATTEMPT (needs correction):
            {json.dumps(previous_attempt, indent=2, ensure_ascii=False)}
            
            FEEDBACK FROM VALIDATION:
            {feedback}
            
            IMPORTANT CORRECTION RULES:
            You MUST KEEP the original idea and meaning.
            You MUST ONLY fix the problems mentioned in the feedback.
            DO NOT rewrite the description from scratch.
            If the narrative is already good, keep it and only fix the title tone.
            """
    else:
        # When the AI fails validation, we send the previous output
        # and feedback so the model can iteratively fix mistakes.
        correction_block = ""

    prompt = f"""
        You are a SQL challenge designer for students.
        
        DATABASE SCHEMA:
        {schema_text}
        
        COLUMN TYPE GUIDE:
        {COLUMN_TYPE_GUIDE}
        
        SCHEMA SEMANTICS:
        {json.dumps(SCHEMA_SEMANTICS, indent=2)}
        
        You MUST use the database schema to understand the available attributes.
        If an attribute is not in the schema, DO NOT mention it.
        
        SQL ANALYSIS (STRICT TRUTH - YOU MUST FOLLOW):
        - Query uses multiple entities: {analysis["has_join"]}
        - Query uses aggregation: {analysis["has_aggregation"]}
        - Query uses grouping: {analysis["has_group_by"]}
        - Query uses subquery: {analysis["has_subquery"]}
        
        {correction_block}
        
        TASK:
        Describe the goal of the SQL query in natural language.
        
        CRITICAL RULES:
        - NEVER explain SQL or query structure
        - NEVER mention JOIN, GROUP BY, HAVING, subqueries
        - You MAY describe the type of data returned
        - NEVER mention column names explicitly
        - Must sound like a real student exercise
        - One sentence max
        - You MUST ONLY describe information that exists in the schema
        - NEVER invent attributes
        
        SIMPLICITY RULE (CRITICAL):
        If the query is simple (single table, no filters, no joins, no aggregation):
        The description MUST be simple and literal.
        
        Do NOT invent analysis, patterns, investigation or secrets.
        
        REALISM RULE:
        Do NOT exaggerate importance.
        Do NOT use words like confidential, secret, hidden, investigation,
        intelligence, surveillance unless SQL clearly implies it.
        
        STRICT CONSISTENCY RULES:
        If multiple entities is FALSE → no relationships.
        If aggregation is FALSE → no totals/averages.
        If grouping is FALSE → no categories.
        If subquery is FALSE → no comparisons vs averages.
        
        TITLE RULES:
        Title must be immersive and narrative.
        Title must NOT look like a database field.
        
        FORMAT (IMPORTANT) :
        - title in Spanish
        - description in Spanish starting with "{verb}"
        
        SQL QUERY:
        {sql_query}
        
        Return ONLY JSON:
        {{
          "title": "...",
          "description": "..."
        }}
    """

    # We force the model to output STRICT JSON.
    # clean_llm_json() later removes markdown/code fences if the model cheats.
    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0.5},
        messages=[
            {
                "role": "system",
                "content": GAME_WORLD_CONTEXT + """
                    You ONLY output valid JSON.
                    No explanations.
                    No markdown.
                    No extra text.
                """
            },
            {"role": "user", "content": prompt}
        ]
    )

    text = response["message"]["content"]

    try:
        clean_json = clean_llm_json(text)
        return json.loads(clean_json)
    except:
        print("💥 RESPUESTA IA INVALIDA:")
        print(text)
        return None


def generate_sql_by_difficulty(difficulty):
    """ Routes difficulty string to the correct SQL generator. """
    if difficulty == "VERY_EASY":
        return generate_very_easy_sql()
    if difficulty == "EASY":
        return generate_easy_sql()
    if difficulty == "MEDIUM":
        return generate_medium_sql()
    if difficulty == "HARD":
        return generate_hard_sql()
    if difficulty == "EXPERT":
        return generate_expert_sql()


def generate_valid_sql_with_rows(difficulty: str, max_tries: int = 15):
    """
    Generates SQL until it is:
    - Not duplicated
    - No type mismatch
    - No forbidden columns
    - Executable
    - Returns rows
    This stage DOES NOT involve the AI.
    """

    for attempt in range(max_tries):
        print(f"\n🛠️ SQL ATTEMPT {attempt+1}")

        sql = generate_sql_by_difficulty(difficulty)
        print("SQL candidate:", sql)

        if not sql:
            print("❌ Generator devolvió None")
            continue

        # validators that depend ONLY on SQL
        if is_duplicate_query(sql):
            print("❌ SQL duplicada")
            continue

        if has_type_mismatch(sql):
            print("❌ Type mismatch")
            continue

        if uses_forbidden_columns(sql):
            print("❌ Uses forbidden columns")
            continue

        if uses_forbidden_constructs(sql):
            print("❌ Uses forbidden constructs")
            continue

        result = execute_query_and_get_expected(sql)

        if result is None:
            print("❌ SQL no ejecutable")
            continue

        if len(result) == 0:
            print("❌ SQL sin filas")
            continue

        print(f"✅ SQL válida con {len(result)} filas")
        return sql, result

    return None, None


def generate_realistic_condition(table: str, alias: str | None = None):
    """
    Generates realistic WHERE conditions using real DB values.

    This prevents:
        - Impossible filters
        - Empty result sets
        - Unrealistic numeric thresholds
    """
    prefix = f"{alias}." if alias else ""
    column_type = random.choice(["numeric", "text"])

    if column_type == "numeric":
        col = pick_numeric_column_safe(table)
        if not col:
            return None

        range_vals = get_column_numeric_range(table, col)
        if not range_vals:
            return None

        min_val, max_val = range_vals
        op = random.choice([">", "<", ">=", "<=", "!="])
        value = random.randint(int(min_val), int(max_val))

        return f"{prefix}{col} {op} {value}"

    col = pick_text_column_safe(table)
    if not col:
        return None

    value = get_random_existing_value(table, col)
    if not value:
        return None

    mode = random.choice(["equal", "starts", "contains"])

    if mode == "equal":
        return f"{prefix}{col} = '{value}'"

    if mode == "starts":
        return f"{prefix}{col} LIKE '{value[0]}%'"

    return f"{prefix}{col} LIKE '%{value[:3]}%'"


def generate_and_store_challenge(
        db,
        chapter_id: int,
        difficulty: str,
        current_user
):
    """
    Challenge generation entrypoint.

    Pipeline overview:
    ------------------------------------------------
    1) Generate VALID SQL (no AI)
    2) Generate narrative using LLM
    3) Validate narrative immersion
    4) Generate progressive hints
    5) Persist challenge in system DB

    The pipeline retries AI generation up to 5 times if needed.
    If AI repeatedly fails → challenge is discarded.
    """
    ChapterService.get_owned_chapter(
        db,
        chapter_id,
        current_user
    )

    valid_difficulties = DIFFICULTY_TO_VALUE

    if difficulty not in valid_difficulties:
        raise ValueError(f"Invalid difficulty: {difficulty}")

    # ─────────────────────────────────────────────
    # Generate valid SQL
    # ─────────────────────────────────────────────
    print("\nGENERANDO SQL VÁLIDA...")

    generated_sql, result = generate_valid_sql_with_rows(difficulty)

    if not generated_sql:
        print("No se pudo generar SQL válida")
        return {"error": "SQL generation failed"}

    print("\nSQL FINAL ELEGIDA:")
    print(generated_sql)
    print(f"Filas devueltas: {len(result)}")

    # ─────────────────────────────────────────────
    # Generate backstory with IA
    # ─────────────────────────────────────────────
    previous_attempt = None
    feedback = "El título debe ser narrativo e inmersivo."

    for attempt in range(5):
        print(f"\n===== IA INTENTO {attempt + 1} =====")
        print("FEEDBACK IA:", feedback if feedback else "Sin feedback")

        challenge = generate_ai_backstory_challenge(
            generated_sql,
            previous_attempt,
            feedback
        )

        if not challenge:
            print("IA no devolvió JSON válido")
            continue

        print("\nRESPUESTA IA:")
        print(json.dumps(challenge, indent=2, ensure_ascii=False))

        # ───────── Backstory Validation ─────────

        if title_not_immersive(challenge["title"]):
            previous_attempt = challenge
            print("Título rompe inmersión")
            feedback = "El título debe ser narrativo e inmersivo."
            continue

        print("Narrativa aceptada")

        # ─────────────────────────────────────────────
        # Hint generation with IA + save challenge
        # ─────────────────────────────────────────────
        hints = generate_hints(generated_sql, challenge["description"])

        print("Hints generados:")
        for h in hints:
            print("-", h)

        save_challenge_to_db(
            chapter_id,
            {
                "title": challenge["title"],
                "description": challenge["description"],
                "sql_query": generated_sql
            },
            result,
            hints,
            difficulty
        )

        print("RETO GUARDADO EN BD")
        return {"status": "challenge created"}

    # ─────────────────────────────────────────────
    # IA fails after 5 attempts
    # ─────────────────────────────────────────────
    print("\nLa IA falló tras 5 intentos")
    return {"error": "AI failed after 5 attempts"}
