"""
Routes API en rapport avec les questions.
"""

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sae_backend.model.database import db_models

from ...model.api.api_models import (
    Answer,
    AnswerCreate,
    Question,
    QuestionUpdate,
    Survey,
    SurveyBase,
    SurveysBase,
    SurveyUpdateParam,
    AnswerBase,
    SurveyInfoBase,
)  # QuestionRead, Token, User, UserCreate, SurveyRead,
from ...model.api.auth import only_teacher_allowed
from ...model.database import get_db
from ...model.database import operations

router = APIRouter()


@router.post("/create_survey")
def create_survey(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    survey: Survey,
):
    """
    Créer un sondage.
    """
    return operations.create_survey(db, current_user.id, survey.title, survey.subject)


@router.get("/read_surveys", response_model=list[SurveysBase])
def read_surveys(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)], db: Annotated[Session, Depends(get_db)]
):
    """
    Permet de lister tous les sondages de l'utilisateur connecté.
    """

    return operations.get_surveys(db, current_user.id)


@router.get("/get_survey_info/{survey_id}", response_model=SurveyInfoBase)
def get_survey_info(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    survey_id: int,
):
    """
    Avoir les informations d'un sondage grâce au "survey_id" passé dans le paramètre de chemin.
    """
    return operations.get_survey_info(db, current_user.id, survey_id)


@router.get("/read_survey/{survey_id}", response_model=list[SurveyBase])
def read_survey(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    survey_id: int,
):
    """
    Avoir les questions d'un sondage grâce au "survey_id" passé dans le paramètre de chemin.
    """
    return operations.get_survey(db, current_user.id, survey_id)


@router.put("/update_survey")
def update_survey(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    survey: SurveyUpdateParam,
):
    """
    Met à jour un sondage à l'aide des paramètres de questionnaire passé en paramètre de requête.
    """
    operations.update_survey(
        db,
        current_user.id,
        survey.survey_id,
        survey.title,
        survey.subject,
    )


@router.delete("/delete_survey")
def delete_survey(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    survey_id: int,
):
    """
    Supprimer un sondage à l'aide du "survey_id" du paramètre passé en paramètre de requête.
    """
    operations.delete_survey(db, current_user.id, survey_id)


@router.post("/link_question")
def add_question_to_survey(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    survey_id: int,
    question_id: int,
):
    """
    Permet de lier une question à un questionnaire grâce au "survey_id" et "question_id" passé en paramètre de requête.
    """
    operations.add_question_to_survey(db, current_user.id, survey_id, question_id)


@router.delete("/unlink_question")
def remove_question_from_survey(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    survey_id: int,
    question_id: int,
):
    """
    Permet de délier une question à un questionnaire grâce au "survey_id" et
    "question_id" passé en paramètre de requête.
    """
    operations.remove_question_from_survey(db, current_user.id, survey_id, question_id)


@router.post("/create_question")
def create_question(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    question: Question,
):
    """
    Créer une question.
    """
    return operations.create_question(db, current_user.id, question.type, question.text, question.media)


@router.get("/read_questions_bank", response_model=list[SurveyBase])
def read_questions(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)], db: Annotated[Session, Depends(get_db)]
):
    """
    Permet de lister toutes les questions pour la banque de question de l'utilisateur connecté.
    """
    return operations.get_questions(db, current_user.id)


@router.get("/read_question/{question_id}", response_model=tuple[SurveyBase, list[AnswerBase]])
def read_question(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    question_id: int,
):
    """
    Renvoi la question et les réponses grâce au "question_id" passé en paramètre de chemin.
    """
    return (
        operations.get_question(db, current_user.id, question_id),
        operations.get_answers(db, current_user.id, question_id),
    )


@router.put("/update_question")
def update_question(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    question: QuestionUpdate,
):
    """
    Met à jour une question grâce aux paramètres d'une question passé en paramètre de requête.
    """
    operations.update_question(db, current_user.id, question.question_id, question.text, question.media, question.type)


@router.delete("/delete_question")
def delete_question(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    id_question: int,
):
    """
    Supprime une question grâce au "question_id" passé dans en paramètre de requête si
    l'autorisation est vrai sinon retourne none (tester d'abord si la question possède
    des liens).
    """
    operations.delete_question(db, current_user.id, id_question)


@router.post("/create_answer")
def create_answer(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    answer: AnswerCreate,
):
    """
    Créer une réponse et l'associe à une question.
    """
    res = operations.create_answer(db, current_user.id, answer.question_id, answer.text, answer.is_good_answer)
    if res is None:
        return "fail"


@router.put("/update_answer")
def update_answer(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    answer: Answer,
):
    """
    Met à jour une réponse grâce aux paramètres d'une réponse passé en paramètre de requête.
    """
    return operations.update_answer(db, current_user.id, answer.id_answer, answer.text, answer.is_good_answer)


@router.delete("/delete_answer")
def delete_answer(
    current_user: Annotated[db_models.User, Depends(only_teacher_allowed)],
    db: Annotated[Session, Depends(get_db)],
    answer_id: int,
):
    """
    Supprime une réponse grâce au "answer_id" passé en paramètre de requête.
    """
    operations.delete_answer(db, current_user.id, answer_id)
