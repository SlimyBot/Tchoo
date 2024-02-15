"""
Routes API en rapport avec les utilisateurs.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sae_backend.model.config import settings

from ...model.api.api_models import NewUserInfo, User, User_gotten, UserCreate
from ...model.api.auth import create_access_token, student_or_teacher_allowed
from ...model.database import get_db
from ...model.database.operations import get_user, get_user_by_id, modify_user, register_user

router = APIRouter()


@router.post("/register")
def register_user_route(db: Annotated[Session, Depends(get_db)], user_in: UserCreate) -> User:
    """
    Crée un compte utilisateur.
    """
    return register_user(db, user_in.name, user_in.surname, user_in.email, user_in.affiliation)


@router.get("/me")
def get_user_info(active_user: Annotated[User, Depends(student_or_teacher_allowed)]) -> User:
    """
    Renvoie des informations sur l'utilisateur actuelement connecté.
    """
    return active_user


@router.post("/me")
def change_user_info(
    db: Annotated[Session, Depends(get_db)],
    active_user: Annotated[User, Depends(student_or_teacher_allowed)],
    new_user_info: NewUserInfo,
) -> User:
    """
    Modifie les informations de l'utilisateur actuelement connecté.
    """
    return modify_user(db, active_user.email, new_user_info.name, new_user_info.surname)


@router.get("/get_user/{user_id}", response_model=User_gotten)
def get_user_route(
    db: Annotated[Session, Depends(get_db)],
    active_user: Annotated[User, Depends(student_or_teacher_allowed)],
    user_id: int,
):
    """
    Récupère un utilisateur.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/get_user_by_email/{user_email}", response_model=User_gotten)
def get_user_by_email_route(
    db: Annotated[Session, Depends(get_db)],
    active_user: Annotated[User, Depends(student_or_teacher_allowed)],
    user_email: str,
):
    """
    Récupère un utilisateur.
    """
    user = get_user(db, user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


if settings.DEPLOY_MODE == "dev":  # pragma: no cover
    @router.get("/dev_only_get_jwt/{email}")
    def dev_only_get_jwt(email: str) -> str:
        """
        Uniquement pendant le developpement, génère un jwt pour cette email sans affiliation.
        """

        return create_access_token({"sub": email})
