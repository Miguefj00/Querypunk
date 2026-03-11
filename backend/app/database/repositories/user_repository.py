from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserUpdate


class UserRepository:

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_ids(db: Session, user_ids: list[int]) -> list[User]:
        stmt = select(User).where(User.id.in_(user_ids))
        result = db.execute(stmt).scalars().all()
        return list(result)

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_first(db: Session) -> User | None:
        stmt = select(User)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_role(db: Session, role_id: int):
        return db.query(User).filter(User.role_id == role_id).first()

    @staticmethod
    def get_all(db: Session) -> list[User]:
        return (
            db.query(User)
            .order_by(User.username.asc())
            .all()
        )

    @staticmethod
    def update(db: Session, user: User, user_update: UserUpdate) -> User:
        update_data = user_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()

    @staticmethod
    def delete_many(db: Session, user_ids: list[int]) -> int:
        deleted = db.query(User).filter(User.id.in_(user_ids)).delete(
            synchronize_session=False
        )

        db.commit()

        return deleted
