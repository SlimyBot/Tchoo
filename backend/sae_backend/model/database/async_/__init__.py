"""
Connexion à la base de données asyncrone
"""
import os
from asyncio import current_task
from functools import partial

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from ...config import get_dsn

if os.getenv("IS_TESTING"):
    engine_creator = create_async_engine
else:
    engine_creator = partial(create_async_engine, pool_size=20, max_overflow=-1)


async_engine = engine_creator(get_dsn(is_async=True))
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)
AsyncScopedSession = async_scoped_session(
    async_session_factory,
    scopefunc=current_task,
)
