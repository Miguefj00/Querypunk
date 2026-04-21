from datetime import datetime

from sqlalchemy import Boolean, Float, Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Attempt(Base):
    __tablename__ = "Attempt"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.id", ondelete="CASCADE"))
    challenge_run_id: Mapped[int] = mapped_column(ForeignKey("ChallengeRun.id", ondelete="CASCADE"))
    submitted_query: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    execution_time: Mapped[float] = mapped_column(Float)
    resolution_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    rows_returned: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
