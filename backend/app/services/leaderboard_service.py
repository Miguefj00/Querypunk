from fastapi import HTTPException
from sqlalchemy import func

from app.database.repositories.game_settings_repository import GameSettingsRepository
from app.models.challenge_run import ChallengeRun
from app.models.leaderboard import Leaderboard
from app.models.challenge import Challenge
from app.models.user import User


class LeaderboardService:

    @staticmethod
    def get_challenge_leaderboard(db, challenge_id: int):
        settings = GameSettingsRepository.get_settings(db)
        if not settings.show_challenge_leaderboard:
            raise HTTPException(
                status_code=403,
                detail="Challenge leaderboard is disabled by instructor"
            )

        runs_subq = db.query(
            ChallengeRun.user_id,
            func.count(ChallengeRun.id).label("runs_count")
        ).filter(
            ChallengeRun.challenge_id == challenge_id
        ).group_by(
            ChallengeRun.user_id
        ).subquery()

        results = db.query(
            Leaderboard.user_id,
            User.username,
            Leaderboard.score,
            func.coalesce(runs_subq.c.runs_count, 0).label("runs_count")
        ).join(
            User, Leaderboard.user_id == User.id
        ).outerjoin(
            runs_subq, runs_subq.c.user_id == Leaderboard.user_id
        ).filter(
            Leaderboard.challenge_id == challenge_id
        ).order_by(
            Leaderboard.score.desc(),
            func.coalesce(runs_subq.c.runs_count, 0).asc()
        ).all()

        ranking = []
        for i, row in enumerate(results, start=1):
            ranking.append({
                "position": i,
                "user_id": row.user_id,
                "username": row.username,
                "score": row.score,
                "runs_count": row.runs_count
            })

        return ranking

    @staticmethod
    def get_chapter_leaderboard(db, chapter_id: int):
        settings = GameSettingsRepository.get_settings(db)

        if not settings.show_chapter_leaderboard:
            raise HTTPException(
                status_code=403,
                detail="Chapter leaderboard is disabled by instructor"
            )

        # Runs totales del usuario en el chapter
        runs_subq = db.query(
            ChallengeRun.user_id,
            func.count(ChallengeRun.id).label("runs_count")
        ).join(
            Challenge, ChallengeRun.challenge_id == Challenge.id
        ).filter(
            Challenge.chapter_id == chapter_id
        ).group_by(
            ChallengeRun.user_id
        ).subquery()

        results = db.query(
            Leaderboard.user_id,
            User.username,
            func.sum(Leaderboard.score).label("total_score"),
            func.coalesce(runs_subq.c.runs_count, 0).label("runs_count")
        ).join(
            Challenge, Leaderboard.challenge_id == Challenge.id
        ).join(
            User, Leaderboard.user_id == User.id
        ).outerjoin(
            runs_subq, runs_subq.c.user_id == Leaderboard.user_id
        ).filter(
            Challenge.chapter_id == chapter_id
        ).group_by(
            Leaderboard.user_id,
            User.username,
            runs_subq.c.runs_count
        ).order_by(
            func.sum(Leaderboard.score).desc(),
            func.coalesce(runs_subq.c.runs_count, 0).asc()
        ).all()

        ranking = []
        for i, row in enumerate(results, start=1):
            ranking.append({
                "position": i,
                "user_id": row.user_id,
                "username": row.username,
                "score": row.total_score,
                "runs_count": row.runs_count
            })

        return ranking

    @staticmethod
    def get_global_leaderboard(db):
        settings = GameSettingsRepository.get_settings(db)

        if not settings.show_global_leaderboard:
            raise HTTPException(
                status_code=403,
                detail="Global leaderboard is disabled by instructor"
            )

        runs_subq = db.query(
            ChallengeRun.user_id,
            func.count(ChallengeRun.id).label("runs_count")
        ).group_by(
            ChallengeRun.user_id
        ).subquery()

        results = db.query(
            Leaderboard.user_id,
            User.username,
            func.sum(Leaderboard.score).label("total_score"),
            func.coalesce(runs_subq.c.runs_count, 0).label("runs_count")
        ).join(
            User, Leaderboard.user_id == User.id
        ).outerjoin(
            runs_subq, runs_subq.c.user_id == Leaderboard.user_id
        ).group_by(
            Leaderboard.user_id,
            User.username,
            runs_subq.c.runs_count
        ).order_by(
            func.sum(Leaderboard.score).desc(),
            func.coalesce(runs_subq.c.runs_count, 0).asc()
        ).all()

        ranking = []
        for i, row in enumerate(results, start=1):
            ranking.append({
                "position": i,
                "user_id": row.user_id,
                "username": row.username,
                "score": row.total_score,
                "runs_count": row.runs_count
            })

        return ranking
