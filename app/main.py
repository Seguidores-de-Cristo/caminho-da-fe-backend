from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import requests
from .db.session import get_db, init_db
from . import models
from .schemas import user as user_schema
from .crud import user as crud_user
from .crud import novo_convertido as crud_nc
from .schemas import novo_convertido as nc_schema

app = FastAPI(title="Caminho da Fé API")

@app.on_event("startup")
def on_startup():
    init_db()

#### usuários e discipuladores ####

@app.post("/users/", response_model=user_schema.UserOut)
def create_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud_user.create_user(db, user_in)

@app.get("/users/{user_id}", response_model=user_schema.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user


@app.put("/users/{user_id}", response_model=user_schema.UserOut)
def update_user_route(user_id: int, user_in: user_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return crud_user.update_user(db, db_user, user_in)



# ========== ROTAS NOVO CONVERTIDO ==========

@app.post("/novos-convertidos/", response_model=nc_schema.NovoConvertidoOut)
def create_novo_convertido(dados: dict, db: Session = Depends(get_db)):
    """
    Cria um novo convertido. Se o CEP estiver presente, preenche os campos de endereço automaticamente.
    """
    # Verifica se o discipulador existe
    discipulador = crud_user.get_user(db, dados.get("discipulador_id"))
    if not discipulador:
        raise HTTPException(status_code=400, detail="Não há discipulador")
    
    # Preenche endereço automaticamente se algum campo estiver faltando
    cep = dados.get("cep")
    if cep and (not dados.get("endereco") or not dados.get("bairro") or not dados.get("uf")):
        endereco = buscar_cep(cep)
        dados["endereco"] = dados.get("endereco") or endereco["logradouro"]
        dados["bairro"] = dados.get("bairro") or endereco["bairro"]
        dados["cidade"] = dados.get("cidade") or endereco["cidade"]
        dados["uf"] = dados.get("uf") or endereco["uf"]
        dados["complemento"] = dados.get("complemento") or endereco["complemento"]
    
    # Cria o schema com todos os campos obrigatórios preenchidos
    nc_in = nc_schema.NovoConvertidoCreate(**dados)
    
    # Cria o novo convertido
    return crud_nc.create_novo_convertido(db, nc_in)



# @app.post("/novos-convertidos/", response_model=nc_schema.NovoConvertidoOut)
# def create_novo_convertido(nc_in: nc_schema.NovoConvertidoCreate, db: Session = Depends(get_db)):
#     # Verifica se o discipulador existe
#     discipulador = crud_user.get_user(db, nc_in.discipulador_id)
#     if not discipulador:
#         raise HTTPException(status_code=400, detail="Não há discipulador")

#     return crud_nc.create_novo_convertido(db, nc_in)


@app.get("/novos-convertidos/", response_model=list[nc_schema.NovoConvertidoOut])
def list_novos_convertidos(db: Session = Depends(get_db)):
    return crud_nc.list_novos_convertidos(db)


@app.get("/novos-convertidos/{nc_id}", response_model=nc_schema.NovoConvertidoOut)
def read_novo_convertido(nc_id: int, db: Session = Depends(get_db)):
    nc = crud_nc.get_novo_convertido(db, nc_id)
    if not nc:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")
    return nc

@app.put("/novos-convertidos/{nc_id}", response_model=nc_schema.NovoConvertidoOut)
def update_novo_convertido(nc_id: int, nc_in: nc_schema.NovoConvertidoUpdate, db: Session = Depends(get_db)):
    # Verifica se existe
    nc = crud_nc.get_novo_convertido(db, nc_id)
    if not nc:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")

    # Se o discipulador foi enviado, validar também
    if nc_in.discipulador_id is not None:
        discipulador = crud_user.get_user(db, nc_in.discipulador_id)
        if not discipulador:
            raise HTTPException(status_code=400, detail="Não há discipulador")

    return crud_nc.update_novo_convertido(db, nc, nc_in)



router = APIRouter(tags=["CEP"])

@router.get("/cep/{cep}")
def buscar_cep(cep: str):
    """
    Recebe um CEP e retorna os dados do endereço.
    """
    # Remove qualquer caractere que não seja número
    cep = ''.join(filter(str.isdigit, cep))
    
    if len(cep) != 8:
        raise HTTPException(status_code=400, detail="CEP inválido. Deve ter 8 dígitos.")

    # Consulta a API ViaCEP
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Não foi possível consultar o CEP")
    
    data = response.json()
    
    if "erro" in data:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    
    # Retorna apenas os campos que interessam para NovoConvertido
    endereco = {
        "logradouro": data.get("logradouro", ""),
        "bairro": data.get("bairro", ""),
        "cidade": data.get("localidade", ""),
        "uf": data.get("uf", ""),
        "cep": data.get("cep", ""),
        "complemento": data.get("complemento", "")
    }
    
    return endereco

app.include_router(router)