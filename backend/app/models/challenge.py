from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class Challenge(Base):
    __tablename__ = "Challenge"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Chapter_id: Mapped[int] = mapped_column(ForeignKey("Chapter.Id"))
    Title: Mapped[str] = mapped_column(String, nullable=False)
    Description: Mapped[str] = mapped_column(Text, nullable=False)
    Difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    Expected_query: Mapped[str] = mapped_column(Text, nullable=False)
    Max_score: Mapped[int] = mapped_column(Integer)
