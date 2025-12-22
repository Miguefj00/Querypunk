from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.app.database.connection import Base

class Challenge(Base):
    __tablename__ = "Challenge"

    Id = Column(Integer, primary_key=True)
    Chapter_id = Column(Integer, ForeignKey("Chapter.Id"))
    Title = Column(String, nullable=False)
    Description = Column(Text, nullable=False)
    Difficulty = Column(Integer, nullable=False)
    Expected_query = Column(Text, nullable=False)
    Max_score = Column(Integer)
