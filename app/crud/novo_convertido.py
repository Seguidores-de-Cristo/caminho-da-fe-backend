from sqlalchemy.orm import Session
from app.models.novo_convertido import NovoConvertido
from app.schemas.novo_convertido import NovoConvertidoCreate
from datetime import date

def create_novo_convertido(db: Session, nc_in: NovoConvertidoCreate):
    novo = NovoConvertido(
        nome=nc_in.nome,
        telefone=nc_in.telefone,
        cep=nc_in.cep,
        endereco=nc_in.endereco,
        complemento=nc_in.complemento,
        bairro=nc_in.bairro,
        cidade=nc_in.cidade,
        uf=nc_in.uf,
        data_nascimento=nc_in.data_nascimento,
        data_cadastro = date.today(),
        idade=nc_in.idade,
        data_conversao=nc_in.data_conversao,
        discipulador_id=nc_in.discipulador_id,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def list_novos_convertidos(db: Session):
    return db.query(NovoConvertido).all()

def get_novo_convertido(db: Session, nc_id: int):
    return db.query(NovoConvertido).filter(NovoConvertido.id == nc_id).first()

def update_novo_convertido(db: Session, nc_db, nc_in):
    for field, value in nc_in.dict(exclude_unset=True).items():
        setattr(nc_db, field, value)

    db.commit()
    db.refresh(nc_db)
    return nc_db
