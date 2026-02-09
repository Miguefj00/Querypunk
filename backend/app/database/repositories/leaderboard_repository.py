from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.leaderboard import Leaderboard


class LeaderboardRepository:

    @staticmethod
    def get_entry(db: Session, user_id: int, challenge_id: int) -> Leaderboard | None:
        stmt = select(Leaderboard).where(
            Leaderboard.user_id == user_id,
            Leaderboard.challenge_id == challenge_id
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def save(db: Session, entry: Leaderboard) -> Leaderboard:
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
