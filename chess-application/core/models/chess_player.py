from more_itertools.recipes import unique
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from .base import Base

class ChessPlayer(Base):
    __tablename__ = 'chess_players'

    chess_player_id: Mapped[int] = mapped_column(unique=True, primary_key=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    world_rank: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)

