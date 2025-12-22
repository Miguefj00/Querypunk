from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class User(Base):
    __tablename__ = "User"

    Id = Column(Integer, primary_key=True, index=True)
    Role_id = Column(Integer, ForeignKey("Role.Id"))
    Username = Column(String, nullable=False)
    Password_hash = Column(String, nullable=False)
    Email = Column(String, nullable=False, unique=True)
