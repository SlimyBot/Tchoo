"""
Routes API en rapport avec les groupes.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sae_backend.model.database import db_models

from ...model.api.auth import only_teacher_allowed

from ...model.api.api_models import GroupCreated, GroupRead, GroupMember, User_gotten
from ...model.database import get_db
from ...model.database.operations import (
    create_group,
    get_group,
    get_groups,
    delete_group,
    get_user_groups,
    remove_member,
    update_group,
    add_user_to_group,
    get_group_users,
)


router = APIRouter()


@router.post("/create_group", response_model=GroupCreated)
def create_group_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    group_name: str,
    parent_group_id: Optional[int] = None,
):
    """
    Crée un groupe.
    """
    new_group = create_group(db, current_user.id, group_name, parent_group_id)
    return new_group


@router.post("/add_member/{group_id}", response_model=GroupMember)
def add_member_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    group_id: int,
    member_id: int,
):
    """
    Ajoute un membre à un groupe.
    """
    add_user_result = add_user_to_group(db, current_user.id, member_id, group_id)

    if not add_user_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add user to the group",
        )

    return add_user_result


@router.get("/get_groups", response_model=list[GroupRead])
def get_groups_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Récupère tous les groupes.
    """
    return get_groups(db)


@router.get("/get_user_groups/{user_id}", response_model=list[GroupRead])
def get_user_groups_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
):
    """
    Récupère tous les groupes d'un utilisateur.
    """
    return get_user_groups(db, user_id)


@router.get("/{group_id}", response_model=GroupRead)
def get_group_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    group_id: int,
):
    """
    Récupère un groupe.
    """
    group = get_group(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    return group


@router.put("/update_group/{group_id}", response_model=GroupRead)
def update_group_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    group_id: int,
    name: str,
):
    """
    Modifie un groupe.
    """
    group = get_group(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    update_group(db, group_id, name)
    return group


@router.delete("/delete_group/{group_id}", response_model=GroupRead)
def delete_group_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    group_id: int,
):
    """
    Supprime un groupe.
    """
    group = get_group(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    delete_group(db, group_id)
    return group


@router.delete("/remove_member/{group_id}", response_model=GroupMember)
def remove_member_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    group_id: int,
    member_id: int,
):
    """
    Supprime un membre d'un groupe.
    """
    removedMember = remove_member(db, group_id, current_user.id, member_id)
    if not removedMember:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove member from the group",
        )
    return removedMember


@router.get("/get_group_users/{group_id}", response_model=list[User_gotten])
def get_group_users_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    group_id: int,
):
    """
    Récupère tous les utilisateurs d'un groupe.
    """
    return get_group_users(db, group_id)
