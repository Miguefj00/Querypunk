import re


def clean_llm_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("No se encontró JSON en la respuesta del modelo")

    json_text = match.group()

    json_text = json_text.replace("\n", " ")

    json_text = json_text.replace("\t", " ")

    json_text = json_text.replace("“", '"').replace("”", '"')

    return json_text
