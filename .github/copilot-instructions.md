Project: Caminho da Fé — backend (FastAPI + SQLAlchemy)

This file gives concise, project-specific guidance for AI coding agents working in this repository.

High-level architecture
- Core stack: `FastAPI` HTTP API (`app/main.py`) using `SQLAlchemy 2` models (`app/models/`) and `Pydantic` schemas (`app/schemas/`).
- DB layer: engine & session in `app/db/session.py`. Alembic is configured under `alembic/` for migrations.
- Patterns: thin `crud/` layer encapsulates DB access (`app/crud/*`), `schemas` define request/response shapes, and `models` hold ORM definitions.

Key files to reference
- `app/main.py` — app startup, route examples (`/users/` create + get).
- `app/core/config.py` — reads `DATABASE_URL` from env (default points to the `db` service in `docker-compose`).
- `app/db/session.py` — `engine`, `SessionLocal`, `Base`, `init_db()` (note: `init_db()` calls `Base.metadata.create_all`, but Alembic is the preferred migration tool).
- `app/models/user.py`, `app/schemas/user.py`, `app/crud/user.py` — canonical example for how models, schemas, and CRUD interact (password hashing with `passlib` in `crud`).
- `alembic/env.py` — Alembic reads `DATABASE_URL` from environment via `python-dotenv`; migrations require `DATABASE_URL` to be set.
- `docker-compose.yaml` — defines `db` service (MariaDB) and credentials which match the default `DATABASE_URL` in `config.py`.

Developer workflows & commands (concrete)
- Install & run via Poetry: use `poetry install` then `poetry run ...` for commands.
- Start DB for local development: `docker compose up -d db` (uses credentials in `docker-compose.yaml`).
- Run the app (local):
  - Example: `poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Migrations (Alembic):
  - Ensure `DATABASE_URL` is set in a `.env` file or environment. `alembic/env.py` will load it via `dotenv`.
  - Create revision: `poetry run alembic revision --autogenerate -m "your message"`
  - Apply migrations: `poetry run alembic upgrade head`
  - If running migrations from outside the compose network, use a host-based URL such as `mysql+pymysql://caminho_user:caminho_password@127.0.0.1:3306/caminho_db` for `DATABASE_URL`.

Project-specific conventions
- Use the `app/` package layout: `models`, `schemas`, `crud`, `db`, `core`.
- Keep DB access in `app/crud/*` functions; routes should call `crud` and use `Depends(get_db)` (see `app/main.py`).
- Use `pydantic` models with `orm_mode = True` for response models (see `UserOut` in `app/schemas/user.py`).
- Passwords are hashed via `passlib` in `app/crud/user.py` — preserve that approach for any auth-related changes.
- Prefer Alembic for schema changes. `app/db/session.init_db()` exists for convenience but don't rely on it for production migrations.

Integration points & environment
- `DATABASE_URL` is central — many tools (app, Alembic) read it. Prefer `.env` for local development; CI should inject it as a secret.
- Docker expectations: default DB URL in `app/core/config.py` points to service `db` (works inside Docker Compose network). When running locally against the DB exposed on `localhost`, update `DATABASE_URL` accordingly.

Notes for contributors/AI agents
- When changing models: update `app/models/*`, then create an Alembic revision (`alembic revision --autogenerate`) and migrate (`alembic upgrade head`). Alembic is configured to import `app.models` and `app.db.session.Base`.
- For DB sessions in handlers, follow existing `Depends(get_db)` generator pattern to ensure proper session lifecycle (`app/db/session.py`).
- Keep changes minimal and consistent with repository style: small, focused edits; do not reformat unrelated files.

Examples to reference when making edits
- Add user endpoint — see `app/main.py` (uses `crud_user.create_user`, `schemas.UserCreate`, `schemas.UserOut`).
- Hashing example — `app/crud/user.py::get_password_hash` uses `passlib.context.CryptContext` with `bcrypt` scheme.

If something is unclear
- Ask for the intended runtime (inside compose vs local host) when database connection details matter.
- If a migration fails, confirm `DATABASE_URL` and that the DB container is reachable (`docker compose ps` / `docker compose logs db`).

Quick checklist for PRs touching DB schema
- Update or add SQLAlchemy model(s) in `app/models/`.
- Run `poetry run alembic revision --autogenerate -m "desc"` and commit the new migration under `alembic/versions/`.
- Run `poetry run alembic upgrade head` locally to validate migrations.

---
Please review these instructions and tell me if you'd like more detail about tests, CI, or example PR templates.
