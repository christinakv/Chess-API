from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class Participant(Base):
    __tablename__ = "participants"

    participant_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.tournament_id"))
    chess_player_id = Column(Integer, ForeignKey("chess_players.chess_player_id"))
    place = Column(Integer, nullable=False)