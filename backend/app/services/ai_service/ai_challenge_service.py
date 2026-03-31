import ollama
import json

from app.services.ai_service.ai_hint_service import generate_hints
from app.services.ai_service.ai_schema_service import get_database_schema
from app.utils.ai_utils import clean_llm_json
from dotenv import load_dotenv

from app.services.ai_service.game_db_executor import execute_query_and_get_expected, save_challenge_to_db

load_dotenv()

MODEL = "llama3"


def difficulty_from_chapter(chapter:int):
    if chapter <= 10:
        return "very easy SQL (SELECT simple)"
    elif chapter <= 20:
        return "easy SQL (WHERE)"
    elif chapter <= 30:
        return "medium SQL (JOIN)"
    elif chapter <= 40:
        return "advanced SQL (GROUP BY)"
    else:
        return "expert SQL (SUBQUERY)"


def generate_ai_sql_challenge(chapter:int):

    schema = get_database_schema()
    difficulty = difficulty_from_chapter(chapter)

    prompt = f"""
        You design SQL challenges for a cyberpunk videogame.
        
        DATABASE SCHEMA (USE EXACT NAMES):
        {schema}
        
        CRITICAL RULES:
        - Use ONLY table names and column names from the schema above
        - NEVER invent tables
        - NEVER invent columns
        - SQL must run in SQLite
        - Only SELECT queries allowed
        - No INSERT UPDATE DELETE
        - No markdown
        - Output ONLY JSON
        
        Generate one SQL challenge for chapter {chapter}.
        Difficulty: {difficulty}
        
        JSON FORMAT:
        {{
        "title": "short title",
        "description": "player mission description",
        "sql_query": "valid SQLite SELECT query"
        }}
        """

    response = ollama.chat(
        model=MODEL,
        options={
            "temperature": 0,
        },
        messages=[
            {
                "role": "system",
                "content": """
                    You are a JSON generator.
                    You ONLY output valid JSON.
                    You NEVER output explanations.
                    You NEVER output markdown.
                    You NEVER output text before or after JSON.
                    If you break the rules you fail.
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
    except:
        print("\n💥 RESPUESTA REAL DE OLLAMA:\n")
        print(text)
        raise

    try:
        return json.loads(clean_json)
    except Exception as e:
        print("❌ JSON inválido generado por IA:")
        print(clean_json)
        raise e


def generate_and_store_challenge(chapter:int):

    for attempt in range(3):
        print(f"\n🔁 Intento IA #{attempt+1}")

        challenge = generate_ai_sql_challenge(chapter)

        print("\n🧠 SQL generado:")
        print(challenge["sql_query"])

        result = execute_query_and_get_expected(challenge["sql_query"])

        if result is not None:
            print("✅ Query válida!")

            hints = generate_hints(
                challenge["sql_query"],
                challenge["description"]
            )

            save_challenge_to_db(chapter, challenge, result, hints)
            return {"status":"challenge created"}

        print("❌ Query inválida, reintentando...")

    return {"error":"AI failed after 3 attempts"}
