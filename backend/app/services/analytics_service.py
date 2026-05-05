from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.models import Challenge, Leaderboard
from app.models.attempt import Attempt
from app.models.challenge_run import ChallengeRun
from app.utils.difficulty_utils import get_ordered_difficulties


class AnalyticsService:

    @staticmethod
    def get_overview(db: Session):
        now = datetime.utcnow()
        last_30_days = now - timedelta(days=30)

        active_users = (
            db.query(func.count(distinct(ChallengeRun.user_id)))
            .filter(ChallengeRun.started_at >= last_30_days)
            .scalar()
        )

        total_runs = db.query(func.count(ChallengeRun.id)).scalar()

        finished_runs = db.query(func.count(ChallengeRun.id)).filter(
            ChallengeRun.finished_at.isnot(None)
        ).scalar()

        successful_runs = db.query(func.count(ChallengeRun.id)).filter(
            ChallengeRun.is_successful.is_(True)
        ).scalar()

        cancelled_or_reset_runs = db.query(func.count(ChallengeRun.id)).filter(
            ChallengeRun.is_successful.is_(False)
        ).scalar()

        run_success_rate = (
            successful_runs / finished_runs * 100 if finished_runs else 0
        )

        total_attempts = db.query(func.count(Attempt.id)).scalar()

        avg_resolution_time = (
            db.query(func.avg(Attempt.resolution_time))
            .filter(Attempt.is_correct.is_(True))
            .scalar()
        )

        avg_attempts_per_run = (
            total_attempts / finished_runs if finished_runs else 0
        )

        return {
            "active_users_30d": active_users,
            "total_runs": total_runs,
            "successful_runs": successful_runs,
            "cancelled_or_reset_runs": cancelled_or_reset_runs,
            "run_success_rate": round(run_success_rate, 2),
            "total_attempts": total_attempts,
            "avg_resolution_time_seconds": round(avg_resolution_time or 0, 2),
            "avg_attempts_per_run": round(avg_attempts_per_run, 2)
        }

    @staticmethod
    def get_challenges_analytics(db: Session):
        challenges = db.query(Challenge.id).all()
        results = []

        for (challenge_id,) in challenges:

            finished_runs = db.query(func.count(ChallengeRun.id)).filter(
                ChallengeRun.challenge_id == challenge_id,
                ChallengeRun.finished_at.isnot(None)
            ).scalar()

            successful_runs = db.query(func.count(ChallengeRun.id)).filter(
                ChallengeRun.challenge_id == challenge_id,
                ChallengeRun.is_successful.is_(True)
            ).scalar()

            cancelled_or_reset_runs = db.query(func.count(ChallengeRun.id)).filter(
                ChallengeRun.challenge_id == challenge_id,
                ChallengeRun.is_successful.is_(False)
            ).scalar()

            run_success_rate = (
                successful_runs / finished_runs * 100 if finished_runs else 0
            )

            total_attempts = db.query(func.count(Attempt.id)).filter(
                Attempt.challenge_id == challenge_id
            ).scalar()

            avg_resolution_time = db.query(func.avg(Attempt.resolution_time)).filter(
                Attempt.challenge_id == challenge_id,
                Attempt.is_correct.is_(True)
            ).scalar()

            avg_attempts_per_run = (
                total_attempts / finished_runs if finished_runs else 0
            )

            results.append({
                "challenge_id": challenge_id,
                "total_runs": finished_runs,
                "successful_runs": successful_runs,
                "cancelled_or_reset_runs": cancelled_or_reset_runs,
                "run_success_rate": round(run_success_rate, 2),
                "avg_attempts_per_run": round(avg_attempts_per_run, 2),
                "avg_resolution_time_seconds": round(avg_resolution_time or 0, 2),
            })

        return results

    @staticmethod
    def get_user_dashboard(db, user_id: int):
        return {
            "overview": AnalyticsService._get_user_overview(db, user_id),
            "behaviour": AnalyticsService._get_user_behaviour(db, user_id),
            "progress": AnalyticsService._get_user_progress(db, user_id)
        }

    @staticmethod
    def _get_user_overview(db, user_id: int):
        total_score, challenges_solved = db.query(
            func.coalesce(func.sum(Leaderboard.score), 0),
            func.count(Leaderboard.challenge_id)
        ).filter(Leaderboard.user_id == user_id).first()

        avg_score = db.query(func.avg(Leaderboard.score)).filter(
            Leaderboard.user_id == user_id
        ).scalar() or 0

        avg_resolution_time = db.query(func.avg(Attempt.resolution_time)).filter(
            Attempt.user_id == user_id,
            Attempt.is_correct.is_(True)
        ).scalar() or 0

        return {
            "total_score": int(total_score),
            "challenges_solved": challenges_solved,
            "avg_score_per_challenge": round(avg_score, 2),
            "avg_resolution_time_sec": round(avg_resolution_time, 2)
        }

    @staticmethod
    def _get_user_behaviour(db, user_id: int):
        finished_runs = db.query(func.count(ChallengeRun.id)).filter(
            ChallengeRun.user_id == user_id,
            ChallengeRun.finished_at.isnot(None)
        ).scalar()

        successful_runs = db.query(func.count(ChallengeRun.id)).filter(
            ChallengeRun.user_id == user_id,
            ChallengeRun.is_successful.is_(True)
        ).scalar()

        cancelled_or_reset_runs = db.query(func.count(ChallengeRun.id)).filter(
            ChallengeRun.user_id == user_id,
            ChallengeRun.is_successful.is_(False)
        ).scalar()

        run_success_rate = (
            successful_runs / finished_runs * 100 if finished_runs else 0
        )

        total_attempts = db.query(func.count(Attempt.id)).filter(
            Attempt.user_id == user_id
        ).scalar()

        avg_attempts_per_run = (
            total_attempts / finished_runs if finished_runs else 0
        )

        runs_attempts = db.query(
            Attempt.challenge_run_id,
            func.count(Attempt.id).label("attempts")
        ).filter(
            Attempt.user_id == user_id
        ).group_by(Attempt.challenge_run_id).subquery()

        first_try_success_runs = db.query(func.count(ChallengeRun.id)).join(
            runs_attempts,
            runs_attempts.c.challenge_run_id == ChallengeRun.id
        ).filter(
            ChallengeRun.user_id == user_id,
            ChallengeRun.is_successful.is_(True),
            runs_attempts.c.attempts == 1
        ).scalar()

        first_try_rate = (
            first_try_success_runs / successful_runs * 100 if successful_runs else 0
        )

        return {
            "total_runs": finished_runs,
            "successful_runs": successful_runs,
            "cancelled_or_reset_runs": cancelled_or_reset_runs,
            "run_success_rate": round(run_success_rate, 2),
            "avg_attempts_per_run": round(avg_attempts_per_run, 2),
            "first_try_success_rate": round(first_try_rate, 2)
        }

    @staticmethod
    def _get_user_progress(db, user_id: int):
        difficulties = get_ordered_difficulties()

        total_per_difficulty = dict(
            db.query(
                Challenge.difficulty,
                func.count(Challenge.id)
            ).group_by(Challenge.difficulty).all()
        )

        solved_per_difficulty = dict(
            db.query(
                Challenge.difficulty,
                func.count(Leaderboard.challenge_id)
            ).join(Challenge, Leaderboard.challenge_id == Challenge.id)
            .filter(Leaderboard.user_id == user_id)
            .group_by(Challenge.difficulty).all()
        )

        played_per_difficulty = dict(
            db.query(
                Challenge.difficulty,
                func.count(func.distinct(ChallengeRun.challenge_id))
            ).join(Challenge, ChallengeRun.challenge_id == Challenge.id)
            .filter(ChallengeRun.user_id == user_id)
            .group_by(Challenge.difficulty).all()
        )

        global_challenges = {}
        played_challenges = {}

        for diff in difficulties:
            global_challenges[diff] = {
                "solved": solved_per_difficulty.get(diff, 0),
                "total": total_per_difficulty.get(diff, 0)
            }

            played_challenges[diff] = {
                "solved": solved_per_difficulty.get(diff, 0),
                "total": played_per_difficulty.get(diff, 0)
            }

        return {
            "global_challenges": global_challenges,
            "played_challenges": played_challenges
        }
