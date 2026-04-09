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
        
        RESPONDE EN ESPAÑOL.
        
        REGLAS IMPORTANTES:
        - NO numeres las pistas
        - NO escribas "Pista 1", "Pista 2", etc.
        - Cada pista debe ser solo una frase corta
        - Las pistas deben ir de general a específica
        
        RETO:
        {description}
        
        SOLUCION:
        {sql_query}
        
        Responde SOLO en JSON válido:
        {{
          "hints": ["pista","pista","pista"]
        }}
        """

    response = ollama.chat(
        model=MODEL,
        options={
            "temperature": 0.6,
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
