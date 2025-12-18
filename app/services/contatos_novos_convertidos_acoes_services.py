from sqlalchemy.orm import Session
from app.models.contatos_novos_convertidos_acoes import ContatoNovoConvertidoAcoes
from app.schemas.contatos_novos_convertidos_acoes import (
    ContatoNovosConvertidosAcoesCreate,
    ContatoNovosConvertidosAcoesUpdate,    
)

from app.crud.contatos_novos_convertidos_acoes import create_contato_novo_convertido_acoes



class ContatosNovosConvertidosAcoesService:
    """ Serviços relacionados às ações dos contatos de novos convertidos. 
    """

    
    def criar_acao_contato_novo_convertido(self, db: Session, contato_acoes_in: ContatoNovosConvertidosAcoesCreate) -> ContatoNovoConvertidoAcoes:
        """
        Cria um novo registro de ações para o contato de convertido.

        Args:
            db: Sessão do banco
            contato_acoes_in: Dados das ações do contato a ser criado

        Returns:
            Registro de ações do contato de novo convertido criado
        """

        return create_contato_novo_convertido_acoes(db, contato_acoes_in)
    

    def atualizar_contato_novo_convertido_acoes(
        self,
        db: Session,
        acao_id: int,
        contato_acoes_in: ContatoNovosConvertidosAcoesUpdate
    ) -> ContatoNovoConvertidoAcoes:

        contato_acoes_db = db.query(ContatoNovoConvertidoAcoes).filter(
            ContatoNovoConvertidoAcoes.id == acao_id
        ).first()

        if not contato_acoes_db:
            raise ValueError("Ação não encontrada")

        for field, value in contato_acoes_in.dict(exclude_unset=True).items():
            setattr(contato_acoes_db, field, value)

        db.commit()
        db.refresh(contato_acoes_db)
        return contato_acoes_db

    
    def obter_contato_novo_convertido_acoes(self, db: Session, contato_acoes_id: int) -> ContatoNovoConvertidoAcoes:
        """
        Obtém um registro de ações para o contato de convertido pelo ID.
        """

        contato_acoes = db.query(ContatoNovoConvertidoAcoes).filter(
            ContatoNovoConvertidoAcoes.id == contato_acoes_id
        ).first()

        if not contato_acoes:
            raise ValueError("Ação do contato não encontrada")

        return contato_acoes

    def listar_contatos_novos_convertidos_acoes(self, db: Session) -> list[ContatoNovoConvertidoAcoes]:
        """
        Lista todos os registros de ações para contatos de novos convertidos.
        """

        return (
            db.query(ContatoNovoConvertidoAcoes)
            .order_by(ContatoNovoConvertidoAcoes.id.desc())
            .all()
        )
    
    def listar_acoes_por_contato(self, db: Session, contato_novo_convertido_id: int) -> list[ContatoNovoConvertidoAcoes]:
        """
        Lista todas as ações de um contato de novo convertido.
        """

        return (
            db.query(ContatoNovoConvertidoAcoes)
            .filter(
                ContatoNovoConvertidoAcoes.contato_novo_convertido_id
                == contato_novo_convertido_id
            )
            .order_by(ContatoNovoConvertidoAcoes.id.desc())
            .all()
        )


    
    def update_contato_novo_convertido_acoes(self, db: Session, contato_acoes_db: ContatoNovoConvertidoAcoes, contato_acoes_in: ContatoNovosConvertidosAcoesUpdate) -> ContatoNovoConvertidoAcoes:
        """
        Atualiza um registro de ações para o contato de convertido.

        Args:
            db: Sessão do banco
            contato_acoes_db: Instância existente do contato de ações a ser atualizada
            contato_acoes_in: Dados atualizados das ações do contato

        Returns:
            Registro de ações do contato de novo convertido atualizado
        """

        for field, value in contato_acoes_in.dict(exclude_unset=True).items():
            setattr(contato_acoes_db, field, value)

        db.commit()
        db.refresh(contato_acoes_db)
        return contato_acoes_db