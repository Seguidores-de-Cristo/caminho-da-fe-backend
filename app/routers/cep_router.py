"""Router para endpoints de CEP."""

from fastapi import APIRouter, HTTPException, Depends
import requests
from .. import models
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/cep", tags=["CEP"])


@router.get("/{cep}")
def buscar_cep(cep: str, current_user: models.User = Depends(get_current_user)):
    """
    Recebe um CEP e retorna os dados do endereço via ViaCEP.
    
    Args:
        cep: CEP a consultar (8 dígitos)
        
    Returns:
        Dados do endereço (logradouro, bairro, cidade, uf, complemento)
        
    Raises:
        HTTPException: Se CEP for inválido ou não encontrado
    """
    # Remove qualquer caractere que não seja número
    cep_limpo = "".join(filter(str.isdigit, cep))
    
    if len(cep_limpo) != 8:
        raise HTTPException(
            status_code=400,
            detail="CEP inválido. Deve ter 8 dígitos."
        )

    # Consulta a API ViaCEP
    response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/")
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível consultar o CEP"
        )
    
    data = response.json()
    
    if "erro" in data:
        raise HTTPException(
            status_code=404,
            detail="CEP não encontrado"
        )
    
    # Retorna apenas os campos que interessam
    endereco = {
        "logradouro": data.get("logradouro", ""),
        "bairro": data.get("bairro", ""),
        "cidade": data.get("localidade", ""),
        "uf": data.get("uf", ""),
        "cep": data.get("cep", ""),
        "complemento": data.get("complemento", "")
    }
    
    return endereco
