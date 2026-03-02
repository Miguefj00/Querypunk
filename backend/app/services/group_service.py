import csv
from io import StringIO
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.group import Group
from app.services.user_service import UserService
from app.database.repositories.user_repository import UserRepository
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
        existing_users_assigned = 0

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
                assign_user_to_group(db, existing_user.id, group.id)
                existing_users_assigned += 1

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

                assign_user_to_group(db, new_user.id, group.id)

                created_users += 1

        return {
            "group_id": group.id,
            "created_users": created_users,
            "existing_users_assigned": existing_users_assigned
        }

