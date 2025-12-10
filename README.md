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

- Subir o > docker-compose up -d
- Testar se o banco subiu > docker compose logs -f db
- Subir migrations (Banco) > poetry alembic upgrade head
- Rodar a api > poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000