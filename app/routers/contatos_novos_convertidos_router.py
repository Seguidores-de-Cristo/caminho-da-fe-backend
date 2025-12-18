from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contatos_novos_convertidos_schema import (
    ContatoNovoConvertidoCreate,
    ContatoNovoConvertidoOut,
)
from app.services.contatos_novos_convertidos_services import (
    ContatosNovosConvertidosService,
)
from .. import models
from app.routers.auth_router import get_current_user

router = APIRouter(
    prefix="/contatos-novos-convertidos",
    tags=["Contatos Novos Convertidos"],
)

@router.post("/", response_model=ContatoNovoConvertidoOut)
def criar_contato(
    contato_in: ContatoNovoConvertidoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        service = ContatosNovosConvertidosService()
        contato = service.criar_contato_novo_convertido(db, contato_in)
        return contato
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
