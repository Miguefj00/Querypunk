from sqlalchemy import func
from app.models.leaderboard import Leaderboard
from app.models.challenge import Challenge
from app.models.user import User


class LeaderboardService:

    @staticmethod
    def get_challenge_leaderboard(db, challenge_id: int):

        results = db.query(
            Leaderboard.user_id,
            User.username,
            Leaderboard.score
        ).join(User).filter(
            Leaderboard.challenge_id == challenge_id
        ).order_by(
            Leaderboard.score.desc()
        ).all()

        ranking = []
        for i, row in enumerate(results, start=1):
            ranking.append({
                "position": i,
                "user_id": row.user_id,
                "username": row.username,
                "score": row.score
            })

        return ranking

    @staticmethod
    def get_chapter_leaderboard(db, chapter_id: int):

        results = db.query(
            Leaderboard.user_id,
            User.username,
            func.sum(Leaderboard.score).label("total_score")
        ).join(Challenge, Leaderboard.challenge_id == Challenge.id) \
            .join(User, Leaderboard.user_id == User.id) \
            .filter(
            Challenge.chapter_id == chapter_id
        ).group_by(
            Leaderboard.user_id,
            User.username
        ).order_by(
            func.sum(Leaderboard.score).desc()
        ).all()

        ranking = []
        for i, row in enumerate(results, start=1):
            ranking.append({
                "position": i,
                "user_id": row.user_id,
                "username": row.username,
                "score": row.total_score
            })

        return ranking

    @staticmethod
    def get_global_leaderboard(db):

        results = db.query(
            Leaderboard.user_id,
            User.username,
            func.sum(Leaderboard.score).label("total_score")
        ).join(User, Leaderboard.user_id == User.id) \
            .group_by(
            Leaderboard.user_id,
            User.username
        ).order_by(
            func.sum(Leaderboard.score).desc()
        ).all()

        ranking = []
        for i, row in enumerate(results, start=1):
            ranking.append({
                "position": i,
                "user_id": row.user_id,
                "username": row.username,
                "score": row.total_score
            })

        return ranking