"""
Les modèles Pydantic utilisé par l'API.
A ne pas confondre avec les modèles de la base de données.
"""
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from sae_backend.model.database.db_models import QuestionType, SurveySessionType, UserAffiliation


class Token(BaseModel):
    """
    Objet renvoyé par la route de login, contiens le token d'accès et son type.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Les données qui sont lié au token JWT.
    """

    username: str | None = None


class UserCreate(BaseModel):
    """
    Données utilisées pour créer un compte.
    """

    email: str
    affiliation: str
    name: str | None = None
    surname: str | None = None


class User(BaseModel):
    """
    Données d'un utilisateur renvoyé par l'API.
    """

    email: str
    name: str | None = None
    surname: str | None = None


class User_gotten(BaseModel):
    """
    Données d'un utilisateur renvoyé par l'API.
    """

    id: int
    email: str
    name: str | None = None
    surname: str | None = None


class NewUserInfo(BaseModel):
    """
    Données d'un utilisateur qui peuven être modifiées.
    """

    name: str | None = None
    surname: str | None = None


class UserInDB(User):
    """
    Un utilisateur dans la base de données.
    """

    hashed_password: str
    affiliation: UserAffiliation

    class Config:
        from_attributes = True


class Survey(BaseModel):
    """
    Données d'un sondage renvoyé par l'API.
    """

    title: str
    subject: str


class SurveyUpdateParam(BaseModel):
    survey_id: int
    title: str
    subject: str


class Question(BaseModel):
    """
    une question dans la base de données.
    """

    type: QuestionType
    text: str
    media: str


class QuestionUpdate(BaseModel):
    """
    une question dans la base de données.
    """

    type: QuestionType
    question_id: int
    text: str
    media: str


class Answer(BaseModel):
    """
    Une réponse dans la base de données.
    """

    id_answer: int
    text: str
    is_good_answer: bool


class AnswerCreate(BaseModel):
    """
    Une réponse dans la base de données.
    """

    question_id: int
    text: str
    is_good_answer: bool


class SurveyRead(BaseModel):
    """
    Données d'un questionnaire renvoyé par l'API.
    """

    id: int
    user_id: int
    subject: str
    title: str


class QuestionRead(BaseModel):
    """
    Données d'une question renvoyé par l'API.
    """

    text: str
    answers: list[Answer]


class GroupCreated(BaseModel):
    """
    Données d'un groupe renvoyé par l'API.
    """

    id: int
    creator_id: int
    group_name: str


class GroupRead(BaseModel):
    """
    Données d'un groupe renvoyé par l'API.
    """

    id: int
    creator_id: int
    group_name: str
    parent_id: int | None = None


class GroupMember(BaseModel):
    """
    Données d'un membre d'un groupe renvoyé par l'API.
    """

    user_id: int
    group_id: int


class SessionTemplateBase(BaseModel):
    """
    Modèle de base des modèles de sessions.
    """

    name: str
    type: SurveySessionType = SurveySessionType.piloted
    authorised_group_id: int | None = None
    show_answers: bool = False


class SessionTemplateCreated(SessionTemplateBase):
    """
    Modèle de session dans la base de données.
    """

    id: int
    survey_id: int


class SessionTemplateCreateable(SessionTemplateBase):
    """
    Modèle de session utilisé lors de sa création.
    """

    survey_id: int


class SessionTemplateUpdateable(BaseModel):
    """
    Modèle de session utilisé lors des mises a jours update.
    """

    name: str | None = None
    type: SurveySessionType | None = None
    authorised_group_id: int | None = None
    show_answers: bool | None = None
    survey_id: int | None = None


class SessionStart(BaseModel):
    session_template_id: int


class StartedSession(BaseModel):
    join_code: str
    created_at: datetime


class SurveySession(BaseModel):
    """
    Session de questionaire déjà crée.
    Renvoyé lors de la liste des sessions.
    """

    name: str
    finished: bool
    join_code: str | None  # peut être None si finished est true
    created_at: datetime


class SurveysBase(BaseModel):
    id: int
    subject: str
    user_id: int
    title: str


class SurveyInfoBase(BaseModel):
    """
    Données d'un questionnaire renvoyé par l'API.
    """

    title: str
    id: int
    user_id: int
    subject: str


class SurveyBase(BaseModel):
    """
    Données d'une session de questionaire renvoyé par l'API.
    """

    user_id: int
    type: QuestionType
    id: int
    text: str
    media: str


class AnswerBase(BaseModel):
    """
    Données d'une réponse renvoyé par l'API.
    """

    question_id: int
    id: int
    is_correct: bool
    text: str


class SessionDetailsBase(BaseModel):
    """
    Données d'une session.
    """

    join_code: str
    survey_id: int
    survey_title: str
    owner_name: str
    correct_answers: int
    total_answers: int


class CasSetupStage(Enum):
    must_cas_login = "must_cas_login"
    logged_in = "logged_in"
    failed_login = "failed_login"


class CasSetup(BaseModel):
    stage: CasSetupStage
    url: str | None = None
    token: Token | None = None
