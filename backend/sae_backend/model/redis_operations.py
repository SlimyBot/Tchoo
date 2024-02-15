from contextlib import asynccontextmanager

import redis.asyncio as aredis

from .config import settings


_pool = aredis.ConnectionPool.from_url(
    settings.REDIS_URL,  # type: ignore
    max_connections=None,
    health_check_interval=10,
    socket_connect_timeout=5,
    retry_on_timeout=True,
    socket_keepalive=True,
)


@asynccontextmanager
async def get_redis_session():
    client = None
    try:
        client = aredis.Redis.from_pool(_pool)
        yield client
    finally:
        if client is not None:
            await client.aclose()


async def join_session(client: aredis.Redis, email: str, join_code: str):
    """
    Enregistre un utilisateur comme faisant partie d'une session.
    """
    await client.sadd(f"{join_code}:users", email)  # type: ignore


async def leave_session(client: aredis.Redis, email: str, join_code: str):
    """
    Fait quitter un utilisateur d'une session.
    """
    await client.srem(f"{join_code}:users", email)  # type: ignore


async def is_in_session(client: aredis.Redis, email: str, join_code: str) -> bool:
    """
    Vérifie si un utilisateur a rejoind une session.
    """
    return bool(await client.sismember(f"{join_code}:users", email))  # type: ignore


async def nb_users_in_session(client: aredis.Redis, join_code: str) -> int:
    """
    Renvoie le nombre d'utilisateurs connectés a une session.
    """
    return await client.scard(f"{join_code}:users")  # type: ignore


async def set_session_sid_owner(client: aredis.Redis, join_code: str, sid: str):
    """
    Sauvegarde le sid  propriétaire de la session.
    """
    await client.set(f"{join_code}:owner_sid", sid)


async def get_session_sid_owner(client: aredis.Redis, join_code: str) -> str:
    """
    Renvoie le sid du propriétaire de la session.
    """
    sid_bytes: bytes = await client.get(f"{join_code}:owner_sid")
    return sid_bytes.decode("utf-8")
