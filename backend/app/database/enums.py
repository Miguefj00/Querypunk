import enum


# Difficulty levels shared across challenges, chapters and analytics.
class DifficultyEnum(str, enum.Enum):
    VERY_EASY = "VERY_EASY"
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"
