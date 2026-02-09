from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Leaderboard(Base):
    __tablename__ = "Leaderboard"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.id"))
    best_score: Mapped[int] = mapped_column(Integer, nullable=False)
    best_time: Mapped[str] = mapped_column(Text, nullable=False)
    attempts_used: Mapped[int] = mapped_column(Integer, nullable=False)
    last_updated: Mapped[str] = mapped_column(Text, nullable=False)
