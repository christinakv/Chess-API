from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import ForeignKey

from .base import Base

class Participant(Base):
    __tablename__ = 'participants'

    participant_id: Mapped[int] = mapped_column(unique=True, primary_key=False)
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.tournament_id'))
    chess_player_id: Mapped[int] = mapped_column(ForeignKey('chess_players.chess_player_id'))
    place: Mapped[int] = mapped_column(nullable=False)