"""Router para endpoints de usuários (discipuladores)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import UserService
from app.services.discipulado_relationship_service import (
    DiscipuladoRelationshipService,
)
from app.exceptions import (
    AppException,
    ResourceNotFoundException,
    ConflictException,
)

router = APIRouter(prefix="/users", tags=["Usuários / Discipuladores"])


@router.post("/", response_model=UserOut, status_code=201)
def criar_usuario(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """Cria um novo usuário (discipulador)."""
    try:
        return UserService.criar_usuario(db, user_in)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/{user_id}", response_model=UserOut)
def obter_usuario(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Obtém um usuário pelo ID."""
    try:
        return UserService.obter_usuario(db, user_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/", response_model=list[UserOut])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Lista usuários com paginação."""
    return UserService.listar_usuarios(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserOut)
def atualizar_usuario(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza um usuário."""
    try:
        return UserService.atualizar_usuario(db, user_id, user_in)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/{user_id}/convertidos-count", response_model=dict)
def contar_convertidos_discipulador(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Conta quantos novos convertidos estão vinculados a um discipulador."""
    try:
        count = DiscipuladoRelationshipService.contar_convertidos_discipulador(
            db, user_id
        )
        return {"discipulador_id": user_id, "total_convertidos": count}
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
