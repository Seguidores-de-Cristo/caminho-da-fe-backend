import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from app.db.session import Base


class ContatoNovoConvertidoAcoes(Base):
    __tablename__ = "contato_novo_convertido_acoes"

    id = Column(Integer, primary_key=True, index=True)
    contato_novo_convertido_id = Column(Integer, ForeignKey("contatoNovoConvertido.id"), nullable=False)
    convite_culto_igreja = Column(Boolean, nullable=False)
    convite_culto_lar = Column(Boolean, nullable=False)
    convite_escola_dominicial = Column(Boolean, nullable=False)
    convite_reuniao_discipulado = Column(Boolean, nullable=False)
    teleoracao = Column(Boolean, nullable=False)
    
    outros_especificar = Column(Boolean, nullable=False)
    especificacao_outros = Column(String(1000), nullable=True)