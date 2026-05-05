from sqlalchemy import Column, Integer, Boolean, DateTime, func
from app.database.connection import Base


class GameSettings(Base):
    __tablename__ = "GameSettings"

    id = Column(Integer, primary_key=True, index=True)

    show_global_leaderboard = Column(Boolean, nullable=False, default=True)
    show_chapter_leaderboard = Column(Boolean, nullable=False, default=True)
    show_challenge_leaderboard = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())