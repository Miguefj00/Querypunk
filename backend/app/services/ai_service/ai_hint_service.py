import json
import ollama

from app.utils.ai_utils import clean_llm_json

MODEL = "llama3"


def generate_hints(sql_query: str, description: str):
    """
    Genera 3 pistas progresivas usando IA local (Ollama)
    """

    prompt = f"""
        Genera EXACTAMENTE 3 pistas progresivas para resolver este reto SQL.
        
        RETO:
        {description}
        
        SOLUCION:
        {sql_query}
        
        Responde SOLO en JSON válido:
        {{
          "hints": ["pista 1","pista 2","pista 3"]
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
    clean_json = clean_llm_json(text)
    return json.loads(clean_json)["hints"]
