"""Router para endpoints de novos convertidos."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.novo_convertido import (
    NovoConvertidoCreate,
    NovoConvertidoUpdate,
    NovoConvertidoOut,
)
from app.services.novo_convertido_service import NovoConvertidoService
from app.exceptions import AppException

router = APIRouter(prefix="/novos-convertidos", tags=["Novos Convertidos"])


@router.post("/", response_model=NovoConvertidoOut, status_code=201)
def criar_novo_convertido(
    convertido_in: NovoConvertidoCreate,
    db: Session = Depends(get_db),
):
    """Cria um novo convertido."""
    try:
        return NovoConvertidoService.criar_convertido(db, convertido_in)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/com-cep/", response_model=NovoConvertidoOut, status_code=201)
def criar_novo_convertido_com_cep(
    convertido_in: NovoConvertidoCreate,
    cep: str = Query(..., description="CEP para preenchimento automático"),
    db: Session = Depends(get_db),
):
    """Cria um novo convertido preenchendo endereço automaticamente via CEP."""
    try:
        return NovoConvertidoService.criar_convertido_com_cep(
            db, convertido_in, cep=cep
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/{convertido_id}", response_model=NovoConvertidoOut)
def obter_novo_convertido(
    convertido_id: int,
    db: Session = Depends(get_db),
):
    """Obtém um novo convertido pelo ID."""
    try:
        return NovoConvertidoService.obter_convertido(db, convertido_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/", response_model=list[NovoConvertidoOut])
def listar_novos_convertidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Lista novos convertidos com paginação."""
    return NovoConvertidoService.listar_convertidos(db, skip=skip, limit=limit)


@router.put("/{convertido_id}", response_model=NovoConvertidoOut)
def atualizar_novo_convertido(
    convertido_id: int,
    convertido_in: NovoConvertidoUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza um novo convertido."""
    try:
        return NovoConvertidoService.atualizar_convertido(
            db, convertido_id, convertido_in
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
