from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Participant(Base):
    __tablename__ = 'participants'

    participant_id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.tournament_id'))
    chess_player_id: Mapped[int] = mapped_column(ForeignKey('chess_players.chess_player_id'))
    place: Mapped[int] = mapped_column(nullable=False)
    place: Mapped[int] = mapped_column(nullable=False)