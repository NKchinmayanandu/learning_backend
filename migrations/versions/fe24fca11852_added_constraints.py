"""added constraints

Revision ID: fe24fca11852
Revises: 587455647eee
Create Date: 2026-04-25 13:16:11.168978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe24fca11852'
down_revision: Union[str, Sequence[str], None] = '587455647eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


import sqlalchemy as sa
from alembic import op


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'foods',
        'name',
        existing_type=sa.VARCHAR(),
        nullable=False
    )

    op.alter_column(
        'foods',
        'price',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
    )

    op.alter_column(
        'restaurants',
        'name',
        existing_type=sa.VARCHAR(),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'restaurants',
        'name',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.alter_column(
        'foods',
        'price',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
    )

    op.alter_column(
        'foods',
        'name',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

