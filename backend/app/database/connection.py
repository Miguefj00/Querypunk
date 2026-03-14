import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SYSTEM_DATABASE_URL = os.getenv("SYSTEM_DATABASE_URL")

if not SYSTEM_DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found in environment variables")

if SYSTEM_DATABASE_URL.startswith("sqlite"):
    db_path = BASE_DIR / "system_database.db"
    DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SYSTEM_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
