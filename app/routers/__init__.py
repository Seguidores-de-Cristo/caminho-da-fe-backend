"""Inicialização dos routers."""

from app.routers.users_router import router as users_router
from app.routers.novos_convertidos_router import router as novos_convertidos_router
from app.routers.discipulado_router import router as discipulado_router
from app.routers.cep_router import router as cep_router

__all__ = [
    "users_router",
    "novos_convertidos_router",
    "discipulado_router",
    "cep_router",
]
