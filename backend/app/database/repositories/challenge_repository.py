from sqlalchemy import select, literal
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate, ValidationRules
from app.utils.difficulty_utils import evaluate_sql_difficulty


class ChallengeRepository:

    @staticmethod
    def get_by_id(db: Session, challenge_id: int) -> Challenge | None:
        # Retrieves a single challenge by id
        stmt = select(Challenge).where(Challenge.id == literal(challenge_id))
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_chapter(db: Session, chapter_id: int) -> list[Challenge]:
        # Returns all challenges belonging to a chapter
        stmt = select(Challenge).where(Challenge.chapter_id == chapter_id)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_difficulties_by_chapter(db: Session, chapter_id: int):
        # Used for chapter difficulty calculation
        rows = (
            db.query(Challenge.difficulty)
            .filter(Challenge.chapter_id == chapter_id)
            .filter(Challenge.difficulty.isnot(None))
            .all()
        )

        return [row[0] for row in rows]

    @staticmethod
    def get_difficulties_by_chapter_sqlite(conn, chapter_id: int):
        # Raw SQLite version used for chapter difficulty calculation
        cursor = conn.cursor()

        cursor.execute("""
                SELECT difficulty FROM challenge WHERE chapter_id = ?
            """, (chapter_id,))

        rows = cursor.fetchall()
        return [r[0] for r in rows]

    @staticmethod
    def create(db: Session, chapter_id: int, data: ChallengeCreate):
        # Creates a new challenge inside a chapter
        payload = data.model_dump()
        payload["chapter_id"] = chapter_id

        challenge = Challenge(**payload)

        db.add(challenge)
        db.flush()
        db.refresh(challenge)

        return challenge

    @staticmethod
    def update(db: Session, challenge: Challenge, data: ChallengeUpdate):
        # Updates a challenge
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(challenge, key, value)

        db.flush()
        db.refresh(challenge)

        return challenge

    @staticmethod
    def delete(db: Session, challenge: Challenge):
        # Removes challenge in cascade
        db.delete(challenge)

    @staticmethod
    def recalc_challenge_difficulty(db: Session, challenge: Challenge):
        # Changes a challenge difficulty after evaluation
        rules = ValidationRules.model_validate(challenge.validation_rules)

        difficulty = evaluate_sql_difficulty(
            challenge.solution,
            rules
        )

        challenge.difficulty = difficulty
        db.flush()
