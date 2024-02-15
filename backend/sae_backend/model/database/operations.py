"""
Opérations sur la base de données.
"""
from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import case, exists, or_
from sqlalchemy.orm import Session
from sqlalchemy import desc, union_all
import json

from .db_models import (
    AuthorisedGroup,
    QuestionType,
    SurveyQuestion,
    SurveySession,
    SurveySessionTemplate,
    SurveySessionType,
    User,
    Question,
    Answer,
    Survey,
    Group,
    GroupMember,
    Results,
    UserAffiliation,
    OpenAnswer
)
from .db_models import SurveyResults
from ..api import api_models
from ..security import create_session_join_code

"""

Concerne les opérations sur la base de données pour les utilisateurs.

"""


def register_user(db: Session, name: str | None, surname: str | None, email: str, affiliation: UserAffiliation) -> User:
    """
    Enregistre un utilisateur dans la base de données.

    Paramètres
    ----------
    email : str
        Adresse email de l'utilisateur.

    name : str
        Prénom de l'utilisateur.

    surname : str
        Nom de l'utilisateur.

    Retour
    ------

    User
        Utilisateur enregistré dans la base de données.
    """

    new_user = User(email=email, name=name, surname=surname, affiliation=affiliation)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user(db: Session, email: str | None) -> User | None:
    """
    Renvoie l'utilisateur qui correspond à un nom d'utilisateur de la base de données.

    Paramètres
    ----------

    email : str
        Nom d'utilisateur.

    Retour
    ------

    User | None
        Utilisateur correspondant à l'email ou None si aucun utilisateur ne correspond.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Renvoie l'utilisateur qui correspond à un id de la base de données.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur.

    Retour
    ------

    User | None
        Utilisateur correspondant à l'id ou None si aucun utilisateur ne correspond.
    """
    return db.query(User).filter(User.id == user_id).first()


def modify_user(db: Session, email: str, name: str | None, surname: str | None) -> User:
    """
    Modifie les données d'un utilisateur.

    Paramètres
    ----------

    name : str
        Prénom de l'utilisateur.

    surname : str
        Nom de l'utilisateur.
    """
    user = db.query(User).filter(User.email == email).first()

    if name is not None:
        user.name = name  # type: ignore

    if surname is not None:
        user.surname = surname  # type: ignore

    db.commit()
    db.refresh(user)

    return user


"""

Concerne les opérations sur la base de données pour les questions.

"""


def create_survey(db: Session, user_id: int, title: str, subject: str) -> Survey:
    """
    Enregistre la création d'un questionnaire dans la base de données.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    title : str
        le titre du questionnaire

    subject : str
        le sujet du questionnaire

    Retour
    ------

    Survey
        questionnaire enregistré dans la base de données.
    """
    new_survey = Survey(user_id=user_id, title=title, subject=subject)
    db.add(new_survey)
    db.commit()
    db.refresh(new_survey)

    return new_survey


def get_surveys(db: Session, user_id: int) -> list[Survey]:
    """
    Renvoie tous les questionnaires appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    Retour
    ------

    list[Survey]
        questionnaires appartenant à l'utilisateur connecté ou
        None si aucun questionnaire ne correspond.
    """
    return db.query(Survey).filter(Survey.user_id == user_id).all()


def get_survey_info(db: Session, user_id: int, survey_id: int) -> Survey | None:
    """
    Renvoie le questionnaire qui correspond à l'id de questionnaire passé en paramètre et
    appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    survey_id : int
        Id du questionnaire.

    Retour
    ------

    Survey | None
        questionnaire correspondant à l'id du questionnaire et appartenant à l'utilisateur connecté ou
        None si aucun questionnaire ne correspond.
    """
    creator = db.query(Survey).filter(Survey.user_id == user_id, Survey.id == survey_id).first()
    if creator is None:
        return None
    return creator


