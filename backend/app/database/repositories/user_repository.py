from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserUpdate


class UserRepository:

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        # Retrieves user by id
        stmt = select(User).where(User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_ids(db: Session, user_ids: list[int]) -> list[User]:
        # Bulk retrieval by ids
        stmt = select(User).where(User.id.in_(user_ids))
        result = db.execute(stmt).scalars().all()
        return list(result)

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        # Retrieves user by username
        stmt = select(User).where(User.username == username)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        # Retrieves user by email
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_role(db: Session, role_id: int):
        # Retrieve user by role
        return db.query(User).filter(User.role_id == role_id).first()

    @staticmethod
    def get_all(db: Session) -> list[User]:
        # Returns all users
        return (
            db.query(User)
            .order_by(User.username.asc())
            .all()
        )

    @staticmethod
    def update(db: Session, user: User, user_update: UserUpdate) -> User:
        # Update of user profile
        update_data = user_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User) -> None:
        # Deletes user
        db.delete(user)
        db.commit()

    @staticmethod
    def delete_many(db: Session, user_ids: list[int]) -> int:
        # Bulk delete users
        deleted = db.query(User).filter(User.id.in_(user_ids)).delete(
            synchronize_session=False
        )

        db.commit()

        return deleted
