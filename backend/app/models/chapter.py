from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Chapter(Base):
    __tablename__ = "Chapter"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str] = mapped_column(String, nullable=False)
    Description: Mapped[str] = mapped_column(Text, nullable=False)
