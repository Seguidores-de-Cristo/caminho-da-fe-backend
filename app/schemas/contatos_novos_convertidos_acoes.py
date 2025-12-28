from pydantic import BaseModel
from typing import Optional


class ContatoNovosConvertidosAcoesBase(BaseModel):
    contato_novo_convertido_id: int
    convite_culto_igreja: bool
    convite_culto_lar: bool
    convite_escola_dominicial: bool
    convite_reuniao_discipulado: bool
    teleoracao: bool
    outros_especificar: bool
    especificacao_outros: Optional[str] = None

    convite_culto_igreja_resposta: bool
    convite_culto_lar_resposta: bool
    convite_escola_dominicial_resposta: bool
    convite_reuniao_discipulado_resposta: bool
    outros_especificar_resposta: bool
    especificacao_outros_resposta: Optional[str]

    manter_contato: bool
    motivo_nao_manter_contato: Optional[str] = None
    cadidato_abandonou_discipulado: bool
    motivo_abandono_discipulado: Optional[str] = None

    agendar_proximo_contato_data: Optional[str] = None
    agendar_proximo_contato_hora: Optional[str] = None

    # Após finalização do discipulado
    candidato_preparado_batismo: bool
    data_batismo: Optional[str] = None

    candidato_esta_em_duvidas_batismo: bool
    motivo_duvidas_batismo: Optional[str] = None

    candidato_desistiu_batismo: bool
    motivo_desistencia_batismo: Optional[str] = None




class ContatoNovosConvertidosAcoesCreate(ContatoNovosConvertidosAcoesBase):
    pass


class ContatoNovosConvertidosAcoesUpdate(BaseModel):
    """Modelo para atualização — todos os campos opcionais."""
    contato_novo_convertido_id: int | None = None
    convite_culto_igreja: bool | None = None
    convite_culto_lar: bool | None = None
    convite_escola_dominicial: bool | None = None
    convite_reuniao_discipulado: bool | None = None
    teleoracao: bool | None = None
    outros_especificar: bool | None = None
    especificacao_outros: Optional[str] = None

    convite_culto_igreja_resposta: bool | None = None
    convite_culto_lar_resposta: bool | None = None
    convite_escola_dominicial_resposta: bool | None = None
    convite_reuniao_discipulado_resposta: bool | None = None
    outros_especificar_resposta: bool | None = None
    especificacao_outros_resposta: Optional[str] = None

    manter_contato: bool | None = None

    motivo_nao_manter_contato: Optional[str] = None
    cadidato_abandonou_discipulado: bool | None = None
    motivo_abandono_discipulado: Optional[str] = None

    agendar_proximo_contato_data: Optional[str] = None
    agendar_proximo_contato_hora: Optional[str] = None

    # Após finalização do discipulado
    candidato_preparado_batismo: bool | None = None
    data_batismo: Optional[str] = None

    candidato_esta_em_duvidas_batismo: bool | None = None
    motivo_duvidas_batismo: Optional[str] = None

    candidato_desistiu_batismo: bool | None = None
    motivo_desistencia_batismo: Optional[str] = None


class ContatoNovosConvertidosAcoesOut(ContatoNovosConvertidosAcoesBase):
    id: int

    class Config:
        from_attributes = True