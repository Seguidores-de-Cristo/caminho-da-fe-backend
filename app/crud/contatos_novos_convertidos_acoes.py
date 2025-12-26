from sqlalchemy.orm import Session
from app.schemas.contatos_novos_convertidos_acoes import ContatoNovosConvertidosAcoesCreate
from app.models.contatos_novos_convertidos_acoes import ContatoNovoConvertidoAcoes


def create_contato_novo_convertido_acoes(db: Session, nc_in: ContatoNovosConvertidosAcoesCreate):
    novo = ContatoNovoConvertidoAcoes(
        contato_novo_convertido_id=nc_in.contato_novo_convertido_id,
        convite_culto_igreja=nc_in.convite_culto_igreja,
        convite_culto_lar=nc_in.convite_culto_lar,
        convite_escola_dominicial=nc_in.convite_escola_dominicial,
        convite_reuniao_discipulado=nc_in.convite_reuniao_discipulado,
        teleoracao=nc_in.teleoracao,
        outros_especificar=nc_in.outros_especificar,
        especificacao_outros=nc_in.especificacao_outros,

        convite_culto_igreja_resposta=nc_in.convite_culto_igreja_resposta,
        convite_culto_lar_resposta=nc_in.convite_culto_lar_resposta,
        convite_escola_dominicial_resposta=nc_in.convite_escola_dominicial_resposta,
        convite_reuniao_discipulado_resposta=nc_in.convite_reuniao_discipulado_resposta,
        outros_especificar_resposta=nc_in.outros_especificar_resposta,
        especificacao_outros_resposta=nc_in.especificacao_outros_resposta,
        
        manter_contato=nc_in.manter_contato,
        motivo_nao_manter_contato=nc_in.motivo_nao_manter_contato,
        cadidato_abandonou_discipulado=nc_in.cadidato_abandonou_discipulado,
        motivo_abandono_discipulado=nc_in.motivo_abandono_discipulado,
        agendar_proximo_contato_data=nc_in.agendar_proximo_contato_data,
        agendar_proximo_contato_hora=nc_in.agendar_proximo_contato_hora,
        candidato_preparado_batismo=nc_in.candidato_preparado_batismo,
        data_batismo=nc_in.data_batismo,
        candidato_esta_em_duvidas_batismo=nc_in.candidato_esta_em_duvidas_batismo,
        motivo_duvidas_batismo=nc_in.motivo_duvidas_batismo,
        candidato_desistiu_batismo=nc_in.candidato_desistiu_batismo,
        motivo_desistencia_batismo=nc_in.motivo_desistencia_batismo,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def list_contatos_novos_convertidos_acoes(db: Session):
    return db.query(ContatoNovoConvertidoAcoes).all()

def get_contato_novo_convertido_acoes(db: Session, nc_id: int):
    return db.query(ContatoNovoConvertidoAcoes).filter(ContatoNovoConvertidoAcoes.id == nc_id).first()

def update_contato_novo_convertido_acoes(db: Session, nc_db, nc_in):
    for field, value in nc_in.dict(exclude_unset=True).items():
        setattr(nc_db, field, value)

    db.commit()
    db.refresh(nc_db)
    return nc_db