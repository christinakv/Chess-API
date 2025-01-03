from sqlalchemy import Column, Integer, String
from .base import Base

class ChessPlayer(Base):
    __tablename__ = "chess_players"

    chess_player_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    world_rank = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String, nullable=False)