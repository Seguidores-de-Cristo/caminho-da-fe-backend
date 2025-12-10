from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . import __init__ as db_init
from ..core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Se quiser criar as tabelas diretamente (uso com Alembic é recomendado)
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()