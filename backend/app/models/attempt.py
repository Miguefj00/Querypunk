from sqlalchemy import Boolean, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class Attempt(Base):
    __tablename__ = "Attempt"

    Id: Mapped[int] = mapped_column(primary_key=True)
    User_id: Mapped[int] = mapped_column(ForeignKey("User.Id"))
    Challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.Id"))

    Submitted_query: Mapped[str] = mapped_column(Text)
    Is_correct: Mapped[bool] = mapped_column(Boolean)
    Score_awarded: Mapped[float] = mapped_column(Float)
    Attempt_number: Mapped[int] = mapped_column(Integer)
    Execution_time: Mapped[float] = mapped_column(Float)
