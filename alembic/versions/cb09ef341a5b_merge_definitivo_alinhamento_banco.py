"""merge definitivo alinhamento banco

Revision ID: cb09ef341a5b
Revises: a0e38abc4e1a, bf6951f621de
Create Date: 2025-12-27 23:51:45.691708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb09ef341a5b'
down_revision: Union[str, Sequence[str], None] = ('a0e38abc4e1a', 'bf6951f621de')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
