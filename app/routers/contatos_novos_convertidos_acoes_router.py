from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contatos_novos_convertidos_acoes import (
    ContatoNovosConvertidosAcoesCreate,
    ContatoNovosConvertidosAcoesOut,
)
from app.services.contatos_novos_convertidos_acoes_services import (
    ContatosNovosConvertidosAcoesService,
)
from .. import models
from app.routers.auth_router import get_current_user

router = APIRouter(
    prefix="/contatos-novos-convertidos-acoes",
    tags=["Ações dos Contatos Novos Convertidos"],
)

@router.post("/", response_model=ContatoNovosConvertidosAcoesOut)
def criar_acao_contato(
    acao_in: ContatoNovosConvertidosAcoesCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        service = ContatosNovosConvertidosAcoesService()
        acao = service.criar_acao_contato_novo_convertido(db, acao_in)
        return acao
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/contato/{contato_id}", response_model=list[ContatoNovosConvertidosAcoesOut])
def listar_acoes_contato(
    contato_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        service = ContatosNovosConvertidosAcoesService()
        return service.listar_acoes_por_contato(db, contato_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{acao_id}", response_model=ContatoNovosConvertidosAcoesOut)
def atualizar_acao_contato(
    acao_id: int,
    acao_in: ContatoNovosConvertidosAcoesCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        service = ContatosNovosConvertidosAcoesService()
        acao = service.atualizar_contato_novo_convertido_acoes(db, acao_id, acao_in)
        return acao
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/{acao_id}", response_model=ContatoNovosConvertidosAcoesOut)
def obter_acao_contato(
    acao_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        service = ContatosNovosConvertidosAcoesService()
        return service.obter_contato_novo_convertido_acoes(db, acao_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[ContatoNovosConvertidosAcoesOut])
def listar_acoes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    service = ContatosNovosConvertidosAcoesService()
    return service.listar_contatos_novos_convertidos_acoes(db)
