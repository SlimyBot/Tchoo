"""
Routes en rapport avec l'historique des sessions auxquelles
l'etudiant a participé'.
"""
from typing import Annotated
from fastapi import APIRouter, Depends
from sae_backend.model.database import db_models
from sqlalchemy.orm import Session
from ...model.database import get_db
from ...model.api.auth import student_or_teacher_allowed
from ...model.database.operations import (
    get_sessions_player,
    get_join_code_survey_id,
    get_name_survey_owner,
    get_sessions_results,
)


router = APIRouter()


@router.get("/get_sessions_player")
def get_sessions(
    current_user: Annotated[db_models.User, Depends(student_or_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Récupère les sessions auxquelles l'étudiant a participé.
    """
    sessions = get_sessions_player(db, current_user.id)
    jcSurveyId = get_join_code_survey_id(db, sessions)
    surveyNameOwner = get_name_survey_owner(db, jcSurveyId)
    sessionsResults = get_sessions_results(db, surveyNameOwner, current_user.id)

    return sessionsResults
