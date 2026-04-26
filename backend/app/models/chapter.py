from sqlalchemy import String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
from app.database.enums import DifficultyEnum


class Chapter(Base):
    """Represents an entire chapter that contains the game challenges"""
    __tablename__ = "Chapter"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

    difficulty: Mapped[DifficultyEnum] = mapped_column(
        Enum(DifficultyEnum),
        nullable=True
    )