def get_survey(db: Session, user_id: int, survey_id: int) -> list[SurveyQuestion] | list[Question] | None:
    """
    Renvoie les questions du questionnaire qui correspond à l'id de questionnaire passé en paramètre et
    appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    survey_id : int
        Id du questionnaire.

    Retour
    ------

    Survey | None
        questionnaire correspondant à l'id du questionnaire et appartenant à l'utilisateur connecté ou
        None si aucun questionnaire ne correspond.
    """
    creator = db.query(Survey).filter(Survey.user_id == user_id, Survey.id == survey_id).first()
    if creator is None:
        return None
    link = db.query(SurveyQuestion).filter(SurveyQuestion.survey_id == survey_id).all()
    if link is None:
        return None
    question_ids = [question.question_id for question in link]
    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
    return questions


def update_survey(db: Session, user_id: int, survey_id: int, title: str, subject: str) -> Survey | None:
    """
    Met à jour le questionnaire qui correspond à l'id questionnaire passé en paramètre et
    appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    survey_id : int
        Id du questionnaire.

    title : str
        le titre du questionnaire

    subject : str
        le sujet du questionnaire

    Retour
    ------

    Survey | None
        questionnaire correspondant à l'id du questionnaire et appartenant à l'utilisateur connecté ou
        None si aucun questionnaire ne correspond.
    """
    creator = db.query(Survey).filter(Survey.user_id == user_id, Survey.id == survey_id).first()
    if creator is None:
        return None
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if survey is None:
        return None
    survey.title = title  # type: ignore
    survey.subject = subject  # type: ignore
    db.commit()
    db.refresh(survey)
    return survey


def delete_survey(db: Session, user_id: int, survey_id: int) -> Survey | None:
    """
    Supprime le questionnaire qui correspond à l'id questionnaire passé en paramètre et
    appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    survey_id : int
        Id du questionnaire.

    Retour
    ------

    Survey | None
        questionnaire correspondant à l'id du questionnaire et appartenant à l'utilisateur connecté ou
        None si aucun questionnaire ne correspond.
    """
    survey = db.query(Survey).filter(Survey.user_id == user_id, Survey.id == survey_id).first()
    if survey is None:
        return None

    db.query(SurveyQuestion).filter(SurveyQuestion.survey_id == survey_id).delete(synchronize_session=False)
    db.delete(survey)
    db.commit()
    return survey


def add_question_to_survey(db: Session, user_id: int, survey_id: int, question_id: int) -> SurveyQuestion | None:
    """
    Ajoute une question à un questionnaire dans la base de données si l'utilisateur connecté passé en paramètre
    est bien le propriétaire de la question et du questionnaire passé en paramètre.

    Paramètres
    ----------
    user_id : int
        Id de l'utilisateur connecté.

    survey_id : int
        Id du questionnaire.

    question_id : int
        Id de la question.

    Retour
    ------

        le questionnaire avec la question ajoutée ou
        None si l'utilisateur n'est pas le créateur du questionnaire ou de la question, ou des deux.
    """
    check1 = db.query(Survey).filter(Survey.id == survey_id, Survey.user_id == user_id).first()
    if check1 is None:
        return None
    check2 = db.query(Question).filter(Question.id == question_id, Question.user_id == user_id).first()
    if check2 is None:
        return None
    new_survey_question = SurveyQuestion(survey_id=survey_id, question_id=question_id)
    db.add(new_survey_question)
    db.commit()
    db.refresh(new_survey_question)

    return new_survey_question


