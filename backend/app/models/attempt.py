from datetime import datetime

from sqlalchemy import Boolean, Float, Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Attempt(Base):
    __tablename__ = "Attempt"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.id"))
    submitted_query: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    execution_time: Mapped[float] = mapped_column(Float)
    rows_returned: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
