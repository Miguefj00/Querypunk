import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import os
from dotenv import load_dotenv

from app.database.connection import SessionLocal
from app.models.user import User
from app.database.repositories.user_repository import UserRepository
from app.security.password import hash_password
from app.core.roles import ROLE_ADMIN

load_dotenv()


def create_admin():
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not email or not password:
        raise RuntimeError("Missing ADMIN_* variables in .env")

    db = SessionLocal()

    try:
        existing_admin = UserRepository.get_by_role(db, ROLE_ADMIN)
        if existing_admin:
            print("✔ Admin already exists. Nothing to do.")
            return

        admin = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role_id=ROLE_ADMIN,
            created_at=datetime.utcnow().isoformat(),
            last_login=None,
        )

        db.add(admin)
        db.commit()

        print("✅ Admin user created successfully")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