def remove_question_from_survey(db: Session, user_id: int, survey_id: int, question_id: int) -> dict[str, str] | None:
    """
    Enlève une question à un questionnaire dans la base de données.

    Paramètres
    ----------
    user_id : int
        Id de l'utilisateur connecté.

    survey_id : int
        Id du questionnaire.

    question_id : int
        Id de la question.

    Retour
    ------

        message de confirmation.
    """
    check1 = db.query(Survey).filter(Survey.id == survey_id, Survey.user_id == user_id).first()
    if check1 is None:
        return None
    check2 = db.query(Question).filter(Question.id == question_id, Question.user_id == user_id).first()
    if check2 is None:
        return None
    survey_question = (
        db.query(SurveyQuestion)
        .filter(SurveyQuestion.survey_id == survey_id, SurveyQuestion.question_id == question_id)
        .first()
    )
    if survey_question is None:
        return None
    db.delete(survey_question)
    db.commit()
    return {"message": "Question supprimée du questionnaire"}


def create_question(db: Session, user_id: int, type: QuestionType, text: str, media: str | None) -> Question:
    """
    Enregistre la création d'une nouvelle question dans la base de données.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    is_multiple : bool
        Si la question est à choix multiple ou non.

    text : str
        le texte de la question

    media : str | None
        si la question contient un média, son url

    Retour
    ------

    Question
        Question enregistrée dans la base de données.
    """
    new_question = Question(user_id=user_id, type=type, text=text, media=media)

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


def get_questions(db: Session, user_id: int) -> list[Question] | None:
    """
    Renvoie les toutes les quesions créé par un utilisateur (celui connecté).

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    Retour
    ------

    list[Question] | None
        Questions qui sont créées par l'utilisateur connecté ou None si aucune questions ne correspond.
    """
    return db.query(Question).filter(Question.user_id == user_id).all()


def get_question(db: Session, user_id: int, question_id: int) -> Question | None:
    """
    Renvoie la question qui correspond a l'id de la question et vérifie qu'elle appartient a
    l'utilisateur qui est connecté.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    question_id : int
        Id de la question.

    Retour
    ------

    Question | None
        Question correspondant à l'id ou None si aucune question ne correspond.
    """

    creator = db.query(Question).filter(Question.user_id == user_id, Question.id == question_id).first()
    if creator is None:
        return None
    return creator


def update_question(
    db: Session, user_id: int, question_id: int, text: str, media: str | None, type: QuestionType
) -> Question | None:
    """
    Met à jour la question qui correspond à l'id de question passé en paramètre et
    vérifie qu'elle à été créée par l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    question_id : int
        Id de la question.

    text : str
        le texte de la question

    media : str | None
        si la question contient un média, son url

    Retour
    ------

    Question | None
        Question correspondant à l'id question et appartenant à l'utilisateur ou
        None si aucune question ne correspond.
    """
    creator = db.query(Question).filter(Question.user_id == user_id, Question.id == question_id).first()
    if creator is None:
        return None
    question = get_question(db, user_id, question_id)  # type: ignore
    if question is None:
        return None
    question.text = text  # type: ignore
    question.media = media  # type: ignore
    question.type = type  # type: ignore
    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, user_id: int, question_id: int) -> Question | None:
    """
    Supprime la question qui correspond à l'id de la question passé en paramètre et
    appartenant à l'utilisateur connecté passsé en paramètre si l'autorisation est en vrai en paramètre.
    supprime égallement le lien question-questionnaire si il existe et supprime les réponses liées à la question.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    question_id : int
        Id de la question.

    Retour
    ------

    Question | None
        Question correspondant à l'id de la question et appartenant à l'utilisateur ou
        None si aucune question ne correspond ou si l'autorisation n'est pas donné.
    """
    question = db.query(Question).filter(Question.user_id == user_id, Question.id == question_id).first()
    if question is None:
        return None

    db.query(Answer).filter(Answer.question_id == question_id).delete()
    db.query(SurveyQuestion).filter(SurveyQuestion.question_id == question_id).delete()

    db.delete(question)
    db.commit()

    return question


