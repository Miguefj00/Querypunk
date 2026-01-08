from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class User(Base):
    __tablename__ = "User"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Role_id: Mapped[int] = mapped_column(ForeignKey("Role.Id"))
    Username: Mapped[str] = mapped_column(String, nullable=False)
    Email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    Password_hash: Mapped[str] = mapped_column(String, nullable=False)
    Created_at: Mapped[str] = mapped_column(Text, nullable=False)
    Last_login: Mapped[str] = mapped_column(Text, nullable=False)


