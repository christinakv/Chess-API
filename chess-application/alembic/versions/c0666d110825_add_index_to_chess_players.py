"""add index to chess_players

Revision ID: c0666d110825
Revises: 3872b9437f77
Create Date: 2025-01-02 00:16:06.790853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0666d110825'
down_revision: Union[str, None] = '3872b9437f77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_chess_players_rating', 'chess_players', ['rating'])


def downgrade() -> None:
    op.drop_index('ix_chess_players_rating')
