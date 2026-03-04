import csv
from io import StringIO
from fastapi import HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import User
from app.models.group import Group
from app.models.user_group import UserGroup
from app.services.user_service import UserService
from app.database.repositories.user_repository import UserRepository
from app.utils.role_utils import ROLE_TEACHER
from app.utils.user_utils import assign_user_to_group, generate_password_from_identifier


class GroupService:

    @staticmethod
    def create_group(db: Session, name: str, description: str, created_by: int):

        existing = db.query(Group).filter(Group.name == name).first()
        if existing:
            raise HTTPException(status_code=409, detail="Group already exists")

        group = Group(
            name=name,
            description=description,
            created_by=created_by
        )

        db.add(group)
        db.commit()
        db.refresh(group)

        return group

    @staticmethod
    async def upload_students_to_group(
            db: Session,
            group_id: int,
            file: UploadFile
    ):

        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        content = await file.read()
        decoded = content.decode("utf-8")
        csv_reader = csv.DictReader(StringIO(decoded))

        created_users = 0
        users_assigned = 0

        try:
            for row in csv_reader:

                if not all(col in row for col in ["Nombre", "Apellido", "Email", "Identificador"]):
                    raise HTTPException(
                        status_code=400,
                        detail="CSV must contain Nombre, Apellido, Email and Identificador columns"
                    )

                nombre = row.get("Nombre", "").strip()
                apellido = row.get("Apellido", "").strip()
                email = row.get("Email", "").strip()
                identificador = row.get("Identificador", "").strip()

                if not email or not identificador:
                    continue

                existing_user = UserRepository.get_by_email(db, email)

                # User exists
                if existing_user:
                    was_assigned = assign_user_to_group(db, existing_user.id, group.id)

                    if was_assigned:
                        users_assigned += 1

                # New user
                else:
                    password = generate_password_from_identifier(identificador)

                    new_user = UserService.create_student_auto(
                        db=db,
                        nombre=nombre,
                        apellido=apellido,
                        email=email,
                        password=password
                    )

                    was_assigned = assign_user_to_group(db, new_user.id, group.id)

                    created_users += 1

                    if was_assigned:
                        users_assigned += 1

            db.commit()

        except Exception:
            db.rollback()
            raise

        return {
            "group_id": group.id,
            "created_users": created_users,
            "users_assigned": users_assigned
        }

    @staticmethod
    def get_all_groups(db: Session):

        results = (
            db.query(
                Group.id,
                Group.name,
                Group.description,
                func.count(UserGroup.user_id).label("student_count")
            )
            .outerjoin(UserGroup, Group.id == UserGroup.group_id)
            .group_by(Group.id)
            .all()
        )

        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "student_count": r.student_count
            }
            for r in results
        ]

    @staticmethod
    def get_group_users(db: Session, group_id: int):

        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        users = (
            db.query(User)
            .join(UserGroup, User.id == UserGroup.user_id)
            .filter(UserGroup.group_id == group_id)
            .all()
        )

        return users

    @staticmethod
    def update_group(
            db: Session,
            group_id: int,
            name: str,
            description: str,
            current_user: User
    ):

        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if current_user.role_id == ROLE_TEACHER and group.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this group")

        group.name = name
        group.description = description

        db.commit()
        db.refresh(group)

        return group

    @staticmethod
    def delete_group(
            db: Session,
            group_id: int,
            current_user: User
    ):

        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if current_user.role_id == ROLE_TEACHER and group.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this group")

        db.query(UserGroup).filter(UserGroup.group_id == group_id).delete()

        db.delete(group)
        db.commit()

        return {"detail": "Group deleted successfully"}

