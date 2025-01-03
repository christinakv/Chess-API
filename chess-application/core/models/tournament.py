from sqlalchemy import Column, Integer, String
from .base import Base

class Tournament(Base):
    __tablename__ = "tournaments"

    tournament_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    tournament_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    date = Column(String, nullable=False)
    qualification = Column(String, nullable=False)