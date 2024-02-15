"""
Constantes et configuration de l'application.
Elles sont remplacé par les variables d'environnement lors du déploiement.
Lors du developpement, elles sont chargées depuis le fichier .env situé à la racine du projet.
"""
import os
import secrets
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


if os.getenv("IS_TESTING"):
    _model_config = SettingsConfigDict()
else:  # pragma: no cover
    _model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class _Settings(BaseSettings):
    PROJECT_NAME: str = "sae-backend"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DEPLOY_MODE: Literal["prod"] | Literal["dev"]

    SECRET_KEY: str = secrets.token_hex(32)

    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    REDIS_URL: Optional[str] = None

    model_config = _model_config


settings = _Settings()  # type: ignore


def get_dsn(*, is_async=False):
    if os.getenv("IS_TESTING"):
        print("/!\\ Using sqlite in-memory database /!\\")
        if is_async:
            return "sqlite+aiosqlite:///file:TESTING?mode=memory&cache=shared&uri=true"
        return "sqlite:///file:TESTING?mode=memory&cache=shared&uri=true"

    return "postgresql+psycopg://{user}:{password}@{host}/{db}".format(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        db=settings.POSTGRES_DB,
    )
