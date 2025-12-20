"""contatos novo convertido acoes

Revision ID: b043f441bc13
Revises: 0b17df3c2ecf
Create Date: 2025-12-19 10:11:13.296185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b043f441bc13'
down_revision: Union[str, Sequence[str], None] = '0b17df3c2ecf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contato_novo_convertido_acoes",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),

        sa.Column(
            "contato_novo_convertido_id",
            sa.Integer(),
            sa.ForeignKey("contatoNovoConvertido.id"),
            nullable=False,
        ),

        sa.Column("convite_culto_igreja", sa.Boolean(), nullable=False),
        sa.Column("convite_culto_lar", sa.Boolean(), nullable=False),
        sa.Column("convite_escola_dominicial", sa.Boolean(), nullable=False),
        sa.Column("convite_reuniao_discipulado", sa.Boolean(), nullable=False),
        sa.Column("teleoracao", sa.Boolean(), nullable=False),

        sa.Column("outros_especificar", sa.Boolean(), nullable=False),
        sa.Column("especificacao_outros", sa.String(length=1000), nullable=True),

        sa.Column("convite_culto_igreja_resposta", sa.Boolean(), nullable=False),
        sa.Column("convite_culto_lar_resposta", sa.Boolean(), nullable=False),
        sa.Column("convite_escola_dominicial_resposta", sa.Boolean(), nullable=False),
        sa.Column("convite_reuniao_discipulado_resposta", sa.Boolean(), nullable=False),

        sa.Column("outros_especificar_resposta", sa.Boolean(), nullable=False),
        sa.Column("especificacao_outros_resposta", sa.String(length=1000), nullable=True),

        sa.Column("manter_contato", sa.Boolean(), nullable=False),

        mysql_engine="InnoDB",
        mysql_default_charset="utf8mb4",
    )

    op.create_index(
        "ix_contato_novo_convertido_acoes_id",
        "contato_novo_convertido_acoes",
        ["id"],
    )



def downgrade() -> None:
    op.drop_table("contato_novo_convertido_acoes")

