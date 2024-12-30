from .base import Base
from sqlalchemy import Column, Integer, String

class ChessPlayer(Base):
    __tablename__ = 'chess_players'

    chess_player_fide_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    world_rank = Column(String, nullable=False)
    rating_std = Column(Integer, nullable=False)
    fide_title = Column(String, nullable=False)