def create_answer(db: Session, user_id: int, question_id: int, text: str, is_correct: bool) -> Answer | None:
    """
    Enregistre la création d'une nouvelle réponse dans la base de données.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    question_id : int
        Id de la question à laquelle la réponse est liée.

    text : str
        le texte de la réponse

    is_correct : bool
        si la réponse est la bonne réponse ou non
    """
    creator = (
        db.query(Question)
        .filter(
            Question.id == question_id,
            Question.user_id == user_id,
            or_(Question.type == QuestionType.multiple_answers, Question.type == QuestionType.single_answer),
        )
        .first()
    )
    if creator is None:
        return None
    new_answer = Answer(question_id=question_id, text=text, is_correct=is_correct)
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer


def get_answers(db: Session, user_id: int, question_id: int) -> list[Answer] | None:
    """
    Renvoie les réponses qui correspondent à l'id de la question passé en paramètre et
    appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    question_id : int
        Id de la question.

    Retour
    ------

    list[Answer]
        Réponses correspondantes à l'id de la question et appartenant à l'utilisateur connecté ou
        None si aucune réponse ne correspond (ou bien si il s'agit d'un type de réponse ouverte).
    """
    creator = db.query(Question).filter(Question.user_id == user_id, Question.id == question_id).first()
    if creator is None:
        return None
    return db.query(Answer).filter(Answer.question_id == question_id).all()


def get_answer(db: Session, user_id: int, answer_id: int) -> Answer | None:
    """
    Renvoie la réponse correspondant à l'id de la réponse passé en paramètre,
    et appartenant à l'utilisateur connecté.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    answer_id : int
        Id de la réponse.

    Retour
    ------

    Answer | None
        Réponse correspondant à l'id ou None si aucune réponse ne correspond.
    """
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if answer is None:
        return None
    creator = db.query(Question).filter(Question.user_id == user_id, Question.id == answer.question_id).first()
    if creator is None:
        return None
    return db.query(Answer).filter(Answer.id == answer_id).first()


def update_answer(db: Session, user_id: int, answer_id: int, text: str, is_correct: bool) -> Answer | None:
    """
    Met à jour la réponse qui correspond à l'id de la réponse passé en paramètre et
    appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    answer_id : int
        Id de la réponse.

    text : str
        le texte de la réponse

    is_correct : bool
        si la réponse est la bonne réponse ou non

    Retour
    ------

    Answer | None
        Réponse correspondant à l'id de la réponse et appartenant à l'utilisateur ou
        None si aucune réponse ne correspond.
    """
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if answer is None:
        return None
    creator = db.query(Question).filter(Question.user_id == user_id, Question.id == answer.question_id).first()
    if creator is None:
        return None
    answer.text = text  # type:ignore
    answer.is_correct = is_correct  # type:ignore
    db.commit()
    db.refresh(answer)
    return answer


def delete_answer(db: Session, user_id: int, answer_id: int) -> Answer | None:
    """
    Supprime la réponse qui correspond à l'id de la réponse passé en paramètre et
    appartenant à l'utilisateur connecté passé en paramètre.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur connecté.

    answer_id : int
        Id de la réponse.

    Retour
    ------

    Answer | None
        Réponse correspondant à l'id de la réponse et appartenant à l'utilisateur connecté ou
        None si aucune réponse ne correspond.
    """
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if answer is None:
        return None
    creator = db.query(Question).filter(Question.user_id == user_id, Question.id == answer.question_id).first()
    if creator is None:
        return None
    answer = get_answer(db, user_id, answer_id)
    if answer is None:
        return None
    db.delete(answer)
    db.commit()
    return answer


"""

Concerne les opérations sur la base de données pour les groupes.

"""


def add_user_to_group(db: Session, user_id: int, added_member_id: int, group_id: int) -> GroupMember | None:
    """
    Ajoute un utilisateur à un groupe dans la base de données.

    Paramètres
    ----------
    user_id : int
        Id de l'utilisateur propriétaire du groupe.

    added_member_id : int
        Id de l'utilisateur à ajouter.

    group_id : int
        Id du groupe.

    Retour
    ------

        Membre du groupe enregistré dans la base de données ou
        None si l'utilisateur n'est pas le créateur du groupe.
    """
    creator_id = db.query(Group.creator_id).filter(Group.id == group_id).scalar()
    if creator_id != user_id:
        return None
    new_group_member = GroupMember(user_id=added_member_id, group_id=group_id)
    db.add(new_group_member)
    db.commit()
    db.refresh(new_group_member)

    return new_group_member


