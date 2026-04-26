from typing import Optional, Dict, Any
from sqlalchemy import String, Text, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base
from app.database.enums import DifficultyEnum


class Challenge(Base):
    """Represents SQL game challenges"""
    __tablename__ = "Challenge"

    id: Mapped[int] = mapped_column(primary_key=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("Chapter.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    expected_result: Mapped[list] = mapped_column(JSON, nullable=True)
    validation_rules: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    generated_by_system: Mapped[bool] = mapped_column(Boolean, default=False)

    difficulty: Mapped[DifficultyEnum] = mapped_column(
        Enum(DifficultyEnum),
        nullable=True
    )
