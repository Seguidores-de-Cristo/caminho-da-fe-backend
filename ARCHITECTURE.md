"""Documentação da arquitetura refatorada."""

# Arquitetura de Software - Caminho da Fé Backend

## Estrutura de Pastas

```
app/
├── models/                      # Modelos SQLAlchemy (ORM)
│   ├── user.py
│   └── novo_convertido.py
├── schemas/                     # Schemas Pydantic (validação)
│   ├── user.py
│   ├── novo_convertido.py
│   └── common.py               # NEW: Schemas comuns (paginação, erros)
├── crud/                        # CRUD básico (database operations)
│   ├── user.py
│   └── novo_convertido.py
├── services/                    # NEW: Lógica de negócio
│   ├── user_service.py
│   ├── novo_convertido_service.py
│   └── discipulado_relationship_service.py
├── routers/                     # NEW: Rotas HTTP (endpoints)
│   ├── users_router.py
│   ├── novos_convertidos_router.py
│   └── discipulado_router.py
├── exceptions/                  # NEW: Exceções customizadas
│   ├── app_exceptions.py
│   └── __init__.py
├── utils/                       # NEW: Utilitários
│   ├── cep_service.py          # Integração com API ViaCEP
│   └── __init__.py
├── db/
│   ├── session.py
│   └── __init__.py
├── core/
│   └── config.py
└── main.py                      # Aplicação FastAPI
```

## Camadas de Arquitetura

### 1. **Models (ORM)** - `app/models/`
Definem a estrutura das tabelas no banco de dados usando SQLAlchemy.

- `User` — usuários/discipuladores
- `NovoConvertido` — novos convertidos

### 2. **Schemas (Validação)** - `app/schemas/`
Definem validação de entrada/saída usando Pydantic.

**Benefícios:**
- Tipagem forte
- Validação automática
- Documentação OpenAPI

**Exemplo:**
```python
class NovoConvertidoCreate(NovoConvertidoBase):
    """Schema para criação (input)"""
    pass

class NovoConvertidoOut(NovoConvertidoBase):
    """Schema para saída (output)"""
    id: int
    data_cadastro: date
```

### 3. **CRUD** - `app/crud/`
Operações básicas de banco: CREATE, READ, UPDATE, DELETE.

- Responsável apenas por I/O do banco
- Sem lógica de negócio
- Sem validações complexas

### 4. **Services (Lógica de Negócio)** - `app/services/` **NEW**
Encapsula toda a lógica de negócio e regras de validação.

**Benefícios:**
- Separação de responsabilidades
- Reutilizável em múltiplos endpoints
- Fácil de testar
- Centraliza validações

**Exemplo:**
```python
class NovoConvertidoService:
    @staticmethod
    def criar_convertido(db: Session, convertido_in: NovoConvertidoCreate) -> NovoConvertido:
        # Validar discipulador existe
        # Validar datas
        # Validar nome e telefone
        # Chamar CRUD para criar
        return create_novo_convertido(db, convertido_in)
```

### 5. **Routers (Endpoints HTTP)** - `app/routers/` **NEW**
Definem os endpoints HTTP.

**Benefícios:**
- Routers organizados por domínio
- Reutilizam services
- Código limpo e legível

**Exemplo:**
```python
@router.post("/novos-convertidos/", response_model=NovoConvertidoOut)
def criar_novo_convertido(convertido_in: NovoConvertidoCreate, db: Session = Depends(get_db)):
    try:
        return NovoConvertidoService.criar_convertido(db, convertido_in)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
```

### 6. **Exceptions (Tratamento de Erros)** - `app/exceptions/` **NEW**
Exceções customizadas para melhor tratamento de erros.

**Tipos:**
- `ResourceNotFoundException` — 404
- `ValidationException` — 400
- `ConflictException` — 409
- `UnauthorizedException` — 401

### 7. **Utils (Utilitários)** - `app/utils/` **NEW**
Funcionalidades reutilizáveis (integração com ViaCEP, etc).

## Fluxo de uma Requisição

```
HTTP Request (POST /novos-convertidos/)
    ↓
Router (novos_convertidos_router.py)
    ↓
Service (NovoConvertidoService.criar_convertido)
    ├─ Validação 1: Discipulador existe
    ├─ Validação 2: Datas válidas
    ├─ Validação 3: Dados obrigatórios
    ↓
CRUD (create_novo_convertido)
    ↓
Database (INSERT)
    ↓
Response (NovoConvertidoOut)
```

## Benefícios da Arquitetura

| Aspecto | Benefício |
|---------|-----------|
| **Separação de responsabilidades** | Cada camada tem um propósito claro |
| **Testabilidade** | Services podem ser testadas isoladamente |
| **Reutilização** | Services usáveis em múltiplos contextos |
| **Manutenibilidade** | Código organizado e legível |
| **Escalabilidade** | Fácil adicionar novos features |
| **Tratamento de erros** | Centralizado e consistente |

## Routers Disponíveis

### Users Router
```
POST   /users/                              # Criar usuário
GET    /users/{user_id}                     # Obter usuário
GET    /users/                              # Listar usuários (paginado)
PUT    /users/{user_id}                     # Atualizar usuário
GET    /users/{user_id}/convertidos-count   # Contar convertidos
```

### Novos Convertidos Router
```
POST   /novos-convertidos/                  # Criar convertido
POST   /novos-convertidos/com-cep/          # Criar com preenchimento automático de CEP
GET    /novos-convertidos/{convertido_id}   # Obter convertido
GET    /novos-convertidos/                  # Listar convertidos (paginado)
PUT    /novos-convertidos/{convertido_id}   # Atualizar convertido
```

### Discipulado Router
```
GET    /discipulador/{id}/convertidos                           # Listar convertidos de um discipulador
POST   /discipulador/convertidos/{id}/vincular/{disc_id}       # Vincular convertido a discipulador
POST   /discipulador/convertidos/{id}/desvincular              # Desvincular convertido
GET    /discipulador/convertidos/{id}/discipulador             # Obter discipulador de um convertido
```

## Como Usar

### 1. Adicionar novo endpoint

**Arquivo:** `app/routers/meu_router.py`
```python
from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.services import MeuService
from app.exceptions import AppException

router = APIRouter(prefix="/meu-recurso", tags=["Meu Recurso"])

@router.post("/", status_code=201)
def criar_meu_recurso(dados_in: MeuSchema, db: Session = Depends(get_db)):
    try:
        return MeuService.criar(db, dados_in)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
```

**Arquivo:** `app/main.py`
```python
from app.routers import meu_router
app.include_router(meu_router)
```

### 2. Adicionar nova service

**Arquivo:** `app/services/meu_service.py`
```python
from app.exceptions import ValidationException, ResourceNotFoundException

class MeuService:
    @staticmethod
    def criar(db: Session, dados_in: MeuSchema):
        # Validações
        # Chamar CRUD
        # Retornar resultado
        pass
```

### 3. Usar a service em testes

```python
from app.services import MeuService

def test_criar_meu_recurso():
    service = MeuService()
    resultado = service.criar(db, dados_validos)
    assert resultado.id is not None
```

## Próximas Melhorias

- [ ] Autenticação JWT
- [ ] Autorização (RBAC)
- [ ] Validações mais avançadas
- [ ] Busca e filtros complexos
- [ ] Logs centralizados
- [ ] Testes unitários completos
- [ ] Documentação Swagger avançada
- [ ] Soft deletes
- [ ] Auditoria (who/when/what changed)
"""

