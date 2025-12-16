"""Camada de serviços para gerenciar relacionamentos entre discipuladores e convertidos."""

from sqlalchemy.orm import Session
from typing import List
from app.models.novo_convertido import NovoConvertido
from app.models.user import User
from app.crud.user import get_user
from app.crud.novo_convertido import get_novo_convertido
from app.exceptions import ResourceNotFoundException, ValidationException


class DiscipuladoRelationshipService:
    """Serviço para gerenciar relacionamento entre discipulador e convertidos."""

    @staticmethod
    def vincular_convertido_discipulador(
        db: Session, convertido_id: int, discipulador_id: int
    ) -> NovoConvertido:
        """
        Vincula um novo convertido a um discipulador.

        Args:
            db: Sessão do banco
            convertido_id: ID do novo convertido
            discipulador_id: ID do discipulador (user)

        Returns:
            Novo convertido atualizado

        Raises:
            ResourceNotFoundException: Se convertido ou discipulador não existe
        """
        # Validar que o convertido existe
        convertido = get_novo_convertido(db, convertido_id)
        if not convertido:
            raise ResourceNotFoundException("Novo Convertido", convertido_id)

        # Validar que o discipulador existe
        discipulador = get_user(db, discipulador_id)
        if not discipulador:
            raise ResourceNotFoundException("Discipulador", discipulador_id)

        # Vincular
        convertido.discipulador_id = discipulador_id
        db.commit()
        db.refresh(convertido)
        return convertido

    @staticmethod
    def desvincular_convertido_discipulador(
        db: Session, convertido_id: int
    ) -> NovoConvertido:
        """
        Remove a vinculação de um convertido com seu discipulador.

        Args:
            db: Sessão do banco
            convertido_id: ID do novo convertido

        Returns:
            Novo convertido atualizado

        Raises:
            ResourceNotFoundException: Se convertido não existe
        """
        convertido = get_novo_convertido(db, convertido_id)
        if not convertido:
            raise ResourceNotFoundException("Novo Convertido", convertido_id)

        convertido.discipulador_id = None
        db.commit()
        db.refresh(convertido)
        return convertido

    @staticmethod
    def obter_discipulador_convertido(
        db: Session, convertido_id: int
    ) -> User:
        """
        Obtém o discipulador (user) responsável por um convertido.

        Args:
            db: Sessão do banco
            convertido_id: ID do novo convertido

        Returns:
            Usuário discipulador

        Raises:
            ResourceNotFoundException: Se convertido não existe ou não tem discipulador
        """
        convertido = get_novo_convertido(db, convertido_id)
        if not convertido:
            raise ResourceNotFoundException("Novo Convertido", convertido_id)

        if not convertido.discipulador_id:
            raise ValidationException(
                "Este convertido não possui um discipulador vinculado",
                details={"convertido_id": convertido_id},
            )

        discipulador = get_user(db, convertido.discipulador_id)
        if not discipulador:
            raise ResourceNotFoundException(
                "Discipulador", convertido.discipulador_id
            )

        return discipulador

    @staticmethod
    def contar_convertidos_discipulador(
        db: Session, discipulador_id: int
    ) -> int:
        """
        Conta quantos novos convertidos estão vinculados a um discipulador.

        Args:
            db: Sessão do banco
            discipulador_id: ID do discipulador

        Returns:
            Número de convertidos

        Raises:
            ResourceNotFoundException: Se discipulador não existe
        """
        # Validar que o discipulador existe
        discipulador = get_user(db, discipulador_id)
        if not discipulador:
            raise ResourceNotFoundException("Discipulador", discipulador_id)

        count = (
            db.query(NovoConvertido)
            .filter(NovoConvertido.discipulador_id == discipulador_id)
            .count()
        )
        return count
