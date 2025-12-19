from sqlalchemy.orm import Session
from app.schemas.contatos_novos_convertidos_schema import ContatoNovoConvertidoCreate
from app.models.contatos_novos_convertidos_models import ContatoNovoConvertido


def create_contato_novo_convertido(db: Session, nc_in: ContatoNovoConvertidoCreate):
    novo = ContatoNovoConvertido(
        discipulador_id=nc_in.discipulador_id,
        novo_convertido_id=nc_in.novo_convertido_id,
        sucesso_contato=nc_in.sucesso_contato,
        data_contato=nc_in.data_contato,
        contact_event_id=nc_in.contact_event_id,
        protocolo=nc_in.protocolo,
        hora_protocolo=nc_in.hora_protocolo,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def list_contatos_novos_convertidos(db: Session):
    return db.query(ContatoNovoConvertido).all()

def get_contato_novo_convertido(db: Session, nc_id: int):
    return db.query(ContatoNovoConvertido).filter(ContatoNovoConvertido.id == nc_id).first()

def update_contato_novo_convertido(db: Session, nc_db, nc_in):
    for field, value in nc_in.dict(exclude_unset=True).items():
        setattr(nc_db, field, value)

    db.commit()
    db.refresh(nc_db)
    return nc_db
