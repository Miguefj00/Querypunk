from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Leaderboard(Base):
    """Represents game ranking with gamification purposes"""
    __tablename__ = "Leaderboard"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.id", ondelete="CASCADE"))
    score: Mapped[int] = mapped_column(Integer, nullable=False)
