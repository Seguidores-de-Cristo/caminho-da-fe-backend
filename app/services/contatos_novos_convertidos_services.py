from sqlalchemy.orm import Session
from app.models.contatos_novos_convertidos_models import ContatoNovoConvertido
from app.schemas.contatos_novos_convertidos_schema import (
    ContatoNovoConvertidoCreate,
    ContatoNovoConvertidoUpdate,
)

from app.crud.contatos_novos_convertidos_crud import create_contato_novo_convertido


class ContatosNovosConvertidosService:
    """ Serviços relacionados aos contatos de novos convertidos. 
    """

    
    def criar_contato_novo_convertido(self, db: Session, contato_in: ContatoNovoConvertidoCreate) -> ContatoNovoConvertido:
        """
        Cria um novo contato de convertido.

        Args:
            db: Sessão do banco
            contato_in: Dados do contato a ser criado

        Returns:
            Contato de novo convertido criado
        """

        return create_contato_novo_convertido(db, contato_in)

        
