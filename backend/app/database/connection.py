import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

# Root folder of the project
BASE_DIR = Path(__file__).resolve().parents[2]

# Read main system database URL from environment
SYSTEM_DATABASE_URL = os.getenv("SYSTEM_DATABASE_URL")
if not SYSTEM_DATABASE_URL:
    raise RuntimeError("SYSTEM_DATABASE_URL not found in environment variables")

# If using SQLite, build absolute path to avoid relative path issues
if SYSTEM_DATABASE_URL.startswith("sqlite"):
    db_path = BASE_DIR / "system_database.db"
    DATABASE_URL = f"sqlite:///{db_path}"
else:
    DATABASE_URL = SYSTEM_DATABASE_URL

# Create SQLAlchemy engine (connection pool manager)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Enable foreign key constraints in SQLite (disabled by default)
@event.listens_for(engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Factory used to create DB sessions per request
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for all SQLAlchemy models
Base = declarative_base()
