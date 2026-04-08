import ollama
import json

import random

from app.services.ai_service.ai_hint_service import generate_hints
from app.services.ai_service.sql_randomizer import pick_table, pick_column, pick_join
from app.services.ai_service.validate_challenge_quality import is_duplicate_query, validate_language, \
    uses_forbidden_columns
from app.utils.ai_utils import clean_llm_json
from dotenv import load_dotenv

from app.services.ai_service.game_db_executor import execute_query_and_get_expected, save_challenge_to_db

load_dotenv()

MODEL = "llama3"


def generate_very_easy_sql():
    table = pick_table()
    column = pick_column(table, allow_ids=False)

    return f"SELECT {column} FROM {table}"


def generate_easy_sql():
    table = pick_table()

    mode = random.choice(["numeric", "text"])

    # =========================
    # NUMERIC FILTER
    # =========================
    if mode == "numeric":
        column = pick_column(table, numeric_only=True, allow_ids=False)

        op = random.choice([">", "<"])
        number = random.randint(1, 10)

        return f"""
        SELECT {column}
        FROM {table}
        WHERE {column} {op} {number}
        """

    # =========================
    # TEXT FILTER
    # =========================
    else:
        column = pick_column(table, text_only=True, allow_ids=False)

        letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        return f"""
        SELECT {column}
        FROM {table}
        WHERE {column} LIKE '{letter}%'
        """


def generate_medium_sql():
    join = pick_join()
    if not join:
        return generate_very_easy_sql()

    t1, t2, col1, col2 = join

    c1 = pick_column(t1, allow_ids=False)
    c2 = pick_column(t2, allow_ids=False)

    return f"""
    SELECT {t1}.{c1}, {t2}.{c2}
    FROM {t1}
    JOIN {t2} ON {t1}.{col1} = {t2}.{col2}
    """


def generate_hard_sql():
    import random

    agg = random.choice(["COUNT", "AVG", "SUM", "MAX", "MIN"])

    join = pick_join()

    if join and random.random() < 0.5:
        t1, t2, col1, col2 = join

        group_col = pick_column(t1, allow_ids=False)

        if agg == "COUNT":
            agg_expr = "COUNT(*)"
        else:
            numeric_col = pick_column(t1, numeric_only=True, allow_ids=False)
            agg_expr = f"{agg}({t1}.{numeric_col})"

        return f"""
        SELECT {t1}.{group_col}, {agg_expr}
        FROM {t1}
        JOIN {t2} ON {t1}.{col1} = {t2}.{col2}
        GROUP BY {t1}.{group_col}
        """

    table = pick_table()
    group_col = pick_column(table, allow_ids=False)

    if agg == "COUNT":
        agg_expr = "COUNT(*)"
    else:
        numeric_col = pick_column(table, numeric_only=True, allow_ids=False)
        agg_expr = f"{agg}({numeric_col})"

    return f"""
    SELECT {group_col}, {agg_expr}
    FROM {table}
    GROUP BY {group_col}
    """


def generate_expert_sql():
    import random

    table = pick_table()
    numeric_col = pick_column(table, numeric_only=True, allow_ids=False)
    select_col = pick_column(table, allow_ids=False)

    operator = random.choice([">", "<"])

    return f"""
    SELECT {select_col}
    FROM {table}
    WHERE {numeric_col} {operator} (
        SELECT AVG({numeric_col}) FROM {table}
    )
    """


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
        
        Debes describir la query de forma LITERAL y EXACTA.
        
        REGLAS CRÍTICAS:
        - NO inventes columnas ni conceptos.
        - SOLO puedes mencionar columnas que aparecen en la query.
        - Si la query usa GROUP BY → debes mencionarlo.
        - Si la query usa JOIN → debes mencionarlo.
        - Si la query usa AVG/SUM/MIN/MAX/COUNT → debes mencionarlo.
        - Describe exactamente qué columnas se seleccionan y de qué tabla vienen.
        - No añadas narrativa extra.
        - No expliques el contexto del juego.
        - No interpretes el significado de las columnas.
        
        Formato:
        - title en inglés
        - description en español empezando por "{verb}"
        
        SQL:
        {sql_query}
        
        Devuelve JSON:
        {{
          "title": "...",
          "description": "...",
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