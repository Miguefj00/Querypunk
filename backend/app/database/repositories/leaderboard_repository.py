from app.models.leaderboard import Leaderboard


class LeaderboardRepository:

    @staticmethod
    def upsert_score(db, user_id, challenge_id, score):
        entry = db.query(Leaderboard).filter_by(
            user_id=user_id,
            challenge_id=challenge_id
        ).first()

        if entry:
            if score > entry.score:
                entry.score = score
        else:
            entry = Leaderboard(
                user_id=user_id,
                challenge_id=challenge_id,
                score=score
            )
            db.add(entry)

        db.commit()
        db.refresh(entry)

        return entry
