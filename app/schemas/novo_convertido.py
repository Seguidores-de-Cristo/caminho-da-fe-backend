from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class NovoConvertidoBase(BaseModel):
    nome: str
    telefone: str
    cep: str
    endereco: str
    complemento: str | None = None
    cidade: str
    bairro: str
    uf: str
    data_nascimento: date
    idade: int | None = None
    data_conversao: date
    discipulador_id: int


class NovoConvertidoCreate(NovoConvertidoBase):
    pass


class NovoConvertidoUpdate(BaseModel):
    """Modelo para atualização — todos os campos opcionais."""
    nome: str | None = None
    telefone: str | None = None
    cep: str | None = None
    endereco: str | None = None
    complemento: str | None = None
    cidade: str | None = None
    bairro: str | None = None
    uf: str | None = None
    data_nascimento: date | None = None
    idade: int | None = None
    data_conversao: date | None = None
    discipulador_id: int | None = None


class NovoConvertidoOut(NovoConvertidoBase):
    id: int
    data_cadastro: date

    class Config:
        from_attributes = True


class NovoConvertidoOutComDiscipulador(NovoConvertidoOut):
    """Schema com dados resumidos do discipulador."""

    class DiscipuladorInfo(BaseModel):
        id: int
        nome: str
        email: str

        class Config:
            from_attributes = True

    discipulador: Optional[DiscipuladorInfo] = None

    class Config:
        from_attributes = True


class NovoConvertidoStats(BaseModel):
    """Estatísticas de um convertido."""

    id: int
    nome: str
    data_cadastro: date
    dias_desde_cadastro: int = Field(
        ..., description="Dias desde a data de cadastro"
    )
    idade: Optional[int] = None

    class Config:
        from_attributes = True
