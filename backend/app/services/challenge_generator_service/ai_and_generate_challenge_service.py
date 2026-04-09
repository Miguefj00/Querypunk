import ollama
import json

import random

from app.services.challenge_generator_service.ai_hint_service import generate_hints
from app.services.challenge_generator_service.generation_helpers import random_where_clause
from app.services.challenge_generator_service.sql_randomizer import pick_table, pick_column, pick_join
from app.services.challenge_generator_service.validate_challenge_quality import is_duplicate_query, validate_language, \
    uses_forbidden_columns
from app.utils.ai_utils import clean_llm_json
from dotenv import load_dotenv

from app.services.challenge_generator_service.game_db_executor import (execute_query_and_get_expected,
                                                                       save_challenge_to_db)
from app.utils.difficulty_utils import DIFFICULTY_TO_VALUE

load_dotenv()

MODEL = "llama3"


def generate_very_easy_sql():
    table = pick_table()

    if random.random() < 0.5:
        col = pick_column(table, allow_ids=False)
        return f"SELECT {col} FROM {table}"

    col1 = pick_column(table, allow_ids=False)
    col2 = pick_column(table, allow_ids=False)

    return f"""
    SELECT {col1}, {col2}
    FROM {table}
    """


def generate_easy_sql():
    table = pick_table()

    mode = random.choice(["numeric", "text"])

    # ───────── NUMERIC ─────────
    if mode == "numeric":
        col1 = pick_column(table, numeric_only=True, allow_ids=False)

        if random.random() < 0.6:
            number = random.randint(1, 10)
            op = random.choice([">", "<"])
            return f"""
            SELECT {col1}
            FROM {table}
            WHERE {col1} {op} {number}
            """

        col2 = pick_column(table, numeric_only=True, allow_ids=False)
        n1, n2 = random.randint(1, 10), random.randint(1, 10)
        logic = random.choice(["AND", "OR"])

        return f"""
        SELECT {col1}
        FROM {table}
        WHERE {col1} > {n1} {logic} {col2} < {n2}
        """

    # ───────── TEXT ─────────
    col = pick_column(table, text_only=True, allow_ids=False)
    letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    return f"""
    SELECT {col}
    FROM {table}
    WHERE {col} LIKE '{letter}%'
    """


def generate_medium_sql():
    join = pick_join()
    if not join:
        return generate_easy_sql()

    t1, t2, col1, col2 = join

    c1 = pick_column(t1, allow_ids=False)
    c2 = pick_column(t2, allow_ids=False)

    base_query = f"""
    SELECT {t1}.{c1}, {t2}.{c2}
    FROM {t1}
    JOIN {t2} ON {t1}.{col1} = {t2}.{col2}
    """

    # 🔥 70% probabilidad de WHERE
    if random.random() < 0.7:
        if random.random() < 0.5:
            condition = random_where_clause(t1, t1)
        else:
            condition = random_where_clause(t2, t2)

        base_query += f"\nWHERE {condition}"

    return base_query


def generate_hard_sql():
    agg = random.choice(["COUNT", "AVG", "SUM", "MAX", "MIN"])
    join = pick_join()

    if join and random.random() < 0.8:
        t1, t2, col1, col2 = join
        group_col = pick_column(t1, allow_ids=False)

        if agg == "COUNT":
            agg_expr = "COUNT(*)"
        else:
            num_col = pick_column(t1, numeric_only=True, allow_ids=False)
            agg_expr = f"{agg}({t1}.{num_col})"

        query = f"""
        SELECT {t1}.{group_col}, {agg_expr}
        FROM {t1}
        JOIN {t2} ON {t1}.{col1} = {t2}.{col2}
        """

        if random.random() < 0.7:
            condition = random_where_clause(t1, t1)
            query += f"\nWHERE {condition}"

        query += f"\nGROUP BY {t1}.{group_col}"

        if random.random() < 0.6:
            query += f"\nHAVING {agg_expr} > 1"

        return query

    table = pick_table()
    group_col = pick_column(table, allow_ids=False)

    if agg == "COUNT":
        agg_expr = "COUNT(*)"
    else:
        num_col = pick_column(table, numeric_only=True, allow_ids=False)
        agg_expr = f"{agg}({num_col})"

    query = f"""
    SELECT {group_col}, {agg_expr}
    FROM {table}
    """

    if random.random() < 0.7:
        query += f"\nWHERE {random_where_clause(table)}"

    query += f"\nGROUP BY {group_col}\nHAVING {agg_expr} > 1"

    return query


