"""
Gestionaire de session des sockets
"""
from socketio import AsyncRedisManager

from ..model.config import settings


manager = AsyncRedisManager(settings.REDIS_URL)  # type: ignore

__all__ = ["manager"]
