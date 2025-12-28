from sqlalchemy.orm import Session
from app.schemas.contatos_novos_convertidos_acoes import ContatoNovosConvertidosAcoesCreate
from app.models.contatos_novos_convertidos_acoes import ContatoNovoConvertidoAcoes


def create_contato_novo_convertido_acoes(
    db: Session,
    nc_in: ContatoNovosConvertidosAcoesCreate
):
    novo = ContatoNovoConvertidoAcoes(
        **nc_in.dict()
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


def list_contatos_novos_convertidos_acoes(db: Session):
    return db.query(ContatoNovoConvertidoAcoes).all()

def get_contato_novo_convertido_acoes(db: Session, nc_id: int):
    return db.query(ContatoNovoConvertidoAcoes).filter(ContatoNovoConvertidoAcoes.id == nc_id).first()

def update_contato_novo_convertido_acoes(
    db: Session,
    nc_db: ContatoNovoConvertidoAcoes,
    nc_in
):
    data = nc_in.dict(exclude_unset=True)

    for field, value in data.items():
        if field in {"id", "contato_novo_convertido_id"}:
            continue
        setattr(nc_db, field, value)

    db.commit()
    db.refresh(nc_db)
    return nc_db