def create_group(db: Session, creator_id: int, group_name: str, parent_id: int | None) -> Group:
    """
    Enregistre la création d'un nouveau groupe dans la base de données.

    Paramètres
    ----------
    creator_id : int
        Id de l'utilisateur qui a créé le groupe.

    group_name : str
        le nom du groupe

    ipp : int | None
        Id du groupe parent ou None s'il n'y a pas de groupe parent.

    Retour
    ------

        Groupe enregistré dans la base de données.
    """
    new_group = Group(creator_id=creator_id, group_name=group_name, parent_id=parent_id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    return new_group


def get_groups(db: Session) -> list[Group]:
    """
    Renvoie tous les groupes qui sont dans la base de données.

    Retour
    ------

    list[Group]
        Tous les groupes ou
        None s'il n'y a aucun groupe.
    """
    return db.query(Group).all()


def get_user_groups(db: Session, user_id: int) -> list[Group]:
    """
    Renvoie tous les groupes qui sont dans la base de données et dont l'utilisateur connecté est membre.

    Paramètres
    ----------
    user_id : int
        Id de l'utilisateur connecté.

    Retour
    ------

    list[Group]
        Tous les groupes dont l'utilisateur connecté est membre ou
        None s'il n'y a aucun groupe.
    """
    return db.query(Group).join(GroupMember).filter(GroupMember.user_id == user_id).all()


def get_group(db: Session, group_id: int) -> Group | None:
    """
    Renvoie le groupe qui correspond à l'id du groupe passé en paramètre.

    Paramètres
    ----------

    group_id : int
        Id du groupe.

    Retour
    ------

    Group | None
        Groupe correspondant à l'id du groupe ou
        None si aucun groupe ne correspond.
    """
    return db.query(Group).filter(Group.id == group_id).first()


def update_group(db: Session, group_id: int, group_name: str) -> Group | None:
    """
    Met à jour le groupe qui correspond à l'id du groupe passé en paramètre et
    dont le nom correspond à celui passé en paramètre.

    Paramètres
    ----------

    group_id : int
        Id du groupe.

    name : str
        le nom du groupe.

    Retour
    ------

    Group | None
        Groupe correspondant à l'id ou
        None si aucun groupe ne correspond.
    """
    group = get_group(db, group_id)
    if group is None:
        return None
    group.group_name = group_name  # type: ignore
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group_id: int) -> Group | None:
    """
    Supprime le groupe qui correspond à un id de la base de données.

    Paramètres
    ----------

    group_id : int
        Id du groupe.

    Retour
    ------

    Group | None
        Groupe correspondant à l'id ou None si aucun groupe ne correspond.
    """
    group = get_group(db, group_id)
    if group is None:
        return None
    db.delete(group)
    db.commit()
    return group


def get_group_users(db: Session, group_id: int) -> list[User] | None:
    """
    Renvoie les utilisateurs qui sont dans le groupe dont l'id est passé en paramètre.

    Paramètres
    ----------

    group_id : int
        Id du groupe.
    Retour
    ------
    list[User] | None
        Utilisateurs qui sont dans le groupe ou
        None si aucun utilisateur ne correspond.
    """
    return db.query(User).join(GroupMember).filter(GroupMember.group_id == group_id).all()


def get_authorised_group_id(db: Session, template: SurveySessionTemplate) -> int | None:
    """
    Renvoie l'id du groupe auquel les participants sont autorisé a participer à la session.
    """

    return db.query(AuthorisedGroup.group_id).filter(AuthorisedGroup.session_template_id == template.id).scalar()


