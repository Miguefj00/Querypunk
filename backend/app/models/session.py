from typing import Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Session(Base):
    __tablename__ = "Session"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    login_time: Mapped[str] = mapped_column(Text, nullable=False)
    logout_time: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str] = mapped_column(Text, nullable=False)
