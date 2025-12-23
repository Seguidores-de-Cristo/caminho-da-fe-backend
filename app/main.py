from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.db.session import init_db
from app.core import config
from app.routers import (
    users_router,
    novos_convertidos_router,
    discipulado_router,
    cep_router,
    contatos_novos_convertidos_router,
    contatos_novos_convertidos_acoes_router,
    auth_router,

)


app = FastAPI(title="Caminho da Fé API")

# Register CORS middleware if configured
if getattr(config, "CORS_ORIGINS", None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(users_router)
app.include_router(novos_convertidos_router)
app.include_router(discipulado_router)
app.include_router(cep_router)
app.include_router(contatos_novos_convertidos_router)
app.include_router(auth_router)
app.include_router(contatos_novos_convertidos_acoes_router)