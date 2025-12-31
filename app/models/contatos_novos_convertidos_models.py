import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from app.db.session import Base


class ContatoNovoConvertido(Base):
    __tablename__ = "contatoNovoConvertido"

    id = Column(Integer, primary_key=True, index=True)
    discipulador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    novo_convertido_id = Column(Integer, ForeignKey("novos_convertidos.id"), nullable=False)
    sucesso_contato = Column(Boolean, nullable=False)
    data_contato = Column(Date, nullable=False, server_default=sa.text('CURRENT_DATE'))

    protocolo = Column(String(26), nullable=False, unique=True, index=True)
    hora_protocolo = Column(String(8), nullable=False)

    status_contato = Column(String(50), nullable=False, server_default=sa.text("'pendente'"))