from typing import Annotated, Literal, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...model.api.api_models import (
    SessionStart,
    SessionTemplateCreated,
    SessionTemplateCreateable,
    SessionTemplateUpdateable,
    StartedSession,
    SurveySession,
)
from ...model.api.auth import only_teacher_allowed
from ...model.database import get_db, db_models
from ...model.database import operations

router = APIRouter()


@router.get("/template/all")
def get_all_session_templates_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)], db: Annotated[Session, Depends(get_db)]
) -> Sequence[SessionTemplateCreated]:
    """
    Renvoie la liste de tous les modèles de sessions crée par l'utilisateur.
    """

    all_templates = operations.get_all_session_templates(db, current_user.id)

    if not all_templates:
        return []

    return [
        SessionTemplateCreated(
            name=t.name,
            type=t.type,  # type: ignore
            authorised_group_id=None if t.is_public else operations.get_authorised_group_id(db, t),
            show_answers=t.show_answers,
            id=t.id,
            survey_id=t.survey_id,
        )
        for t in all_templates
    ]


@router.get("/template/{session_template_id}")
def get_session_template_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    session_template_id: int,
) -> SessionTemplateCreated:
    """
    Renvoie des informations sur un modèle de session.
    """

    template = operations.get_session_template(db, current_user.id, session_template_id)

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session template not found",
        )

    return SessionTemplateCreated(
        name=template.name,
        type=template.type,  # type: ignore
        authorised_group_id=None if template.is_public else operations.get_authorised_group_id(db, template),
        show_answers=template.show_answers,
        id=template.id,
        survey_id=template.survey_id,
    )


@router.post("/template/new")
def create_session_template_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    session_template: SessionTemplateCreateable,
) -> SessionTemplateCreated:
    """
    Crée un modèle de session.
    """

    template = operations.create_session_template(
        db,
        current_user.id,
        session_template.survey_id,
        session_template.name,
        session_template.type,
        session_template.authorised_group_id,
        session_template.show_answers,
    )

    if not template:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can't link session template to this survey",
        )

    return SessionTemplateCreated(
        name=template.name,
        type=template.type,  # type: ignore
        authorised_group_id=None if template.is_public else operations.get_authorised_group_id(db, template),
        show_answers=template.show_answers,
        id=template.id,
        survey_id=template.survey_id,
    )


@router.put("/template/update/{session_template_id}")
def update_session_template_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    session_template_id: int,
    session_template: SessionTemplateUpdateable,
) -> SessionTemplateCreated:
    """
    Modifie un modèle de session déjà existant.
    """

    updated_template = operations.update_session_template(
        db,
        current_user.id,
        session_template_id,
        session_template.survey_id,
        session_template.name,
        session_template.type,
        session_template.authorised_group_id,
        session_template.show_answers,
    )

    if not updated_template:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can't link session template to this survey",
        )

    return SessionTemplateCreated(
        name=updated_template.name,
        type=updated_template.type,  # type: ignore
        authorised_group_id=(
            None if updated_template.is_public else operations.get_authorised_group_id(db, updated_template)
        ),
        show_answers=updated_template.show_answers,
        id=updated_template.id,
        survey_id=updated_template.survey_id,
    )


@router.delete("/template/delete/{session_template_id}")
def delete_session_template_route(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    session_template_id: int,
) -> Literal["OK"]:
    """
    Supprime un modèle de session.
    """

    success = operations.delete_session_template(db, current_user.id, session_template_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this session template",
        )

    return "OK"


@router.post("/start")
def start_survey_session(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    session_start: SessionStart,
) -> StartedSession:
    """
    Démarre une session de questionaire à partir d'un modèle.
    """

    session = operations.start_survey_session(db, current_user.id, session_start.session_template_id)

    return StartedSession(join_code=session.join_code, created_at=session.created_at)


@router.get("/all")
def list_all_sessions(
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[db_models.User, Depends(only_teacher_allowed)]
) -> list[SurveySession]:
    """
    Renvoie la liste de toutes les sessions "lancée" par l'utilisateur.
    """
    return operations.get_all_session(db, current_user.id)
