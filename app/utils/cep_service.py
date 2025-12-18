"""Utilitários para CEP e endereço."""

import requests
from typing import Dict, Any, Optional
from app.exceptions import ValidationException


class CEPService:
    """Serviço para buscar dados de CEP via API ViaCEP."""

    API_URL = "https://viacep.com.br/ws/{cep}/json/"

    @staticmethod
    def buscar_cep(cep: str) -> Dict[str, Any]:
        """
        Busca informações de endereço pelo CEP.

        Args:
            cep: CEP no formato xxxxx-xxx ou xxxxxxxx

        Returns:
            Dict com dados do endereço (logradouro, bairro, localidade, uf, etc)

        Raises:
            ValidationException: Se o CEP é inválido ou não foi encontrado
        """
        # Remover caracteres não numéricos
        cep_limpo = "".join(filter(str.isdigit, cep))

        if len(cep_limpo) != 8:
            raise ValidationException(
                "CEP inválido. Deve conter 8 dígitos.",
                details={"cep": cep},
            )

        try:
            response = requests.get(
                CEPService.API_URL.format(cep=cep_limpo),
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()

            # ViaCEP retorna {"erro": true} se não encontra
            if data.get("erro"):
                raise ValidationException(
                    f"CEP {cep} não encontrado",
                    details={"cep": cep},
                )

            return {
                "logradouro": data.get("logradouro", ""),
                "complemento": data.get("complemento", ""),
                "bairro": data.get("bairro", ""),
                "cidade": data.get("localidade", ""),
                "uf": data.get("uf", ""),
            }
        except requests.RequestException as e:
            raise ValidationException(
                "Erro ao consultar CEP. Tente novamente.",
                details={"error": str(e)},
            )

    @staticmethod
    def preencher_endereco(
        cep: str,
        endereco: Optional[str] = None,
        bairro: Optional[str] = None,
        cidade: Optional[str] = None,
        uf: Optional[str] = None,
        complemento: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Preenche dados de endereço consultando CEP e mesclando com dados fornecidos.

        Se algum campo já foi fornecido, mantém o valor fornecido.
        Caso contrário, preenche com dados da API ViaCEP.

        Args:
            cep: CEP para buscar
            endereco: Endereço (se não fornecido, busca da API)
            bairro: Bairro (se não fornecido, busca da API)
            cidade: Cidade (se não fornecido, busca da API)
            uf: Estado (se não fornecido, busca da API)
            complemento: Complemento (se não fornecido, busca da API)

        Returns:
            Dict com os campos preenchidos
        """
        dados_cep = CEPService.buscar_cep(cep)

        return {
            "endereco": endereco or dados_cep["logradouro"],
            "bairro": bairro or dados_cep["bairro"],
            "cidade": cidade or dados_cep["cidade"],
            "uf": uf or dados_cep["uf"],
            "complemento": complemento or dados_cep["complemento"],
        }
