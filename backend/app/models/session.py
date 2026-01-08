from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class Session(Base):
    __tablename__ = "Session"

    Id: Mapped[int] = mapped_column(primary_key=True)
    User_id: Mapped[int] = mapped_column(ForeignKey("User.Id"))
    Login_time: Mapped[str] = mapped_column(Text, nullable=False)
    Logout_time: Mapped[str] = mapped_column(Text, nullable=False)
    Ip_address: Mapped[str] = mapped_column(Text, nullable=False)
