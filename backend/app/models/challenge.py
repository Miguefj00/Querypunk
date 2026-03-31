from typing import Optional, Dict, Any
from sqlalchemy import String, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Challenge(Base):
    __tablename__ = "Challenge"

    id: Mapped[int] = mapped_column(primary_key=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("Chapter.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    validation_rules: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    generated_by_ai: Mapped[bool] = mapped_column(Boolean, default=False)