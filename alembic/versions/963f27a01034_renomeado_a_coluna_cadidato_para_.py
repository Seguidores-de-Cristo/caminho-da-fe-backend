"""Renomeado a coluna cadidato para candidato

Revision ID: 963f27a01034
Revises: 1a38ad7c53c2
Create Date: 2026-01-03 14:27:18.290779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '963f27a01034'
down_revision: Union[str, Sequence[str], None] = '1a38ad7c53c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'contato_novo_convertido_acoes',
        'cadidato_abandonou_discipulado',
        new_column_name='candidato_abandonou_discipulado',
        existing_type=sa.Boolean(),
        existing_nullable=False,
        existing_server_default=sa.text('false')
    )


def downgrade():
    op.alter_column(
        'contato_novo_convertido_acoes',
        'candidato_abandonou_discipulado',
        new_column_name='cadidato_abandonou_discipulado',
        existing_type=sa.Boolean(),
        existing_nullable=False,
        existing_server_default=sa.text('false')
    )
