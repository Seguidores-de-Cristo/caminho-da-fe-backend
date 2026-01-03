"""Add valor padrao 'pendente' coluna status_contato

Revision ID: 1a38ad7c53c2
Revises: 6a1ad07901c1
Create Date: 2025-12-30 23:16:15.910545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a38ad7c53c2'
down_revision: Union[str, Sequence[str], None] = '6a1ad07901c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('contatoNovoConvertido', 'status_contato', server_default=sa.text("'pendente'"))


def downgrade() -> None:
    op.alter_column('contatoNovoConvertido', 'status_contato', server_default=None)
