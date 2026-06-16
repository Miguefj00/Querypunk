import csv
from io import StringIO
from fastapi import HTTPException, UploadFile, BackgroundTasks
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import User
from app.models.group import Group
from app.models.user_group import UserGroup
from app.services.email_service import EmailService
from app.services.user_service import UserService
from app.database.repositories.user_repository import UserRepository
from app.utils.role_utils import ROLE_TEACHER, ROLE_ADMIN
from app.utils.user_utils import assign_user_to_group, generate_password_from_identifier, generate_username_from_name


class GroupService:

    @staticmethod
    def create_group(db: Session, name: str, description: str, created_by: int):
        """ Creates a new student group ensuring unique name. """
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
            file: UploadFile,
            background_tasks: BackgroundTasks
    ):
        """
        Bulk import students from CSV file.
        Existing users are assigned to the group,
        new users are automatically created and emailed.
        """
        group = db.query(Group).filter(Group.id == group_id).first()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="File must be CSV")

        content = await file.read()

        csv_data = StringIO(content.decode("utf-8"))
        reader = csv.DictReader(csv_data)

        users_assigned = 0
        created_users = 0

        for row in reader:

            name = row.get("Nombre")
            surname = row.get("Apellido")
            email = row.get("Email")
            identifier = row.get("Identificador")

            if not email:
                continue

            email = email.strip().lower()

            user = UserRepository.get_by_email(db, email)

            # User already exists
            if user:

                try:
                    GroupService.add_user_to_group(
                        db,
                        group_id,
                        user.username,
                        background_tasks
                    )
                    users_assigned += 1
                except HTTPException:
                    pass

            # User doesn't exist
            else:

                password = generate_password_from_identifier(identifier)

                user = UserService.create_student_auto(
                    db=db,
                    nombre=name,
                    apellido=surname,
                    email=email,
                    password=password
                )

                username = generate_username_from_name(name, surname)

                assign_user_to_group(db, user.id, group_id)

                created_users += 1
                users_assigned += 1

                background_tasks.add_task(
                    EmailService.send_new_user_credentials,
                    email,
                    username,
                    password,
                    group.name
                )

        db.commit()

        return {
            "group_id": group_id,
            "created_users": created_users,
            "users_assigned": users_assigned
        }

    @staticmethod
    def add_user_to_group(
            db: Session,
            group_id: int,
            username: str,
            background_tasks: BackgroundTasks
    ):
        """
        Assign an existing user to a group manually.
        Sends email notification if successful.
        """

        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        user = db.query(User).filter(
            User.username == username
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        assigned = assign_user_to_group(
            db,
            user.id,
            group.id
        )

        if not assigned:
            raise HTTPException(
                status_code=400,
                detail="User already assigned to this group"
            )

        db.commit()

        background_tasks.add_task(
            EmailService.send_existing_user_added,
            user.email,
            group.name
        )

        return {
            "group_id": group.id,
            "users_assigned": 1
        }

    @staticmethod
    def get_available_users(
            db: Session,
            group_id: int
    ):
        """ Returns users who don't belong to the group """
        group = db.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        assigned_ids = [
            user.id for user in group.users
        ]

        users = db.query(User).filter(
            User.role_id != ROLE_ADMIN
        )

        if assigned_ids:
            users = users.filter(
                ~User.id.in_(assigned_ids)
            )

        return users.all()

    @staticmethod
    def get_all_groups(db: Session):
        """ Returns all groups with number of students per group. """
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
        """ Returns all users belonging to a group. """
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
        """
        Updates group name and description.
        Teachers can only modify their own groups.
        """
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
        """ Deletes a group and all its user assignments. """
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if current_user.role_id == ROLE_TEACHER and group.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this group")

        db.query(UserGroup).filter(UserGroup.group_id == group_id).delete()

        db.delete(group)
        db.commit()

        return {"detail": "Group deleted successfully"}

