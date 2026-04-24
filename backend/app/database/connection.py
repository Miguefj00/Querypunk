import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

SYSTEM_DATABASE_URL = os.getenv("SYSTEM_DATABASE_URL")
if not SYSTEM_DATABASE_URL:
    raise RuntimeError("SYSTEM_DATABASE_URL not found in environment variables")

if SYSTEM_DATABASE_URL.startswith("sqlite"):
    db_path = BASE_DIR / "system_database.db"
    DATABASE_URL = f"sqlite:///{db_path}"
else:
    DATABASE_URL = SYSTEM_DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


@event.listens_for(engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
