import json
import re

"""
Utilities and prompt context used by the AI challenge generator.

This module provides:
- Global world-building context for SQL challenge generation
- Semantic schema descriptions for LLM prompts
- JSON cleaning utilities for repairing imperfect model outputs
"""


# Global world context injected into every LLM call.
GAME_WORLD_CONTEXT = """
    You are designing SQL challenges for a CYBERPUNK game database.
    
    This is NOT a real-world database.
    
    WORLD RULES:
    - Species = humanoid races (Human, Cyborg, Android, GenMod, Synthetic)
    - Security incidents = corporate or physical incidents in futuristic HQs
    - Personnel = employees/agents working in districts and corporations
    - Districts, Sectors and Corporations belong to a futuristic city
    
    NEVER use real-world interpretations like:
    animals, wildlife, biology, IT security, SQL security.
    
    Everything must sound like part of a cyberpunk city world.
"""

# Hints context for AI generation
HINT_SYSTEM_CONTEXT = """
    You are a SQL teacher helping students think about problems.
    
    Your job is to guide reasoning, not storytelling.
    
    Hints must be:
    - Educational
    - Clear
    - Grounded in data analysis thinking
    - Not narrative or immersive
    
    Avoid roleplay or cyberpunk storytelling.
"""

# Human-readable explanation of semantic column types used by the LLM
COLUMN_TYPE_GUIDE = """
    COLUMN SEMANTIC TYPES:
    
    text → names, titles, descriptions (used for display or text filtering)
    numeric → quantities, money, counts, population (used for comparisons and aggregations)
    categorical → levels, categories, status values (used for grouping or filtering)
    boolean → true/false flags (used for yes/no filtering only)
    date → time related information (used for ordering or filtering by time)
    foreign_key → relationships between entities (used for combining data)
"""

# Semantic description of the game database used to guide AI challenge generation.
SCHEMA_SEMANTICS = {
    "Corporation": {
        "description": "Mega-corporations that control most economic and political power in the city.",
        "columns": {
            "Name": {"description": "Official name of the corporation.", "type": "text"},
            "Founded_year": {"description": "Year the corporation was established.", "type": "number"},
            "Ceo_name": {"description": "Name of the current CEO leading the corporation.", "type": "text"},
            "Net_worth": {"description": "Estimated total corporate value in credits.", "type": "number"},
            "Influence_level": {"description": "Relative political and social influence of the corporation.", "type": "number"}
        }
    },

    "Corporation_sector": {
        "description": "Relationship between corporations and the sectors they operate in.",
        "columns": {
            "Corporation_id": {"description": "Corporation operating in the sector.", "type": "fk"},
            "Sector_id": {"description": "Sector in which the corporation is active.", "type": "fk"}
        }
    },

    "Data_leak": {
        "description": "Confidential corporate data breaches and leaked information.",
        "columns": {
            "Corporation_id": {"description": "Corporation affected by the leak.", "type": "fk"},
            "Title": {"description": "Short title describing the leak.", "type": "text"},
            "Confidentiality_lvl": {"description": "Sensitivity level of the leaked information.", "type": "number"},
            "Content": {"description": "Summary of the leaked data.", "type": "text"},
            "Date": {"description": "Date when the leak became public.", "type": "date"}
        }
    },

    "District": {
        "description": "City districts with unique demographics and risk levels.",
        "columns": {
            "Name": {"description": "District name.", "type": "text"},
            "Population": {"description": "Number of residents living in the district.", "type": "number"},
            "Description": {"description": "Narrative description of the district.", "type": "text"},
            "Danger_lvl": {"description": "Security and crime risk rating of the district.", "type": "number"}
        }
    },

    "Headquarter": {
        "description": "Corporate headquarters buildings located across the city.",
        "columns": {
            "Corporation_id": {"description": "Corporation that owns the headquarters.", "type": "fk"},
            "District_id": {"description": "District where the headquarters is located.", "type": "fk"},
            "Main": {"description": "Indicates whether the building is the corporation primary headquarters.", "type": "boolean"},
            "Security_lvl": {"description": "Security rating of the building.", "type": "number"},
            "Employees": {"description": "Number of employees working in the building.", "type": "number"}
        }
    },

    "Implant": {
        "description": "Cybernetic implants available in the market.",
        "columns": {
            "Name": {"description": "Commercial name of the implant.", "type": "text"},
            "Manufacturer": {"description": "Company producing the implant.", "type": "text"},
            "Legality": {"description": "Legal status of the implant.", "type": "boolean"},
            "Power_consumption": {"description": "Energy required to operate the implant.", "type": "number"},
            "Type": {"description": "Category of implant (combat, medical, neural…).", "type": "text"}
        }
    },

    "Personnel_implant": {
        "description": "Cybernetic implants installed in employees.",
        "columns": {
            "Install_date": {"description": "Date when the implant was installed.", "type": "date"},
            "Personnel_id": {"description": "Employee receiving the implant.", "type": "fk"},
            "Implant_id": {"description": "Installed implant.", "type": "fk"}
        }
    },

    "Sector": {
        "description": "Corporate divisions dedicated to specific business activities.",
        "columns": {
            "Budget": {"description": "Financial resources assigned to the sector.", "type": "number"},
            "Director": {"description": "Person responsible for the sector.", "type": "text"},
            "Sector_type_id": {"description": "Type of activity the sector focuses on.", "type": "fk"}
        }
    },

    "Sector_type": {
        "description": "Categories describing different industry sectors.",
        "columns": {
            "Name": {"description": "Name of the sector category.", "type": "text"},
            "Description": {"description": "Explanation of the sector activities.", "type": "text"}
        }
    },

    "Security_incident": {
        "description": "Security breaches and incidents occurring in corporate headquarters.",
        "columns": {
            "Headquarter_id": {"description": "Headquarters where the incident occurred.", "type": "fk"},
            "Severity": {"description": "Seriousness level of the incident.", "type": "number"},
            "Description": {"description": "Summary of the incident.", "type": "text"},
            "Date": {"description": "Date when the incident occurred.", "type": "date"}
        }
    },

    "Species": {
        "description": "Humanoid species coexisting in the cyberpunk city.",
        "columns": {
            "Name": {"description": "Name of the species.", "type": "text"},
            "Description": {"description": "Short explanation of the species characteristics.", "type": "text"}
        }
    },

    "Personnel": {
        "description": "Employees working for corporations across the city.",
        "columns": {
            "First_name": {"description": "Employee first name.", "type": "text"},
            "Last_name": {"description": "Employee last name.", "type": "text"},
            "Salary": {"description": "Annual salary of the employee.", "type": "number"},
            "Corporation_id": {"description": "Corporation employing the person.", "type": "fk"},
            "Species_id": {"description": "Species of the employee.", "type": "fk"},
            "District_id": {"description": "District where the employee works.", "type": "fk"}
        }
    }
}


def _escape_control_chars_in_strings(json_text: str) -> str:
    """ Escapes control characters inside JSON string literals. """
    def replacer(match):
        content = match.group(0)

        content = content.replace("\n", "\\n")
        content = content.replace("\r", "\\r")
        content = content.replace("\t", "\\t")

        return content

    return re.sub(r'".*?"', replacer, json_text, flags=re.DOTALL)


def clean_llm_json(text: str) -> str:
    """
    Repairs malformed JSON responses produced by LLMs.

    Fixes common issues such as:
    - Missing closing braces
    - Control characters inside strings
    - Extra text before JSON block

    Raises an error if the JSON cannot be repaired.
    """
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

