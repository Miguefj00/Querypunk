import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

SYSTEM_DATABASE_URL = os.getenv("SYSTEM_DATABASE_URL")

if not SYSTEM_DATABASE_URL:
    raise RuntimeError("SYSTEM_DATABASE_URL not found")

engine = create_engine(
    SYSTEM_DATABASE_URL,
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