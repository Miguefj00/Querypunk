from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Leaderboard(Base):
    __tablename__ = "Leaderboard"

    Id: Mapped[int] = mapped_column(primary_key=True)
    User_id: Mapped[int] = mapped_column(ForeignKey("User.Id"))
    Challenge_id: Mapped[int] = mapped_column(ForeignKey("Challenge.Id"))
    Best_score: Mapped[int] = mapped_column(Integer, nullable=False)
    Best_time: Mapped[str] = mapped_column(Text, nullable=False)
    Attempts_used: Mapped[int] = mapped_column(Integer, nullable=False)
    Last_updated: Mapped[str] = mapped_column(Text, nullable=False)