def get_all_session_templates(db: Session, user_id: int) -> Sequence[SurveySessionTemplate] | None:
    """
    Renvoie tous les modèles de session de l'utilisateur.
    """

    return (
        db.query(SurveySessionTemplate)
        .join(Survey)
        .join(User)
        .filter(User.id == user_id)
        .filter(SurveySessionTemplate.deleted == False)  # noqa
        .all()
    )


def get_session_template(db: Session, user_id: int, session_template_id: int) -> SurveySessionTemplate | None:
    """
    Renvoie des infomrations sur un modèle de session.
    """

    return (
        db.query(SurveySessionTemplate)
        .join(Survey)
        .join(User)
        .filter(User.id == user_id)
        .filter(SurveySessionTemplate.id == session_template_id)
        .filter(SurveySessionTemplate.deleted == False)  # noqa
    ).first()


def create_session_template(
    db: Session,
    user_id: int,
    survey_id: int,
    name: str,
    type: SurveySessionType,
    authorised_group_id: int | None,
    show_answers: bool,
) -> SurveySessionTemplate | None:
    """
    Crée un modèle de session.
    """

    # Est-ce qu'on a le droit de créer un modèle de session depuis ce questionaire ?
    survey_creator_id = db.query(Survey.user_id).filter(Survey.id == survey_id).scalar()
    if survey_creator_id != user_id:
        return None

    is_public = authorised_group_id is None

    template = SurveySessionTemplate(
        survey_id=survey_id, name=name, type=type, is_public=is_public, show_answers=show_answers
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    if not is_public:
        auth = AuthorisedGroup(group_id=authorised_group_id, session_template_id=template.id)
        db.add(auth)
        db.commit()
        db.refresh(template)

    return template


def update_session_template(
    db: Session,
    user_id: int,
    session_template_id: int,
    survey_id: int | None,
    name: str | None,
    type: SurveySessionType | None,
    authorised_group_id: int | None,
    show_answers: bool | None,
) -> SurveySessionTemplate | None:
    """
    Modifie un modele de session.
    """

    session_template: SurveySessionTemplate = (
        db.query(SurveySessionTemplate)
        .join(Survey)
        .join(User)
        .filter(SurveySessionTemplate.id == session_template_id)
        .filter(SurveySessionTemplate.deleted == False)  # noqa
        .filter(User.id == user_id)
    ).first()

    if not session_template:
        return None

    if survey_id is not None:
        session_template.survey_id = survey_id  # type: ignore

    if name is not None:
        session_template.name = name  # type: ignore

    if type is not None:
        session_template.type = type  # type: ignore

    if authorised_group_id is None:
        session_template.is_public = True  # type: ignore
        db.query(AuthorisedGroup).filter(AuthorisedGroup.session_template_id == session_template_id).delete()
    else:
        session_template.is_public = False  # type: ignore
        # On supprime l'ancien groupe lié
        db.query(AuthorisedGroup).filter(AuthorisedGroup.session_template_id == session_template_id).delete()
        auth = AuthorisedGroup(group_id=authorised_group_id, session_template_id=session_template_id)
        db.add(auth)

    if show_answers is not None:
        session_template.show_answers = show_answers  # type: ignore

    db.commit()
    db.refresh(session_template)

    return session_template


def delete_session_template(db: Session, user_id: int, session_template_id: int) -> bool:
    """
    Supprime un modèle de session.
    """

    session_template: SurveySessionTemplate = (
        db.query(SurveySessionTemplate)
        .join(Survey)
        .join(User)
        .filter(SurveySessionTemplate.id == session_template_id)
        .filter(User.id == user_id)
    ).first()

    if not session_template:
        return False

    session_template.deleted = True  # type: ignore
    db.commit()
    db.refresh(session_template)

    return True


def start_survey_session(db: Session, user_id: int, session_template_id: int) -> SurveySession:
    """
    Démarre une session de questionaires.
    """

    template_owner_id = (
        db.query(Survey.user_id).join(SurveySessionTemplate).filter(SurveySessionTemplate.id == session_template_id)
    ).scalar()

    if not template_owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="A session template with this id does not exist."
        )

    if template_owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You must own the template to be able to start a session."
        )

    survey_session = SurveySession(session_template_id=session_template_id, created_at=datetime.now())
    survey_session.join_code = create_session_join_code(survey_session.id)  # type: ignore

    db.add(survey_session)
    db.commit()
    db.refresh(survey_session)

    return survey_session


