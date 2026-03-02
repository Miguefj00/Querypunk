from sqlalchemy import Column, Integer, ForeignKey

from app.database.connection import Base


class UserGroup(Base):
    __tablename__ = "UserGroup"

    user_id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("Group.id"), primary_key=True)