def generate_expert_sql():
    join = pick_join()

    if join and random.random() < 0.7:
        t1, t2, col1, col2 = join

        num_col = pick_column(t1, numeric_only=True, allow_ids=False)
        select_col = pick_column(t1, allow_ids=False)

        query = f"""
        SELECT {t1}.{select_col}
        FROM {t1}
        JOIN {t2} ON {t1}.{col1} = {t2}.{col2}
        WHERE {t1}.{num_col} > (
            SELECT AVG({num_col}) FROM {t1}
        )
        """

        if random.random() < 0.7:
            extra = random_where_clause(t1, t1)
            query += f"\nAND {extra}"

        return query

    table = pick_table()
    num_col = pick_column(table, numeric_only=True, allow_ids=False)
    select_col = pick_column(table, allow_ids=False)

    query = f"""
    SELECT {select_col}
    FROM {table}
    WHERE {num_col} > (
        SELECT AVG({num_col}) FROM {table}
    )
    """

    if random.random() < 0.7:
        query += f"\nAND {random_where_clause(table)}"

    return query


def generate_ai_backstory_challenge(sql_query: str):

    verbs = [
        "Busca",
        "Encuentra",
        "Localiza",
        "Extrae",
        "Identifica",
        "Recupera",
        "Obtén",
        "Analiza"
    ]

    verb = random.choice(verbs)

    prompt = f"""
        Eres diseñador de retos SQL.
        
        Debes describir la tarea SIN explicar cómo escribir la query.
        
        REGLAS CRÍTICAS:
        - NO inventes columnas ni conceptos.
        - NO expliques la estructura de la query.
        - NO menciones JOIN, GROUP BY, HAVING o subqueries.
        - NO describas columnas paso a paso.
        - Describe el objetivo del reto en lenguaje natural.
        - Debe explicar QUÉ datos se buscan, no CÓMO obtenerlos.
        - Debe sonar como un ejercicio real para estudiantes.
        - Máximo 1 frase.
        
        Formato:
        - title en inglés
        - description en español empezando por "{verb}"
        
        SQL:
        {sql_query}
        
        Devuelve JSON:
        {{
          "title": "...",
          "description": "..."
        }}
    """

    response = ollama.chat(
        model=MODEL,
        options={
            "temperature": 0.7,
        },
        messages=[
            {
                "role": "system",
                "content": """
                You ONLY output valid JSON.
                No explanations.
                No markdown.
                No extra text.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]

    try:
        clean_json = clean_llm_json(text)
        return json.loads(clean_json)
    except Exception as e:
        print("💥 RESPUESTA IA INVALIDA:")
        print(text)
        return None


def generate_sql_by_difficulty(difficulty):
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


def generate_and_store_challenge(chapter:int, difficulty:str):
    valid_difficulties = DIFFICULTY_TO_VALUE

    if difficulty not in valid_difficulties:
        raise ValueError(f"Invalid difficulty: {difficulty}")

    feedback = ""

    for attempt in range(5):
        print(f"\n\n🤖 ===== INTENTO {attempt+1} =====")
        print("📝 FEEDBACK ENVIADO AL MODELO:")
        print(feedback if feedback else "Sin feedback")

        generated_sql = generate_sql_by_difficulty(difficulty)
        challenge = generate_ai_backstory_challenge(generated_sql)
        sql = generated_sql

        if not challenge:
            print("❌ IA no devolvió JSON válido")
            continue

        print("\n🧠 RESPUESTA IA:")
        print(json.dumps(challenge, indent=2, ensure_ascii=False))
        print("\n💾 SQL GENERADA:")
        print(sql)

        if is_duplicate_query(sql):
            print("❌ RECHAZADO: query duplicada")
            feedback = "Tu SQL es duplicada. Debes usar tablas y estructura completamente diferente."
            continue

        if uses_forbidden_columns(sql):
            print("❌ RECHAZADO: uso de columnas ID (anti-gameplay)")
            feedback = "No uses columnas ID o *_id. Debes usar columnas con significado real."
            continue

        if not validate_language(challenge):
            print("❌ RECHAZADO: idioma incorrecto")
            feedback = "Has mezclado idiomas. Title inglés y description español obligatorios."
            continue

        print("\n✅ RETO ACEPTADO POR VALIDADORES")

        result = execute_query_and_get_expected(sql)

        if result is None:
            print("❌ ERROR: la SQL no se pudo ejecutar en la game DB")
            feedback = "La query no se pudo ejecutar en la base de datos real. Debe devolver filas reales."
            continue

        if len(result) == 0:
            print("❌ ERROR: la SQL no devuelve filas")
            feedback = "La query no devuelve resultados reales. Debe devolver filas existentes."
            continue

        print(f"📊 Filas devueltas: {len(result)}")

        hints = generate_hints(sql, challenge["description"])

        print("💡 Hints generados:")
        for h in hints:
            print("-", h)

        save_challenge_to_db(
            chapter,
            {
                "title": challenge["title"],
                "description": challenge["description"],
                "sql_query": generated_sql
            },
            result,
            hints,
            difficulty
        )

        print("💾 RETO GUARDADO EN BD")

        return {"status": "challenge created"}

    print("\n💥 La IA falló tras 5 intentos")
    return {"error": "AI failed after 5 attempts"}