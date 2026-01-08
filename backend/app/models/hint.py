from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class Hint(Base):
    __tablename__ = "Hint"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.Id"))
    Hint_number: Mapped[int] = mapped_column(Integer, nullable=False)
    Unlock_attempt: Mapped[int] = mapped_column(Integer, nullable=False)
    Content: Mapped[str] = mapped_column(Text, nullable=False)