def get_all_session(db: Session, user_id: int) -> list[api_models.SurveySession]:
    """
    Renvoie la liste de toutes les sessions (en cours et finies) lancées par l'utilisateur.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur ayant lancé ces sessions.

    Retour
    ------

    list[SurveySession]
        Liste de toutes les sessions.
    """

    results_attached = exists().where(Results.session_id == SurveySession.id)
    sessions = (
        db.query(
            SurveySession.created_at,
            case((results_attached, True), else_=False).label("is_finished"),
            SurveySession.join_code.label("join_code"),
            SurveySessionTemplate.name.label("template_name"),
        )
        .join(SurveySessionTemplate)
        .join(Survey)
        .join(User)
        .filter(User.id == user_id)
        .order_by(desc(SurveySession.created_at))
    ).all()

    return [
        api_models.SurveySession(
            created_at=sess.created_at,
            finished=sess.is_finished,
            join_code=sess.join_code,
            name=sess.template_name,
        )
        for sess in sessions
    ]


def remove_member(db: Session, group_id: int, user_id: int, removed_user_id: int) -> GroupMember | None:
    """
    Supprime un utilisateur d'un groupe dans la base de données.

    Paramètres

    ----------

    group_id : int
        Id du groupe.

    user_id : int
        Id de l'utilisateur propriétaire du groupe.

    removed_user_id : int
        Id de l'utilisateur à supprimer.

    Retour
    ------

    User | None
        l'utilisateur supprimé du groupe ou None si l'utilisateur n'est pas le créateur du
        groupe ou l'utilisateur a supprimé n'est pas dans le groupe.
    """
    creator_id = db.query(Group.creator_id).filter(Group.id == group_id).scalar()
    group = get_group(db, group_id)
    if group is None:
        return None
    if creator_id != user_id:
        return None
    group_member = db.query(GroupMember).filter_by(group_id=group_id, user_id=removed_user_id).first()
    if group_member is None:
        return None
    db.delete(group_member)
    db.commit()
    return group_member


def get_saved_results(db: Session, code: str) -> str:
    """
    Récupère le résultat du questionnaire.

    Paramètres

    ----------

    join_code : str
        Code de la session.

    Retour
    ------

    str | None
        le résultat du questionnaire
    """
    saved_id = db.query(SurveySession.id).filter(SurveySession.join_code == code).scalar()
    return db.query(SurveyResults.saved_results).filter(SurveyResults.session_id == saved_id).scalar()


def add_name_to_players(db: Session, infos_players) -> str:
    """
    Ajoute les noms de joueurs en fonction de leur id dans le json

    Paramètres

    ----------

    infos_players
        Json avec id_player, questions_answers

    Retour
    ------

    str
        Json modifié
    """
    for player in infos_players:
        user = db.query(User).filter(User.id == int(player["id_player"])).scalar()
        player["name"] = user.name + " " + user.surname

    return infos_players


def add_name_to_player(db: Session, infos_players) -> str:
    """
    Ajoute le noms du joueur en fonction de son id dans le json

    Paramètres

    ----------

    infos_players
        Json avec id_player, questions_answers

    Retour
    ------

    str
        Json modifié
    """
    user = db.query(User).filter(User.id == int(infos_players["id_player"])).scalar()
    infos_players["name"] = user.name + " " + user.surname

    return infos_players


