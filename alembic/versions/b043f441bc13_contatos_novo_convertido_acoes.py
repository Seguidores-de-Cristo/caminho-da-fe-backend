"""contatos novo convertido acoes

Revision ID: b043f441bc13
Revises: 0b17df3c2ecf
Create Date: 2025-12-19 10:11:13.296185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b043f441bc13'
down_revision: Union[str, Sequence[str], None] = '0b17df3c2ecf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('contato_novo_convertido_acoes', sa.Column('convite_culto_igreja_resposta', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('contato_novo_convertido_acoes', sa.Column('convite_culto_lar_resposta', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('contato_novo_convertido_acoes', sa.Column('convite_escola_dominicial_resposta', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('contato_novo_convertido_acoes', sa.Column('convite_reuniao_discipulado_resposta', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('contato_novo_convertido_acoes', sa.Column('outros_especificar_resposta', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('contato_novo_convertido_acoes', sa.Column('especificacao_outros_resposta', sa.String(length=1000), nullable=True))
    op.add_column('contato_novo_convertido_acoes', sa.Column('manter_contato', sa.Boolean(), nullable=False, server_default=sa.false()))

def downgrade() -> None:
    op.drop_column('contato_novo_convertido_acoes', 'convite_culto_igreja_resposta')
    op.drop_column('contato_novo_convertido_acoes', 'convite_culto_lar_resposta')
    op.drop_column('contato_novo_convertido_acoes', 'convite_escola_dominicial_resposta')
    op.drop_column('contato_novo_convertido_acoes', 'convite_reuniao_discipulado_resposta')
    op.drop_column('contato_novo_convertido_acoes', 'outros_especificar_resposta')
    op.drop_column('contato_novo_convertido_acoes', 'especificacao_outros_resposta')
    op.drop_column('contato_novo_convertido_acoes', 'manter_contato')
