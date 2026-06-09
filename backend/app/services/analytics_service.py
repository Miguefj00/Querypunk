from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.models import Challenge, Leaderboard, User
from app.models.attempt import Attempt
from app.models.challenge_run import ChallengeRun
from app.utils.difficulty_utils import get_ordered_difficulties


class AnalyticsService:

    @staticmethod
    def get_overview(db: Session):
        """
        Returns global system metrics (last 30 days + totals):
        active users, runs, attempts, success rates and averages.
        """
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
        """
        Returns aggregated analytics per challenge:
        finished runs, successes, cancellations, avg attempts and avg time.
        """
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
        """
        Returns the full student dashboard:
        overview + behaviour + progress.
        """
        return {
            "overview": AnalyticsService._get_user_overview(db, user_id),
            "behaviour": AnalyticsService._get_user_behaviour(db, user_id),
            "progress": AnalyticsService._get_user_progress(db, user_id)
        }

    @staticmethod
    def _get_user_overview(db, user_id: int):
        """
        Global student metrics:
        total score, solved challenges and average resolution time.
        """
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
        """
        Analyzes student behaviour:
        total runs, success rate, attempts per run and first-try success rate.
        """
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
        """
        Returns student progress grouped by difficulty:
        global challenges vs played challenges.
        """
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

    @staticmethod
    def get_student_attempts_history(db: Session, user_id: int):
        """
        Returns the complete SQL query history of a student:
        Challenges → Runs → Executed attempts.
        Designed for teacher visualization.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        rows = (
            db.query(
                Challenge.id.label("challenge_id"),
                Challenge.title.label("challenge_title"),
                ChallengeRun.id.label("run_id"),
                ChallengeRun.started_at,
                Attempt.id.label("attempt_id"),
                Attempt.submitted_query,
                Attempt.is_correct
            )
            .join(ChallengeRun, ChallengeRun.challenge_id == Challenge.id)
            .join(Attempt, Attempt.challenge_run_id == ChallengeRun.id)
            .filter(ChallengeRun.user_id == user_id)
            .order_by(Challenge.id, ChallengeRun.id, Attempt.id)
            .all()
        )

        challenges_map = {}

        for row in rows:
            ch_id = row.challenge_id
            run_id = row.run_id

            if ch_id not in challenges_map:
                challenges_map[ch_id] = {
                    "challenge_id": ch_id,
                    "challenge_title": row.challenge_title,
                    "runs": {}
                }

            if run_id not in challenges_map[ch_id]["runs"]:
                challenges_map[ch_id]["runs"][run_id] = {
                    "run_id": run_id,
                    "started_at": row.started_at,
                    "attempts": []
                }

            challenges_map[ch_id]["runs"][run_id]["attempts"].append({
                "attempt_id": row.attempt_id,
                "query": row.submitted_query,
                "is_correct": row.is_correct
            })

        response = []
        for ch in challenges_map.values():
            ch["runs"] = list(ch["runs"].values())
            response.append(ch)

        return response

    @staticmethod
    def get_my_progress(
            db: Session,
            user_id: int
    ):
        """
        Returns only the progress section
        for the currently authenticated user.
        """
        return AnalyticsService._get_user_progress(
            db,
            user_id
        )

    @staticmethod
    def get_my_challenges_progress(
            db: Session,
            user_id: int
    ):
        """ Returns progress inside a chapter. """
        solved = (
            db.query(
                Leaderboard.challenge_id,
                Challenge.chapter_id,
                Leaderboard.score
            )
            .join(
                Challenge,
                Challenge.id == Leaderboard.challenge_id
            )
            .filter(
                Leaderboard.user_id == user_id
            )
            .all()
        )

        return [
            {
                "challenge_id": row.challenge_id,
                "chapter_id": row.chapter_id,
                "best_score": row.score
            }
            for row in solved
        ]