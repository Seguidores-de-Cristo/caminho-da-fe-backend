from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bf6951f621de'
down_revision: Union[str, Sequence[str], None] = 'b043f441bc13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove coluna duplicada
    op.drop_column('contatoNovoConvertido', 'contact_event_id')


def downgrade() -> None:
    op.add_column('contatoNovoConvertido', sa.Column('contact_event_id', sa.String(length=26), nullable=True))