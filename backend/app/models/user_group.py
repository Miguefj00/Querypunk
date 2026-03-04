from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class UserGroup(Base):
    __tablename__ = "UserGroup"

    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("Group.id"), primary_key=True)
