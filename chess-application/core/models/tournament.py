from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from .base import Base
from sqlalchemy import Column, Integer, String

class Tournament(Base):
    __tablename__ = 'tournaments'

    tournament_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tournament_name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    qualification: Mapped[str] = mapped_column(nullable=False)