def get_sessions_player(db: Session, user_id: int) -> str:
    """
    Renvoie la liste des sessions auxquelles l'utilisateur a participé.

    Paramètres
    ----------

    user_id : int
        Id de l'utilisateur.

    Retour
    ------

    str | None
        Liste des sessions auxquelles l'utilisateur a participé au format JSON.
    """
    results_query = (
        db.query(Results.session_id)
        .filter(Results.user_id == user_id)
        .order_by(desc(Results.session_id))
        .distinct()
    )

    open_answer_query = (
        db.query(OpenAnswer.session_id)
        .filter(OpenAnswer.user_id == user_id)
        .order_by(desc(OpenAnswer.session_id))
        .distinct()
    )

    combined_query = union_all(results_query, open_answer_query)

    combined_results = db.execute(combined_query).fetchall()

    unique_results = set(result[0] for result in combined_results)

    return str(list(unique_results))


def get_join_code_survey_id(db: Session, results: str):
    """
    Renvoie le code pour rejoindre et l'id du questionnaire des sessions

    Paramètres
    ----------

    results : list
        Liste de tuples des sessions.

    Retour
    ------

    str
        JSON du join code et du survey auxquelles l'utilisateur a participé.
    """
    results_list_clean = []

    for session in results:
        results_list_clean.extend(int(val) for val in session if val.isdigit())

    results_list = []

    for session_id in results_list_clean:
        join_code = db.query(SurveySession.join_code).filter(SurveySession.id == session_id).scalar()
        session_template_id = (
            db.query(SurveySession.session_template_id).filter(SurveySession.id == session_id).scalar()
        )
        survey_id = (
            db.query(SurveySessionTemplate.survey_id).filter(SurveySessionTemplate.id == session_template_id).scalar()
        )

        result_dict = {"session_id": session_id, "join_code": join_code, "survey_id": survey_id}
        results_list.append(result_dict)

    return results_list


def get_name_survey_owner(db: Session, results: str) -> str:
    """
    Renvoie le nom du questionnaire, son id et le nom de l'utilisateur qui l'a créé

    Paramètres
    ----------

    results : list
        JSON du join code et du survey.

    Retour
    ------

    str
        JSON du join code, du nom questionnaire, son id, et propriétaire.
    """
    for result in results:
        survey_id = result["survey_id"]  # type: ignore
        survey = db.query(Survey.title, Survey.user_id).filter(Survey.id == survey_id).first()

        if survey:
            title, user_id = survey
            owner_name = db.query(User.name).filter(User.id == user_id).first()

            if owner_name:
                owner_name = owner_name[0]
                result["survey_title"] = title  # type: ignore
                result["owner_name"] = owner_name  # type: ignore

    return results


def get_sessions_results(db: Session, results: str, user_id: int) -> str:
    """
    Renvoie le resultat sauvegardé des sessions.

    Paramètres
    ----------

    results : str
        JSON du du questionnaire, son id et le nom de l'utilisateur qui l'a créé.

    Retour
    ------

    str
        JSON des résultats sauvegardés.
    """
    results.reverse()
    for result in results:
        session_id = result.get("session_id")
        saved_results_row = db.query(SurveyResults.saved_results).filter(SurveyResults.session_id == session_id).first()

        if saved_results_row:
            saved_results_str = saved_results_row.saved_results

            saved_results = json.loads(saved_results_str)
            result["saved_results"] = saved_results

            player_results = saved_results.get(str(user_id), {})
            total_questions = len(player_results)
            correct_answers = sum(answer.get("correctly_answered", False) for answer in player_results.values())
            total_open_answers = sum(1 for answer in player_results.values() if "correctly_answered" not in answer)
            total_answers = total_questions - total_open_answers

            result["correct_answers"] = correct_answers
            result["total_open_answers"] = total_open_answers
            result["total_answers"] = total_answers

            result.pop("survey_id", None)
            result["id_player"] = user_id

    return results
