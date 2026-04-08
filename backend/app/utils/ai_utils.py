import json
import re


def _escape_control_chars_in_strings(json_text: str) -> str:
    def replacer(match):
        content = match.group(0)

        content = content.replace("\n", "\\n")
        content = content.replace("\r", "\\r")
        content = content.replace("\t", "\\t")

        return content

    return re.sub(r'".*?"', replacer, json_text, flags=re.DOTALL)


def clean_llm_json(text: str) -> str:
    start = text.find("{")
    if start == -1:
        raise ValueError("No se encontró JSON en la respuesta del modelo")

    json_text = text[start:]

    open_braces = json_text.count("{")
    close_braces = json_text.count("}")

    if open_braces > close_braces:
        json_text += "}" * (open_braces - close_braces)

    last_brace = json_text.rfind("}")
    json_text = json_text[: last_brace + 1]

    json_text = _escape_control_chars_in_strings(json_text)

    try:
        json.loads(json_text)
        return json_text
    except Exception:
        print("\n💥 RESPUESTA ORIGINAL DEL MODELO:\n")
        print(text)
        print("\n💥 JSON TRAS LIMPIEZA FINAL:\n")
        print(json_text)
        raise ValueError("No se pudo reparar el JSON del modelo")

