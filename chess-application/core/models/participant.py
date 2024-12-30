from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Participant(Base):
    __tablename__ = 'participants'

    participant_id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.tournament_id'), nullable=False)
    chess_player_id = Column(Integer, ForeignKey('chess_players.chess_player_fide_id'), nullable=False)
    place = Column(Integer, nullable=False)