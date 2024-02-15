"""
Tout ce aqui concerne la communication avec la base de données ainsi que les opération CRUD.
"""

from sqlalchemy.orm import Session
from typing import Generator, Any

from .connection import SessionLocal, engine
from .db_models import Base


def init_db():
    """
    Effectue la population initiale de la base de données.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, Any, Any]:  # pragma: no cover
    """
    Fourni une connexion à la base de données depuis une route API.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
