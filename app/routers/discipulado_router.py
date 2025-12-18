"""Router para endpoints de relacionamento entre discipuladores e convertidos."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.novo_convertido import NovoConvertidoOut
from app.schemas.user import UserOut
from app.services.discipulado_relationship_service import (
    DiscipuladoRelationshipService,
)
from app.services.novo_convertido_service import NovoConvertidoService
from app.exceptions import AppException
from .. import models
from app.routers.auth_router import get_current_user

router = APIRouter(
    prefix="/discipulador",
    tags=["Relacionamento Discipulador-Convertido"],
)


@router.get("/{discipulador_id}/convertidos", response_model=list[NovoConvertidoOut])
def listar_convertidos_por_discipulador(
    discipulador_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Lista todos os novos convertidos de um discipulador."""
    try:
        return NovoConvertidoService.listar_convertidos_por_discipulador(
            db, discipulador_id, skip=skip, limit=limit
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post(
    "/convertidos/{convertido_id}/vincular/{discipulador_id}",
    response_model=NovoConvertidoOut,
)
def vincular_convertido_discipulador(
    convertido_id: int,
    discipulador_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Vincula um novo convertido a um discipulador."""
    try:
        return DiscipuladoRelationshipService.vincular_convertido_discipulador(
            db, convertido_id, discipulador_id
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post(
    "/convertidos/{convertido_id}/desvincular",
    response_model=NovoConvertidoOut,
)
def desvincular_convertido_discipulador(
    convertido_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Remove a vinculação de um convertido com seu discipulador."""
    try:
        return DiscipuladoRelationshipService.desvincular_convertido_discipulador(
            db, convertido_id
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/convertidos/{convertido_id}/discipulador", response_model=UserOut)
def obter_discipulador_convertido(
    convertido_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Obtém o discipulador (user) responsável por um convertido."""
    try:
        return DiscipuladoRelationshipService.obter_discipulador_convertido(
            db, convertido_id
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
