"""add content column to post table

Revision ID: 6a042282ff8f
Revises: 84a5a61bdb53
Create Date: 2025-07-01 14:43:37.215759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a042282ff8f'
down_revision: Union[str, Sequence[str], None] = '84a5a61bdb53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
