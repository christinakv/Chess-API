"""add new columns to chess_players

Revision ID: 3872b9437f77
Revises: b34e49f57bdb
Create Date: 2025-01-02 00:15:04.123570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3872b9437f77'
down_revision: Union[str, None] = 'b34e49f57bdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chess_players', sa.Column('email', sa.String(), nullable=True))
    op.add_column('chess_players', sa.Column('phone', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('chess_players', 'email')
    op.drop_column('chess_players', 'phone')
