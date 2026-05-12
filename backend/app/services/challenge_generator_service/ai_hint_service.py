import json
import ollama

from app.services.challenge_generator_service.schema_structured_service import format_schema_for_llm
from app.utils.ai_utils import clean_llm_json, HINT_SYSTEM_CONTEXT
from app.utils.query_analizer import QueryAnalyzer

MODEL = "llama3"

"""
AI Hint Generator

Generates 3 progressive hints that guide the student's reasoning
WITHOUT revealing the SQL solution.

Hints focus on:
    - How to think about the data
    - What type of operations are needed
    - Increasing specificity

Hints must NEVER mention:
    - Table names
    - Column names
    - SQL keywords
"""


def generate_hints(sql_query: str, description: str):
    """
    Generates 3 progressive conceptual hints using local AI (Ollama).
    Hints must guide the thinking process WITHOUT revealing the SQL solution.
    """

    schema_text = format_schema_for_llm()[:6000]

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

    prompt = f"""
        You must generate hints for a SQL challenge in a cyberpunk game.
        
        DATABASE SCHEMA:
        {schema_text}
        
        CHALLENGE DESCRIPTION:
        {description}
        
        INTERNAL SOLUTION CONTEXT (DO NOT REVEAL OR EXPLAIN):
        {sql_query}
        
        SQL ANALYSIS (STRICT TRUTH - YOU MUST FOLLOW):
        - Query uses multiple entities: {analysis["has_join"]}
        - Query uses aggregation: {analysis["has_aggregation"]}
        - Query uses grouping: {analysis["has_group_by"]}
        - Query uses subquery: {analysis["has_subquery"]}
        
        PROBLEM SCOPE LOCK (VERY IMPORTANT):

        Hints must ONLY refer to the task described in the challenge description.
        Do NOT expand the scenario.
        Do NOT introduce new concepts, actors, locations or entities.
        Do NOT speculate about additional data.
        Do NOT suggest extra information that is not required.
        
        Hints must stay strictly inside the scope of the task.
        If the task only asks to display a single attribute → hints must reflect a simple task.
        If the task does not mention filtering → hints must not suggest filtering.
        
        CRITICAL:
        You MUST NOT contradict this analysis in the hints.
        If "multiple entities" is false → NEVER mention combining or relating data.
        If "aggregation" is false → NEVER mention calculations or totals.
        If "grouping" is false → NEVER mention grouping or categories.
        If "subquery" is false → NEVER mention comparisons against averages or nested logic.
                
        IMPORTANT RULES FOR HINTS:
        - Respond in Spanish
        - NEVER explain or reference the SQL solution
        - NEVER mention table names
        - NEVER mention column names
        - NEVER mention SQL keywords (SELECT, JOIN, WHERE, GROUP BY, etc)
        - NEVER describe the steps of the query
        - NEVER reveal the answer
        - Focus on HOW TO THINK, not WHAT TO TYPE
        Hints must guide DATA THINKING:
        - what kind of information is needed
        - whether filtering is needed
        - whether combining data is needed
        - whether aggregation is needed
        
        Hints should reflect the complexity of the task.
        VERY EASY tasks must produce simple hints.
        Do not overcomplicate simple challenges.
        
        GOOD HINT EXAMPLE:
        "Piensa qué entidad del sistema almacena esta información."
        "Necesitas mostrar atributos descriptivos de esa entidad."
        "No necesitas aplicar filtros ni cálculos."
        
        BAD HINT EXAMPLE:
        "Debes seleccionar columnas de la tabla Species"
        "Haz un SELECT Name FROM..."
        "Usa un JOIN entre..."
        
        Generate EXACTLY 3 hints:
        - Each hint must be one short sentence
        - Progressive difficulty (general → specific)
        - No numbering
        - Output ONLY valid JSON
        
        JSON FORMAT:
        {{
          "hints": ["hint","hint","hint"]
        }}
    """

    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0.2},
        messages=[
            {
                "role": "system",
                "content": HINT_SYSTEM_CONTEXT + "\nYou ONLY output valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]
    clean_json = clean_llm_json(text)
    return json.loads(clean_json)["hints"]
