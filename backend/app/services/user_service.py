from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.utils.role_utils import ROLE_TEACHER, ROLE_STUDENT, ROLE_ADMIN
from app.database.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, ChangePasswordRequest, UserUpdate
from app.security.password import verify_password
from app.security.password import hash_password
from app.utils.user_utils import generate_username_from_name


class UserService:

    @staticmethod
    def _create_user(
            db: Session,
            *,
            username: str,
            email: str,
            password: str,
            role_id: int
    ) -> User:
        """ Internal helper that creates a user with hashed password. """
        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role_id=role_id,
            created_at=datetime.utcnow(),
            last_login=None
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def create(db: Session, data: UserCreate):
        """
        Creates a user manually (teacher or student).
        Ensures username and email uniqueness.
        """
        if UserRepository.get_by_username(db, data.username):
            raise HTTPException(status_code=409, detail="Username already exists")

        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=409, detail="Email already exists")

        if data.role == "teacher":
            role_id = ROLE_TEACHER
        else:
            role_id = ROLE_STUDENT

        return UserService._create_user(
            db,
            username=data.username,
            email=data.email,
            password=data.password,
            role_id=role_id
        )

    @staticmethod
    def create_student_auto(
            db: Session,
            nombre: str,
            apellido: str,
            email: str,
            password: str
    ) -> User:
        """ Automatically creates a student (used during CSV import). """
        username = generate_username_from_name(nombre, apellido)

        if UserRepository.get_by_email(db, email):
            raise HTTPException(status_code=409, detail="Email already exists")

        return UserService._create_user(
            db=db,
            username=username,
            email=email,
            password=password,
            role_id=ROLE_STUDENT
        )

    @staticmethod
    def change_password(db: Session, current_user: User, data: ChangePasswordRequest):
        """ Allows a user to change their password after verifying the current one. """
        if not verify_password(data.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        if len(data.new_password) < 6:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 6 characters"
            )

        current_user.password_hash = hash_password(data.new_password)

        db.commit()

        return {"detail": "Password updated successfully"}

    @staticmethod
    def get_all(db: Session, current_user: User):
        """
        Returns all users.
        Non-admins cannot see admin accounts.
        """
        users = UserRepository.get_all(db)

        if current_user.role_id != ROLE_ADMIN:
            users = [u for u in users if u.role_id != ROLE_ADMIN]

        return users

    @staticmethod
    def get_by_id(db: Session, user_id: int, current_user: User):
        """ Returns a user by ID with role-based access restrictions. """
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.role_id == ROLE_ADMIN and current_user.role_id != ROLE_ADMIN:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    @staticmethod
    def update(db: Session, user_id: int, user_update: UserUpdate, current_user: User):
        """
        Updates user data.
        Users can update themselves, admins can update anyone.
        """
        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        is_admin = current_user.role_id == ROLE_ADMIN

        if not is_admin and current_user.id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own user"
            )

        return UserRepository.update(db, user, user_update)

    @staticmethod
    def delete(db: Session, user_id: int, current_user: User):
        """
        Deletes a user with role rules:
        - Users can delete themselves (except admin)
        - Teachers can delete students only
        - Admin can delete anyone except itself
        """
        target_user = UserRepository.get_by_id(db, user_id)

        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Self deletion forbidden for everyone
        if current_user.id == target_user.id:
            raise HTTPException(
                status_code=400,
                detail="You cannot delete your own account"
            )

        # Admin can delete anyone except itself
        if current_user.role_id == ROLE_ADMIN:
            UserRepository.delete(db, target_user)
            return {"detail": "User deleted successfully"}

        # Teacher can delete students only
        if current_user.role_id == ROLE_TEACHER:
            if target_user.role_id == ROLE_STUDENT:
                UserRepository.delete(db, target_user)
                return {"detail": "User deleted successfully"}

        # Otherwise forbidden
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this user"
        )

    @staticmethod
    def delete_bulk(db: Session, user_ids: list[int], current_user: User):
        """ Bulk deletion based on permissions. """
        users = UserRepository.get_by_ids(db, user_ids)

        if not users:
            raise HTTPException(
                status_code=404,
                detail="Users not found"
            )

        deletable_ids = []

        for user in users:

            # Self delete forbidden
            if user.id == current_user.id:
                continue

            # Admin can delete everybody excepts himself
            if current_user.role_id == ROLE_ADMIN:
                deletable_ids.append(user.id)
                continue

            # Teacher or student
            if (
                    current_user.role_id == ROLE_TEACHER
                    and user.role_id == ROLE_STUDENT
            ):
                deletable_ids.append(user.id)

        if not deletable_ids:
            raise HTTPException(
                status_code=403,
                detail="No users can be deleted with your permissions"
            )

        deleted = UserRepository.delete_many(
            db,
            deletable_ids
        )

        return {
            "detail": f"{deleted} users deleted successfully",
            "deleted_count": deleted
        }
