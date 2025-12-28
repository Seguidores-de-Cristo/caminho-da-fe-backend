from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

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
        
        # Converte datas para string antes de retornar
        resultado = acao.__dict__.copy()
        if resultado.get("agendar_proximo_contato_data") and isinstance(resultado["agendar_proximo_contato_data"], date):
            resultado["agendar_proximo_contato_data"] = resultado["agendar_proximo_contato_data"].isoformat()
        if resultado.get("data_batismo") and isinstance(resultado["data_batismo"], date):
            resultado["data_batismo"] = resultado["data_batismo"].isoformat()
        
        return resultado
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
    acoes = service.listar_contatos_novos_convertidos_acoes(db)

    # Converte datas para string para cada item da lista
    resultado = []
    for acao in acoes:
        item = acao.__dict__.copy()
        if item.get("agendar_proximo_contato_data") and isinstance(item["agendar_proximo_contato_data"], date):
            item["agendar_proximo_contato_data"] = item["agendar_proximo_contato_data"].isoformat()
        if item.get("data_batismo") and isinstance(item["data_batismo"], date):
            item["data_batismo"] = item["data_batismo"].isoformat()
        resultado.append(item)

    return resultado

