"""
Models pour la base de données avec SQLAlchemy.
A ne pas confondre avec les modèles de l'API.
"""
import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship

from .connection import Base


class UserAffiliation(enum.Enum):
    student = "student"
    teacher = "teacher"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    affiliation = Column(Enum(UserAffiliation))

    question = relationship("Question", back_populates="user")
    survey = relationship("Survey", back_populates="user")
    group_member = relationship("GroupMember", back_populates="user")
    group = relationship("Group", back_populates="user")
    results = relationship("Results", back_populates="user")
    session_participant = relationship("SessionParticipant", back_populates="user")


class QuestionType(enum.Enum):
    """
    Type des questions
    """

    single_answer = "single_answer"  # QCM réponse unique
    multiple_answers = "multiple_answers"  # QCM réponses multiples
    open = "open"  # Question ouverte
    open_restricted = "open_restricted"  # Question ouverte un seul mot


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    type = Column(Enum(QuestionType))
    text = Column(String)
    media = Column(String)

    user = relationship("User", back_populates="question")
    answer = relationship("Answer", back_populates="question")
    survey_question = relationship("SurveyQuestion", back_populates="question")


class Survey(Base):
    __tablename__ = "survey"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String)
    subject = Column(String)

    user = relationship("User", back_populates="survey")
    survey_question = relationship("SurveyQuestion", back_populates="survey")


class SurveyQuestion(Base):
    __tablename__ = "survey_question"

    survey_id = Column(Integer, ForeignKey("survey.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"), primary_key=True)

    survey = relationship("Survey", back_populates="survey_question")
    question = relationship("Question", back_populates="survey_question")


class SurveySessionType(enum.Enum):
    """
    Types des session de questionaires.
    """

    piloted = "piloted"  # Type de session pilotée
    auto_timer = "auto_timer"  # Type de session autonome avec minuteur
    auto_free = "auto_free"  # Type de session autonome libre


class SurveySessionTemplate(Base):
    """
    Un modèle de session de questionaire.
    Objet utilisé lors de la création et de la modification des sessions de questionaires.
    """

    __tablename__ = "survey_session_template"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("survey.id"))
    name = Column(String)
    type = Column(Enum(SurveySessionType))
    is_public = Column(Boolean, default=True)
    show_answers = Column(Boolean, default=False)  # Si on montre les réponses correctes après chaque questions
    deleted = Column(Boolean, default=False)


class SurveySession(Base):
    """
    Une session de questionaire en cours.
    Les paramètres viennent de la table survey_session_template.
    """

    __tablename__ = "survey_session"

    id = Column(Integer, primary_key=True, index=True)
    session_template_id = Column(Integer, ForeignKey("survey_session_template.id"))
    join_code = Column(String)
    created_at = Column(DateTime)

    # Etat de session en cours
    has_started = Column(Boolean, default=False)
    current_question_id = Column(Integer, ForeignKey("question.id"))

    session_participant = relationship("SessionParticipant", back_populates="survey_session")
    results = relationship("Results", back_populates="survey_session")


class SurveyResults(Base):
    __tablename__ = "survey_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("survey_session.id"), unique=True)
    saved_results = Column(Text)


class Results(Base):
    __tablename__ = "results"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    answer_id = Column(Integer, ForeignKey("answer.id"), primary_key=True)
    session_id = Column(Integer, ForeignKey("survey_session.id"), primary_key=True)

    user = relationship("User", back_populates="results")
    answer = relationship("Answer", back_populates="results")
    survey_session = relationship("SurveySession", back_populates="results")


class OpenAnswer(Base):
    """
    Réponse d'un utilisateur à une question ouverte.
    """

    __tablename__ = "open_answer"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey("question.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    session_id = Column(Integer, ForeignKey("survey_session.id"))


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    text = Column(String)
    is_correct = Column(Boolean)

    question = relationship("Question", back_populates="answer")
    results = relationship("Results", back_populates="answer")


class SessionParticipant(Base):
    __tablename__ = "session_participant"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    session_id = Column(Integer, ForeignKey("survey_session.id"), primary_key=True)

    survey_session = relationship("SurveySession", back_populates="session_participant")
    user = relationship("User", back_populates="session_participant")


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("user.id"))
    group_name = Column(String)
    parent_id = Column(Integer, ForeignKey("group.id"))

    user = relationship("User", back_populates="group")
    group_member = relationship("GroupMember", back_populates="group")


class GroupMember(Base):
    __tablename__ = "group_member"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id"), primary_key=True)

    group = relationship("Group", back_populates="group_member")
    user = relationship("User", back_populates="group_member")


class AuthorisedGroup(Base):
    """
    Groupe autorisé a participer à une session de questionaires.
    """

    __tablename__ = "authorised_group"

    group_id = Column(Integer, ForeignKey("group.id"), primary_key=True)
    session_template_id = Column(Integer, ForeignKey("survey_session_template.id"), primary_key=True)
