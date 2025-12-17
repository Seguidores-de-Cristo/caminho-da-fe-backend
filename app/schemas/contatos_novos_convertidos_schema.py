from pydantic import BaseModel
from datetime import date
from typing import Optional


class ContatoNovoConvertidoBase(BaseModel):
    discipulador_id: int
    novo_convertido_id: int
    sucesso_contato: bool
    data_contato: date
    contact_event_id: str
    protocolo: str
    hora_protocolo: str


class ContatoNovoConvertidoCreate(ContatoNovoConvertidoBase):
    pass


class ContatoNovoConvertidoUpdate(BaseModel):
    """Modelo para atualização — todos os campos opcionais."""
    discipulador_id: int | None = None
    novo_convertido_id: int | None = None
    sucesso_contato: bool | None = None
    data_contato: date | None = None
    contact_event_id: str | None = None
    protocolo: str | None = None
    hora_protocolo: str | None = None


class ContatoNovoConvertidoOut(ContatoNovoConvertidoBase):
    id: int

    class Config:
        from_attributes = True


class ContatoNovoConvertidoOutComDiscipulador(ContatoNovoConvertidoOut):
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


