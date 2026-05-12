import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Add project root to Python path when running script directly
sys.path.append(str(BASE_DIR))

import os
from dotenv import load_dotenv

from app.database.connection import SessionLocal
from app.models import User
from app.database.repositories.user_repository import UserRepository
from app.security.password import hash_password
from app.utils.role_utils import ROLE_ADMIN

# Load ADMIN_* variables from .env file
load_dotenv()

"""
Initial admin bootstrap script.

Creates the first administrator account using environment variables.
Intended to run once during deployment or first project setup.
"""


def create_admin():
    """
    Creates the default administrator user if it does not exist.

    Required environment variables:
    - ADMIN_USERNAME
    - ADMIN_EMAIL
    - ADMIN_PASSWORD
    """
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not email or not password:
        raise RuntimeError("Missing ADMIN_* variables in .env")

    db = SessionLocal()  # Open DB session

    try:
        # Ensure only one admin exists in the system
        existing_admin = UserRepository.get_by_role(db, ROLE_ADMIN)
        if existing_admin:
            print("✔ Admin already exists. Nothing to do.")
            return

        admin = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role_id=ROLE_ADMIN,
            created_at=datetime.utcnow(),
            last_login=None,
        )

        db.add(admin)
        db.commit()

        print("✅ Admin user created successfully")

    finally:
        db.close()  # Close DB session


if __name__ == "__main__":
    # Entry point for manual execution
    create_admin()
