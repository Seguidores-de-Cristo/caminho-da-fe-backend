# caminho-da-fe-backend

## Dependencias

Execute e siga as instruções para cada dependencia 

### Python (pyenv)

> curl https://pyenv.run | bash

- Instale a versão do python para trabalhar (3.12.1)

### Poetry

> curl -sSL https://install.python-poetry.org | python3 -

## Instalar dependencias e ativar ambiente

> poetry install

> poetry env activate

## Rodar localmente

- Subir o > docker compose up -d
- Testar se o banco subiu > docker compose logs -f db
- Subir migrations (Banco) > poetry alembic upgrade head
- VersionsDB -> poetry run alembic revision --autogenerate -m "description of migration"
- Subir migrations (Banco) > poetry run alembic upgrade head
- Rodar a api > poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

## Senhas e hashing

- O projeto usa Argon2 para hashing de senhas através do `passlib` (handler `argon2`).
- A dependência `argon2-cffi` é requerida (já adicionada no `pyproject.toml`).
- Motivo: Argon2 evita o limite de 72 bytes do bcrypt e oferece hashing moderno e seguro.
- Observação sobre compatibilidade: se já existirem hashes antigos com bcrypt no banco, verifique se você
	precisa manter suporte a verificação legacy (adicionar `bcrypt` ou `bcrypt_sha256` no `CryptContext`).

Exemplo de verificação/geração local rápida:
```bash
poetry run python -c "from app.crud.user import get_password_hash; print(get_password_hash('minha_senha_segura'))"
```

Instalação do resquests:
pip install requests