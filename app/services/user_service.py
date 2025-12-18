"""Camada de serviços para gerenciar lógica de negócio de usuários."""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.user import (
    create_user,
    get_user,
    get_user_by_email,
    update_user,
)
from app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    ConflictException,
)
from app.crud.user import get_password_hash


class UserService:
    """Serviço centralizado para operações de usuário."""

    @staticmethod
    def criar_usuario(db: Session, user_in: UserCreate) -> User:
        """
        Cria um novo usuário com validações.

        Args:
            db: Sessão do banco
            user_in: Dados do novo usuário

        Returns:
            Usuário criado

        Raises:
            ConflictException: Se email já existe
            ValidationException: Se dados inválidos
        """
        # Validar email único
        existing_user = get_user_by_email(db, user_in.email)
        if existing_user:
            raise ConflictException(
                f"Email '{user_in.email}' já está registrado",
                details={"email": user_in.email},
            )

        # Validar nome (não vazio, tamanho mínimo)
        if not user_in.nome or len(user_in.nome.strip()) < 3:
            raise ValidationException(
                "Nome deve ter pelo menos 3 caracteres",
                details={"nome": user_in.nome},
            )

        # Validar email formato (básico)
        if "@" not in user_in.email or len(user_in.email) < 5:
            raise ValidationException(
                "Email inválido",
                details={"email": user_in.email},
            )

        return create_user(db, user_in)

    @staticmethod
    def obter_usuario(db: Session, user_id: int) -> User:
        """
        Obtém um usuário pelo ID.

        Args:
            db: Sessão do banco
            user_id: ID do usuário

        Returns:
            Usuário encontrado

        Raises:
            ResourceNotFoundException: Se usuário não existe
        """
        user = get_user(db, user_id)
        if not user:
            raise ResourceNotFoundException("Usuário", user_id)
        return user

    @staticmethod
    def atualizar_usuario(
        db: Session, user_id: int, user_in: UserUpdate
    ) -> User:
        """
        Atualiza um usuário.

        Args:
            db: Sessão do banco
            user_id: ID do usuário
            user_in: Dados a atualizar

        Returns:
            Usuário atualizado

        Raises:
            ResourceNotFoundException: Se usuário não existe
            ConflictException: Se novo email já existe
        """
        user = get_user(db, user_id)
        if not user:
            raise ResourceNotFoundException("Usuário", user_id)

        # Se email mudou, validar unicidade
        if user_in.email and user_in.email != user.email:
            existing = get_user_by_email(db, user_in.email)
            if existing:
                raise ConflictException(
                    f"Email '{user_in.email}' já está registrado",
                    details={"email": user_in.email},
                )

        return update_user(db, user, user_in)

    @staticmethod
    def listar_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lista usuários com paginação.

        Args:
            db: Sessão do banco
            skip: Quantidade de registros a pular
            limit: Limite de registros

        Returns:
            Lista de usuários
        """
        return db.query(User).offset(skip).limit(limit).all()
