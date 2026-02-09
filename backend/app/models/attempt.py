from sqlalchemy import Boolean, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Attempt(Base):
    __tablename__ = "Attempt"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.id"))
    submitted_query: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    score_awarded: Mapped[float] = mapped_column(Float)
    attempt_number: Mapped[int] = mapped_column(Integer)
    execution_time: Mapped[float] = mapped_column(Float)
