import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from app.db.session import Base


class ContatoNovoConvertidoAcoes(Base):
    __tablename__ = "contato_novo_convertido_acoes"

    id = Column(Integer, primary_key=True, index=True)

    contato_novo_convertido_id = Column(
        Integer,
        ForeignKey("contatoNovoConvertido.id", ondelete="CASCADE"),
        nullable=False,
    )

    convite_culto_igreja = Column(Boolean, nullable=False, server_default=sa.false())
    convite_culto_lar = Column(Boolean, nullable=False, server_default=sa.false())
    convite_escola_dominicial = Column(Boolean, nullable=False, server_default=sa.false())
    convite_reuniao_discipulado = Column(Boolean, nullable=False, server_default=sa.false())
    teleoracao = Column(Boolean, nullable=False, server_default=sa.false())

    outros_especificar = Column(Boolean, nullable=False, server_default=sa.false())
    especificacao_outros = Column(String(1000), nullable=True)

    convite_culto_igreja_resposta = Column(Boolean, nullable=False, server_default=sa.false())
    convite_culto_lar_resposta = Column(Boolean, nullable=False, server_default=sa.false())
    convite_escola_dominicial_resposta = Column(Boolean, nullable=False, server_default=sa.false())
    convite_reuniao_discipulado_resposta = Column(Boolean, nullable=False, server_default=sa.false())

    outros_especificar_resposta = Column(Boolean, nullable=False, server_default=sa.false())
    especificacao_outros_resposta = Column(String(1000), nullable=True)

    manter_contato = Column(Boolean, nullable=False, server_default=sa.false())
    motivo_nao_manter_contato = Column(String(1000), nullable=True)

    cadidato_abandonou_discipulado = Column(Boolean, nullable=False, server_default=sa.false())
    motivo_abandono_discipulado = Column(String(1000), nullable=True)

    agendar_proximo_contato_data = Column(Date, nullable=True)
    agendar_proximo_contato_hora = Column(String(8), nullable=True)

    # Após finalização do discipulado
    candidato_preparado_batismo = Column(Boolean, nullable=False, server_default=sa.false())
    data_batismo = Column(Date, nullable=True)

    candidato_esta_em_duvidas_batismo = Column(Boolean, nullable=False, server_default=sa.false())
    motivo_duvidas_batismo = Column(String(1000), nullable=True)

    candidato_desistiu_batismo = Column(Boolean, nullable=False, server_default=sa.false())
    motivo_desistencia_batismo = Column(String(1000), nullable=True)
