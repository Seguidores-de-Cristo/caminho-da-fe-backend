# importa modelos para que Alembic possa detectá-los durante autogenerate
from .user import User  # noqa: F401
from .contatos_novos_convertidos_acoes import ContatoNovoConvertidoAcoes
from .contatos_novos_convertidos_models import ContatoNovoConvertido
from .novo_convertido import NovoConvertido