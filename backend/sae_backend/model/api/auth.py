"""
Authentification et vérification des utilisateurs.
"""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ...model.database import db_models, get_db
from ...model.database.operations import get_user
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")  # XXX: url non utilisée


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crée un token d'accès JWT.

    Paramètres
    ----------

    data : dict
        Données à encoder dans le token.

    expires_delta : int | None
        Durée de validité du token, en minutes.

    Retour
    ------

    str
        Le token d'accès JWT qui correspond.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Expire par default au bout de 15 minutes

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def get_email_from_jwt(token: str) -> str | None:
    """
    Renvoie l'adresse mail contenue dans le token JWT

    Paramètres
    ----------

    token : str
        Token JWT.

    Retour
    ------

    str | None
        Adresse mail contenue dans le token.
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload.get("sub")


def _get_current_user(db: Session, token: str, *, only_teachers=False) -> db_models.User:
    """
    Renvoie l'utilisateur qui correspond au token de connexion (méthode interne).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = get_email_from_jwt(token)

        # Test si le token contient un nom d'utilisateur
        if username is None:
            raise credentials_exception

    except JWTError:
        # Le token n'est pas valide (expiré, mauvaise signature, etc.)
        raise credentials_exception

    user = get_user(db, username)

    # Test si l'utilisateur existe dans la base de données
    if user is None:
        raise credentials_exception

    if only_teachers and user.affiliation == db_models.UserAffiliation.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student not allowed to use this route",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def only_teacher_allowed(
    db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]
) -> db_models.User:
    """
    Authorise uniquement un professeur a utiliser la route.
    """
    return _get_current_user(db, token, only_teachers=True)


def student_or_teacher_allowed(
    db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]
) -> db_models.User:
    """
    Authorise les étudiants et professeurs a utiliser la route.
    """
    return _get_current_user(db, token)
