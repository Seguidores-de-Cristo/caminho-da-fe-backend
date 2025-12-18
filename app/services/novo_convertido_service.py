"""Camada de serviços para gerenciar lógica de negócio de novos convertidos."""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.novo_convertido import NovoConvertido
from app.schemas.novo_convertido import (
    NovoConvertidoCreate,
    NovoConvertidoUpdate,
)
from app.crud.novo_convertido import (
    create_novo_convertido,
    get_novo_convertido,
    list_novos_convertidos,
    update_novo_convertido,
)
from app.crud.user import get_user
from app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
)
from app.utils.cep_service import CEPService


class NovoConvertidoService:
    """Serviço centralizado para operações de novo convertido."""

    @staticmethod
    def criar_convertido(
        db: Session, convertido_in: NovoConvertidoCreate
    ) -> NovoConvertido:
        """
        Cria um novo convertido com validações completas.

        Validações:
        - Discipulador existe
        - Dados obrigatórios preenchidos
        - Datas válidas
        - CEP preenchimento automático

        Args:
            db: Sessão do banco
            convertido_in: Dados do novo convertido

        Returns:
            Novo convertido criado

        Raises:
            ValidationException: Se dados inválidos
            ResourceNotFoundException: Se discipulador não existe
        """
        # Validar discipulador
        discipulador = get_user(db, convertido_in.discipulador_id)
        if not discipulador:
            raise ResourceNotFoundException(
                "Discipulador", convertido_in.discipulador_id
            )

        # Validar datas
        if convertido_in.data_nascimento >= date.today():
            raise ValidationException(
                "Data de nascimento deve ser no passado",
                details={"data_nascimento": str(convertido_in.data_nascimento)},
            )

        if convertido_in.data_conversao > date.today():
            raise ValidationException(
                "Data de conversão não pode ser no futuro",
                details={"data_conversao": str(convertido_in.data_conversao)},
            )

        # Validar nome
        if not convertido_in.nome or len(convertido_in.nome.strip()) < 3:
            raise ValidationException(
                "Nome deve ter pelo menos 3 caracteres",
                details={"nome": convertido_in.nome},
            )

        # Validar telefone (básico: apenas números)
        telefone_limpo = "".join(filter(str.isdigit, convertido_in.telefone))
        if len(telefone_limpo) < 10:
            raise ValidationException(
                "Telefone deve ter pelo menos 10 dígitos",
                details={"telefone": convertido_in.telefone},
            )

        # Criar objeto e retornar
        return create_novo_convertido(db, convertido_in)

    @staticmethod
    def criar_convertido_com_cep(
        db: Session,
        convertido_in: NovoConvertidoCreate,
        cep: Optional[str] = None,
    ) -> NovoConvertido:
        """
        Cria novo convertido preenchendo endereço automaticamente via CEP se informado.

        Args:
            db: Sessão do banco
            convertido_in: Dados do novo convertido
            cep: CEP para preenchimento automático (se não fornecido em convertido_in)

        Returns:
            Novo convertido criado

        Raises:
            ValidationException: Se dados inválidos ou CEP inválido
        """
        # Se CEP não foi fornecido em convertido_in, usar o parâmetro
        cep_final = cep or convertido_in.cep

        if not cep_final:
            raise ValidationException(
                "CEP é obrigatório",
                details={"cep": None},
            )

        # Preencher endereço via CEP
        endereco_data = CEPService.preencher_endereco(
            cep=cep_final,
            endereco=convertido_in.endereco,
            bairro=convertido_in.bairro,
            cidade=convertido_in.cidade,
            uf=convertido_in.uf,
            complemento=convertido_in.complemento,
        )

        # Atualizar convertido_in com dados do CEP
        convertido_in.cep = cep_final
        convertido_in.endereco = endereco_data["endereco"]
        convertido_in.bairro = endereco_data["bairro"]
        convertido_in.cidade = endereco_data["cidade"]
        convertido_in.uf = endereco_data["uf"]
        if not convertido_in.complemento:
            convertido_in.complemento = endereco_data["complemento"]

        # Criar convertido
        return NovoConvertidoService.criar_convertido(db, convertido_in)

    @staticmethod
    def obter_convertido(db: Session, convertido_id: int) -> NovoConvertido:
        """
        Obtém um novo convertido pelo ID. A idade é calculada automaticamente via property.

        Args:
            db: Sessão do banco
            convertido_id: ID do convertido

        Returns:
            Novo convertido encontrado (com idade calculada em memória)

        Raises:
            ResourceNotFoundException: Se convertido não existe
        """
        convertido = get_novo_convertido(db, convertido_id)
        if not convertido:
            raise ResourceNotFoundException("Novo Convertido", convertido_id)
        return convertido

    @staticmethod
    def listar_convertidos(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[NovoConvertido]:
        """
        Lista novos convertidos com paginação. A idade é calculada automaticamente via property.

        Args:
            db: Sessão do banco
            skip: Quantidade de registros a pular
            limit: Limite de registros

        Returns:
            Lista de novos convertidos (com idade calculada em memória para cada um)
        """
        query = db.query(NovoConvertido).offset(skip).limit(limit)
        return query.all()

    @staticmethod
    def listar_convertidos_por_discipulador(
        db: Session, discipulador_id: int, skip: int = 0, limit: int = 100
    ) -> List[NovoConvertido]:
        """
        Lista todos os novos convertidos de um discipulador. Idade calculada automaticamente via property.

        Args:
            db: Sessão do banco
            discipulador_id: ID do discipulador
            skip: Quantidade de registros a pular
            limit: Limite de registros

        Returns:
            Lista de novos convertidos do discipulador (com idade calculada em memória)

        Raises:
            ResourceNotFoundException: Se discipulador não existe
        """
        # Validar que discipulador existe
        discipulador = get_user(db, discipulador_id)
        if not discipulador:
            raise ResourceNotFoundException("Discipulador", discipulador_id)

        query = (
            db.query(NovoConvertido)
            .filter(NovoConvertido.discipulador_id == discipulador_id)
            .offset(skip)
            .limit(limit)
        )
        return query.all()

    @staticmethod
    def atualizar_convertido(
        db: Session, convertido_id: int, convertido_in: NovoConvertidoUpdate
    ) -> NovoConvertido:
        """
        Atualiza um novo convertido.

        Args:
            db: Sessão do banco
            convertido_id: ID do convertido
            convertido_in: Dados a atualizar

        Returns:
            Novo convertido atualizado

        Raises:
            ResourceNotFoundException: Se convertido não existe
            ValidationException: Se dados inválidos
        """
        convertido = get_novo_convertido(db, convertido_id)
        if not convertido:
            raise ResourceNotFoundException("Novo Convertido", convertido_id)

        # Se discipulador foi alterado, validar
        if (
            convertido_in.discipulador_id
            and convertido_in.discipulador_id != convertido.discipulador_id
        ):
            novo_disc = get_user(db, convertido_in.discipulador_id)
            if not novo_disc:
                raise ResourceNotFoundException(
                    "Discipulador", convertido_in.discipulador_id
                )

        return update_novo_convertido(db, convertido, convertido_in)
