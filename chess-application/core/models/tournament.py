from .base import Base
from sqlalchemy import Column, Integer, String

class Tournament(Base):
    __tablename__ = 'tournaments'

    tournament_id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    date = Column(String, nullable=False)
    qualification_level = Column(String, nullable=False)