"""
Exemplo de integração dos novos routers no main.py

Para usar a nova arquitetura, substitua o conteúdo de main.py por:

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.db.session import get_db, init_db
from app.routers import (
    users_router,
    novos_convertidos_router,
    discipulado_router,
)
from app.exceptions import AppException
from fastapi.responses import JSONResponse
from app import models  # garante que modelos sejam carregados

app = FastAPI(
    title="Caminho da Fé API",
    description="API para gerenciar discipuladores (usuários) e novos convertidos",
    version="2.0.0",
)


@app.on_event("startup")
def on_startup():
    init_db()


# Handlers de exceções customizadas
@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "details": exc.details,
        },
    )


# Incluir routers
app.include_router(users_router)
app.include_router(novos_convertidos_router)
app.include_router(discipulado_router)


# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "message": "Bem-vindo à API Caminho da Fé",
        "docs": "/docs",
        "redoc": "/redoc",
    }
"""

