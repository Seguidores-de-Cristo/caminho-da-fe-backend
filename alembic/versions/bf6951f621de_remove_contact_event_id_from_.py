from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bf6951f621de'
down_revision: Union[str, Sequence[str], None] = 'b043f441bc13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove coluna duplicada
    op.drop_column('contatoNovoConvertido', 'contact_event_id')


def downgrade() -> None:
    # Downgrade não suportado: coluna era duplicada e removida de forma definitiva
    raise NotImplementedError(
        "Downgrade não suportado: coluna contact_event_id foi removida por ser duplicada de 'protocolo'."
    )
