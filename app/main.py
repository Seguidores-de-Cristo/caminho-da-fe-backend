from fastapi import FastAPI
from app.db.session import init_db
from app.routers import (
    users_router,
    novos_convertidos_router,
    discipulado_router,
    cep_router,
    contatos_novos_convertidos_router,
    auth_router,
)

app = FastAPI(title="Caminho da Fé API")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(users_router)
app.include_router(novos_convertidos_router)
app.include_router(discipulado_router)
app.include_router(cep_router)
app.include_router(contatos_novos_convertidos_router)
app.include_router(auth_router)