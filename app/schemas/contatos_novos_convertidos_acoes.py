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


class ContatoNovosConvertidosAcoesOut(ContatoNovosConvertidosAcoesBase):
    id: int

    class Config:
        from_attributes = True





