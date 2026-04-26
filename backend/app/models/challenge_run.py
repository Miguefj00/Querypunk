from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class ChallengeRun(Base):
    """Represents a user run in a challenge"""
    __tablename__ = "ChallengeRun"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id", ondelete="CASCADE")
    )

    challenge_id: Mapped[int] = mapped_column(
        ForeignKey("Challenge.id", ondelete="CASCADE")
    )

    started_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)