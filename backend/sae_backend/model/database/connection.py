"""
Connexion avec la base de données.
"""
import os
from functools import partial

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import get_dsn

if os.getenv("IS_TESTING"):
    engine_creator = create_engine
else:  # pragma: no cover
    engine_creator = partial(create_engine, pool_size=25)


engine = engine_creator(get_dsn())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
