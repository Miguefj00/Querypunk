from sqlalchemy import Column, Integer, Text, Boolean, Float, ForeignKey
from app.database.connection import Base

class Attempt(Base):
    __tablename__ = "Attempt"

    Id = Column(Integer, primary_key=True)
    User_id = Column(Integer, ForeignKey("User.Id"))
    Challenge_id = Column(Integer, ForeignKey("Challenge.Id"))
    Submitted_query = Column(Text, nullable=False)
    Is_correct = Column(Boolean, nullable=False)
    Score_awarded = Column(Float, nullable=False)
    Attempt_number = Column(Integer, nullable=False)
    Execution_time = Column(Float, nullable=False)
