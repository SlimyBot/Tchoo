from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from sae_backend import app
from sae_backend.model.config import get_dsn
from sae_backend.model.database import Base, get_db
from sae_backend.model.database.async_ import AsyncScopedSession as TestingAsyncSession

from .testing_data import populate_database

engine = create_engine(
    get_dsn(),
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création du DDL
Base.metadata.create_all(bind=engine)

# Population initiale de la base de données
with TestingSessionLocal() as db:
    populate_database(db)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

__all__ = ["TestingAsyncSession"]
