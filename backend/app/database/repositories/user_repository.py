from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        stmt = select(User).where(User.Id == user_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        stmt = select(User).where(User.Username == username)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        stmt = select(User).where(User.Email == email)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_first(db: Session) -> User | None:
        stmt = select(User)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_role(db: Session, role_id: int):
        return db.query(User).filter(User.Role_id == role_id).first()
